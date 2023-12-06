# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Website First Order/New User Discount in Odoo',
    'category': 'Website',
    'sequence': 7,
    'summary': 'Apps use for allow First order discount popup for new users website new order discount website first order offer new user discount first discount new user offer website new register user discount offer shop offers coupon website discount website offers',
    'website': 'https://www.browseinfo.com',
    'version': '16.0.0.0',
    'author': 'BrowseInfo',
    "description": """
    
    Purpose :-
	
	first order discount
	dicount for new user
	discount for first order 
	new order discount
	first time order discount 
	dicsount for first time buyer
	first time buyer discount 
	offer for first time order
	first order offer 
    website first user discount
    website new register user discount
	
    This Module allow users to provide first time order discount on website
    Website first order discount, Webshop First order Discount, First order discount on website, Website portal user discount,
    Website public user discount,Website order discount,Website discount on first order, Apply discount Website.
    discount on Odoo shop, Discount on webshop order, Manage discount on website, Custom discount Webshop order.
    Website discount for public users, Website discount for first order, Discount on shop for first order, New user discount on website order, Website new user discount, new register user discount on website, new register user discount on shop, Shop new user discount
    Website configurable discount for first order
    o to website settings where you can find the configuration options for website popup.
By default popup message is set but if you want to change that default message then just unchecked that default popup box after that you can set your custom message.
website Configuration Default Discount and Popup message
shop first order discount

This odoo apps help to allow First order discount for new register user on website, When visitors  comes on website after installing this module it show configure popup message on website view for new users about configured discount setup notification. You can easily configure the discount pop-up message for all website visitors also you can configure discount amount which you want to give to all new users as website promotion. This Odoo apps provides extra Website settings where you can see that configuration options for website popup. You can set your custom message for pop-up as well as configure discount percentage from this configuration options. 

    """,
    "price": 19,
    "currency": 'EUR',
    'depends': ['website', 'website_sale', 'sale_management', 'stock'],
    'installable': True,
    'data': [
        'data/demo_data.xml',
        'views/res_user.xml',
        'views/website_template.xml',
    ],

    'application': True,
    'live_test_url': 'https://youtu.be/hphqf5xwMmo',
    'license': 'OPL-1',
    "images": ['static/description/Banner.gif'],
    'assets': {
        'web.assets_frontend': [
            'bi_website_first_order_discount/static/src/js/discount_popup.js',
        ],
    },

}
