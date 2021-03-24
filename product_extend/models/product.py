# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # MAIN INFO
    num_item = fields.Char(string="# Item")
    description_x = fields.Char(string="Description")
    msrp = fields.Float(string="MSRP")
    upc = fields.Char(string="UPC")
    types = fields.Selection([('retail', 'Retail Item'), ('mfg', 'MFG Part')], string='Type')
    country_id = fields.Many2one('res.country', string="Country")
    length = fields.Char(string="Length")
    width = fields.Char(string="Width")
    depth = fields.Char(string="Depth")
    #ADD INFO
    prop65 = fields.Boolean(string="Prop 65", default=True)
    prop65_ids = fields.Many2many('product.prop65', string="Prop 65")
    reach = fields.Boolean(string='REACH', default=True)
    reach_ids = fields.Many2many('product.reach', string="REACH")
    rosh = fields.Boolean(string='RoSH', default=True)
    rohs_ids = fields.Many2many('product.rohs', string='RoHS')
    htc_id = fields.Many2one('product.htc', string="HTC")
    coo_id = fields.Many2one('product.coo', string="COO")
    shelf_pack_qty = fields.Integer(string='Shelf Pack QTY')
    pricing_schedule = fields.Selection([('wholesale', 'Wholesale'), ('distributor', 'Distributor')], string='Pricing Schedule')
    shelf_pack_barcode = fields.Char(string="Shelf Pack Barcode")
    xl_barcode = fields.Char(string="Product Barcode")
    new_uom = fields.Char(string="Unit of Measure")
    sales_BOX = fields.Char(string="BOX")
    #PRICING
    wholesale_price = fields.Float(string="Wholesale Price")
    distributor_price = fields.Float(string="Distributor Price")
    special_price = fields.Float(string="Special Price")
    
    
   

class ProductProduct(models.Model):
    _inherit = 'product.product'

        # MAIN INFO
    sales_BOX = fields.Char(string="BOX")    
    num_item = fields.Char(string="# Item")
    description_x = fields.Char(string="Description")
    msrp = fields.Float(string="MSRP")
    upc = fields.Char()
    types = fields.Selection([('retail', 'Retail Item'), ('mfg', 'MFG Part')], string='Type')
    country_id = fields.Many2one('res.country', string="Country")
    length = fields.Char(string="Length")
    width = fields.Char(string="Width")
    depth = fields.Char(string="Depth")
    #ADD INFO
    prop65 = fields.Boolean(string="Prop 65")
    reach = fields.Boolean(string='REACH', default=True)
    rosh = fields.Boolean(string='RoSH', default=True)
    rohs_ids = fields.Many2many('product.rohs', string='RoHS')
    htc_id = fields.Many2one('product.htc', string="HTC")
    coo_id = fields.Many2one('product.coo', string="COO")
    shelf_pack_qty = fields.Integer(string='Shelf Pack QTY')
    pricing_schedule = fields.Selection([('wholesale', 'Wholesale'), ('distributor', 'Distributor')], string='Pricing Schedule')
    shelf_pack_barcode = fields.Char(string="Shelf Pack Barcode")
    xl_barcode = fields.Char(string="Product Barcode")
    new_uom = fields.Char(string="Unit of Measure")
    #PRICING
    wholesale_price = fields.Float(string="Wholesale Price")
    distributor_price = fields.Float(string="Distributor Price")
    special_price = fields.Float(string="Special Price")    


# NEW MODELS
class ProductROHS(models.Model):
    _name = 'product.rohs'
    _description = 'Product ROHS'

    name = fields.Char(string='Name')

class ProductProp65(models.Model):
    _name = 'product.prop65'
    _description = 'Product prop65'

    name = fields.Char(string='Name')

class ProductReach(models.Model):
    _name = 'product.reach'
    _description = 'Product Reach'

    name = fields.Char(string='Name')

class ProductHTC(models.Model):
    _name = 'product.htc'
    _description = 'Product HTC'

    name = fields.Char(string='Name')

class ProductCOO(models.Model):
    _name = 'product.coo'
    _description = 'Product COO'
    name = fields.Char(string='Name')

            