# -*- coding: utf-8 -*-
{
    'name': 'Product Pricelist Suggestion',
    'version': '17.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': """
        a custom module suggest lowest price pricelist for selected product in
        sale order line.
    """,
    'description': """
        Using a pricelist, a custom module suggests the best price pricelist
        for each sale order line.
    """,
    'website': "http://www.aktivsoftware.com",
    'author': "Aktiv Software",
    'depends': [
        'sale_management'
    ],
    'data': [
        'views/product_pricelist_view.xml',
        'views/sale_order_views.xml'
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
