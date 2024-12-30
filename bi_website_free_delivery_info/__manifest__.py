# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    'name': "Website Free Delivery Offers",
    'version': '16.0.0.0',
    'category': 'eCommerce',
    'summary': "Website Free Delivery Offers Free Shipping Charge on Webshop Delivery Charge Free Delivery Charges Products Shop Free Delivery Charges Free Product Shipping eCommerce Free Product Delivery Web Portal Free Delivery Charge Web Store Free Product Delivery",
    'description': """

        Website Store Product Odoo App helps users to update customer information about free delivery offers. User can view the free delivery information as per the configured shipping method in website. When the free delivery condition fulfilled, then customer will get a popup message as 'You have won FREE DELIVERY on this order'.

    """,
    "author": "BROWSEINFO",
    "price": 20,
    "currency": 'EUR',
    "website" : "https://www.browseinfo.com/demo-request?app=bi_website_free_delivery_info&version=16&edition=Community",
    'depends': ['base','website','website_sale','sale_management','account','stock','website_sale_delivery'],
    'data': [
        'views/templates.xml',
    ],
        'assets':{
        'web.assets_frontend':[
            'bi_website_free_delivery_info/static/src/scss/custom.scss',
            'bi_website_free_delivery_info/static/src/js/website_delivery.js',
        ]
    },
    'license':'OPL-1',
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://www.browseinfo.com/demo-request?app=bi_website_free_delivery_info&version=16&edition=Community',
    "images":['static/description/Website-Store-Product-Pickup-Banner.gif'],
}
