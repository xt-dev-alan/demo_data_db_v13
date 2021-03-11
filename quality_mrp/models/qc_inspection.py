# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger( __name__ )

class QcInspection(models.Model):
    _inherit = "qc.inspection"

    production_id = fields.Many2one('mrp.production', string='Production')