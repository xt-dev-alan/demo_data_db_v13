# -*- coding: utf-8 -*-
import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(  __name__ )

class SaleQuotePricing(models.Model):
    _name = 'sale.quote.pricing'
    _description = 'Sale Quote Pricing'

    order_line_id = fields.Many2one('sale.order.line', string='Line')
    order_id = fields.Many2one('sale.order', string='Order')

    WEB = fields.Float(string='WEB', required=True)
    index_q = fields.Float(string='Index', required=True)
    up = fields.Float(string='#Up', required=True)
    material = fields.Char(string='Material',required=True)
    gauge = fields.Float(string='Gauge',required=True)
    gravity = fields.Float(string='Spec Gravity', required=True)
    color = fields.Char(string='Color', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda s: s.env.user.company_id.currency_id)

    tool_cost = fields.Monetary(string='Tool Cost')
    freight_cost = fields.Monetary(string='Freight Cost')

    material_qty = fields.Float(string="Material $/Lbs")
    qty = fields.Integer(string="Quantity")
    labor_rate =  fields.Float(string="Labor Rate")
    line_speed = fields.Float(string="Line Speed")
    commission = fields.Float(string="Comm %")
    

    # TOTALS 

    total_shots = fields.Float(string='Total Shots', compute="_compute_total_shots")
    total_material_pound = fields.Float(string='Total Materia Pound', compute="_compute_total_material_pound")
    total_material_yards = fields.Float(string='Total Material Yards', compute="_compute_total_material_yards")
    total_material = fields.Float(string='Total Material $', compute="_compute_total_material")
    total_material_m = fields.Float(string='Material $/m', compute="_compute_total_material_m")
    labor_rate_m = fields.Float(string='Labor Rate/m', compute="_compute_labor_rate_m")
    total_labor = fields.Float(string='Total Labor', compute="_compute_total_labor")
    part_cost = fields.Monetary(string='Part Cost/ k', compute="_compute_part_cost")
    total_k = fields.Monetary(string='Total/ k', compute="_compute_part_cost")
    total_commision = fields.Monetary(string='Total Commision', compute="_compute_part_cost")
    dlp_unit_price = fields.Monetary(string="Price / Unit", compute = "_compute_unit_price")

    @api.depends('labor_rate_m', 'total_material_m', 'commission')
    def _compute_part_cost(self):
        for record in self:
            part_cost = record.labor_rate_m + record.total_material_m
            record.update({
                'part_cost': part_cost,
                'total_k':  (part_cost * record.commission / 100) + part_cost,
                'total_commision': part_cost * record.commission / 100,
                })


    @api.depends('total_k')
    def _compute_unit_price(self):
        for record in self:
            dlp_unit_price_c = 0.0
            if record.total_k:
                dlp_unit_price_c = record.total_k / 1000
            record.update({
                'dlp_unit_price': dlp_unit_price_c
                })


    @api.depends('qty', 'up')
    def _compute_total_shots(self):
        for record in self:
            shots = 0.0
            if record.qty and record.up:
                shots = record.qty / record.up
            record.update({
                'total_shots': shots
                })

    @api.depends('gauge', 'WEB', 'index_q', 'gravity', 'total_shots' )
    def _compute_total_material_pound(self):
        for record in self:
            pound = record.gauge * (record.WEB + 1.5) * (record.index_q + 0.5) * record.gravity * record.total_shots
            record.update({
                'total_material_pound': pound
                })

    @api.depends('index_q', 'total_shots')
    def _compute_total_material_yards(self):
        for record in self:
            yards = (record.index_q + 0.5) * (record.total_shots / 36)
            record.update({
                'total_material_yards': yards
                })

    @api.depends('total_material_pound', 'material_qty')
    def _compute_total_material(self):
        for record in self:
            material = record.total_material_pound * record.material_qty
            record.update({
                    'total_material': material
                    })

    @api.depends('material_qty')
    def _compute_total_material_m(self):
        for record in self:
            try:
                material = (record.gauge * (record.WEB + 1.5) * (record.index_q + 0.5) 
                        * record.gravity * 1000) * (record.material_qty / record.up)
            except:
                material = 0.0
            record.update({
                    'total_material_m': material
                    })            

    @api.depends('labor_rate', 'line_speed')
    def _compute_labor_rate_m(self):
        for record in self:
            try:
                labor_rate = (record.labor_rate * (record.qty / 1000) / (record.up * record.line_speed) * 1000) / (record.qty / 1000)
            except:
                labor_rate = 0.0
            record.update({
                    'labor_rate_m': labor_rate
                    }) 

    @api.depends('total_shots', 'line_speed', 'labor_rate')
    def _compute_total_labor(self):
        for record in self:
            try:
                total_labor = (record.total_shots / record.line_speed) * record.labor_rate
            except:
                total_labor = 0.0
            record.update({
                    'total_labor': total_labor
                    }) 


    def action_done(self):
        order_line = self.env['sale.order.line']
        if self.commission > 100 or self.commission < 0:
            raise UserError(_('Error. Ingrese comisión.'))
        name = '[DLP Project (%sx%sx%s) (%s) (%s) (%s)]'%( self.WEB, self.index_q, self.up, self.material, self.color, self.gauge )
        self.order_line_id.write({
            'name': name,
            'price_unit': self.total_k / 1000,
            'product_uom_qty': self.qty,
            'quote_pricing_id': self.id
        })
        if self.freight_cost:
            product_id = self.env.ref('custom_quote_pricing.product_freight_cost')
            order_line.create({
                'product_id': product_id.id,
                'name': product_id.name,
                'price_unit': self.freight_cost,
                'product_uom_qty': 1.0,
                'order_id': self.order_id.id
            })

        if self.tool_cost:
            product_id = self.env.ref('custom_quote_pricing.product_tool_cost')
            order_line.create({
                'product_id': product_id.id,
                'name': product_id.name,
                'price_unit': self.tool_cost,
                'product_uom_qty': 1.0,
                'order_id': self.order_id.id
            })
        