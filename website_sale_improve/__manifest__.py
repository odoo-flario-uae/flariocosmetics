# -*- encoding: utf-8 -*-

{
    'name': 'Editing website page',
    'category': 'Website/Website',
    'summary': 'Update Website pages',
    'version': '1.0',
    'description': "Module for updating and changing view of website pages",
    'depends': [
        'website',
        'sale'
    ],
    'data': [
        'views/website_sale_product_inherit.xml', 
        'views/res_config_settings_views.xml'
    ],
    'license': 'LGPL-3',
}
