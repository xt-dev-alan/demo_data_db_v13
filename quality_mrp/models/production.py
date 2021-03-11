# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger( __name__ )

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    inspection_ids = fields.One2many('qc.inspection', 'production_id', string='Inspection')
    inspection_count = fields.Integer(compute='_compute_inspection_count', string='Inspection Count')
    sale_order_id = fields.Many2one('sale.order', string="Sale Order", readonly=True)
    customer_po = fields.Char(string='Customer Po')

    @api.model
    def create(self, values):
        sale_order = self.env['sale.order'].sudo()
        production = super(MrpProduction, self).create(values)
        production.create_qc_inspection()
        if values.get('origin'):
            order_id = sale_order.search([('name', '=', values.get('origin'))])
            production.update( {'sale_order_id': order_id.id if order_id else False,
                                'customer_po': order_id.customer_po if order_id else ''} )
        return production

    def create_qc_inspection(self):
        inspection = self.env['qc.inspection'].sudo()
        test = self.env.ref('quality_mrp.default_test_for_production')
        for record in self:
            inspection_id = inspection.create({
                'production_id': record.id,
                'qty': record.product_qty,
                'test': test.id,
                'inspection_lines': inspection._prepare_inspection_lines( test )
            })
            inspection_id.name = '%s [%s]'%(inspection_id.name, record.name)

    def view_qc_inspection(self):
        action = self.env.ref('quality_control_oca.action_qc_inspection').read()[0]
        action['domain'] = [('production_id', '=', self.id)]
        return action

    @api.depends("inspection_ids")
    def _compute_inspection_count(self):
        for production in self:
            if production.inspection_ids:
                production.update( {'inspection_count': len(production.inspection_ids) } )

    