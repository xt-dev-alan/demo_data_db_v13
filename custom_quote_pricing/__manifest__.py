{
    'name': 'Custom Quote Pricing',
    'version': '1.0',
    'author': 'Xetechs GT',
    'website': 'https://xetechs.com',
    'license': 'LGPL-3',
    'depends': [
        'sale_management'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/product_data.xml',
        'views/sale_views.xml',
        'views/sale_quote_pricing_views.xml',

    ]
}