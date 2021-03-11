# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLiene(models.Model):
    _inherit = 'sale.order.line'
    
    moq_qty = fields.Float(string="MOQ Qty")

