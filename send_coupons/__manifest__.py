# -*- coding: utf-8 -*-
{
    'name': "send_coupons",

    'summary': """
        Improve coupons codes in default loyalty program""",

    'description': """
        Module for send email template with coupon code to user from Amazon.ae
    """,

    'author': "Pavel Androsov",
    'website': "https://www.flario.ae",
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'loyalty'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/thankyou.xml',
        'data/menu.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
