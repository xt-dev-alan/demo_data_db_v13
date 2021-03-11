# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _get_current_address(self, type, order=False):
        sale_order = self.env['sale.order']
        if not order:
            if type == 'invoice':
                partner_ids = self.child_ids.filtered(lambda r: r.type == 'invoice')
                return partner_ids[0] if partner_ids else self
            else:
                partner_ids = self.child_ids.filtered(lambda r: r.type == 'delivery')
                return partner_ids[0] if partner_ids else self
        else:
            order_id = sale_order.search([('name', '=', order)], limit=1)
            if type == 'invoice':
                return order_id.partner_invoice_id
            else:
                partner_ids = self.child_ids.filtered(lambda r: r.type == 'delivery')
                return order_id.partner_shipping_id



    