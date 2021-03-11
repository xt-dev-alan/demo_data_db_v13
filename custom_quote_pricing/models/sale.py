# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    quote_pricing_id = fields.Many2one('sale.quote.pricing', string='Quote Pricing')

    def action_open_quote_pricing(self):
        res = {
            'name': 'Quote Pricing',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.quote.pricing',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'
        }
        if not self.quote_pricing_id:
            context = {
                'default_order_line_id': self.id,
                'default_order_id': self.order_id.id
            }
            res.update({'context': context})
        else:
            res.update({'res_id': self.quote_pricing_id.id})
        return res


    