# -*- coding: utf-8 -*-

{
    'name': 'Quality MRP',
    'version': '1.0',
    'author': 'Xetechs GT',
    'license': 'LGPL-3',
    'category': 'Tools',
    'depends': [
        'mrp', 
        'quality_control_oca',
        'sale_management'
    ],
    'data': [
        'data/qc_test_views.xml',
        'views/qc_views.xml',
        'views/mrp_production_views.xml',
        'views/sale_views.xml'
    ]
}
