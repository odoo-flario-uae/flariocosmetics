# -*- coding: utf-8 -*-
{
    'name': "invoice_reports",

    'summary': """
        Update report of invoice""",

    'description': """
        Change description to product display name,
        Add company ID,
        Add company  
    """,

    'author': "pandrosov",
    'website': "https://www.flario.ae",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    'depends' : ['account'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/invoice_report.xml',
        'views/report_invoice_changes.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
