{
    'name': "XLSX reports",
    'summary': """ This module for export custom xlsx reports """,
    'author': "pavel androsov",
    'website': "",
    'support': 'pandrosov98@gmail.com',
    'category': 'Sale',
    'version': '16.0.1',
    'license': 'AGPL-3',
    'description': """  This module for export custom xlsx reports
    """,
    'depends': ['sale_management', 'report_xlsx'],
    'data': [
        "reports/sale_orders_xlsx_view.xml",
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
