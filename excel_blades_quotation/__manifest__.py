# -*- coding: utf-8 -*-
{
    'name': "Excel Blades Quotation",

    'summary': """
        Sale order quotation with no prices, includes 2 reports: products only, total only""",

    'description': """
        Module developed to include a personalized quotation for EXCEL BLADES""",

    'author': "Xetechs GT",
    'website': "http://www.xetechs.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '2.1.0',

    # any module necessary for this one to work correctly
    'depends': ['sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_report_templates.xml',
        'views/sale_views.xml',
        # 'reports/report.xml',
        # 'reports/excel_blades_quotation.xml',
    ]
}
