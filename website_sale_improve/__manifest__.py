# -*- encoding: utf-8 -*-

{
    'name': 'Website Sale: Improvments',
    'category': 'Website/Website',
    'summary': 'Update Website pages',
    'version': '1.0',
    'description': "Module for updating and changing view of website pages",
    'depends': [
        'website_sale',
        'delivery'
    ],
    'data': [
        'views/website_sale_product_inherit.xml',
        'views/delivery_carrier_form_inherit.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'website_sale_improve/static/src/css/scss/amazon_button.css'
        ]
    },
    'license': 'LGPL-3',
}