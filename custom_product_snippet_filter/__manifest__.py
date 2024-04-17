# -*- coding: utf-8 -*-
{
    'name': "custom_product_snippet_filter",

    'summary': """
        Change filter product snippet""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    
    'version': '1.0',
    'depends': ['website_sale', 'website'],


    # always loaded
    'data': [
        'views/website_sale_custom_filters.xml'
    ]
}
