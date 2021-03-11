# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger( __name__ )

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_po = fields.Char(string='Customer Po')