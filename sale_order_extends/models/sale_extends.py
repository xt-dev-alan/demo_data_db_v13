# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class SalesTemplate(models.Model):
    _inherit = 'sale.order'

    # MAIN INFO

    shipping_types = fields.Selection([('FEDEX', 'Fedex'), ('UPS', 'UPS'), ('USPS', 'USPS'), ('Other', 'Other')], string='Delivery Type')
    shipping_many_types = fields.Many2many('sale.excel_shipping', string="Delivery Selection")
    shipping_datee = fields.Date(string="Shipping Date")
    customer_PO = fields.Char(string="PO Number")
    



# NEW MODELS
class SalesShippingExcel(models.Model):
    _name = 'sale.excel_shipping'
    _description = 'Sale Shipping Method'

    name = fields.Char(string='Shipping Method')



            