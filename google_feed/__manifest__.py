{
    'name': 'Google Feed',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Generate Google product feed',
    'depends': ['base', 'website_sale', 'stock', 'website'],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
