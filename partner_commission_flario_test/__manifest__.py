# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Resellers Commissions For Flario Test',
    'category': 'Sales/Commissions',
    'summary': 'Configure resellers commissions on subscription sale',
    'author': 'Flario',
    'version': '1.0',
    'description': """
This module allows to configure commissions for resellers.
    """,
    'depends': [
        'purchase',
        'website_crm_partner_assign',
    ],
    'data': [
        'data/data.xml',
        'security/commission_security.xml',
        'security/ir.model.access.csv',
        'views/account_move_views.xml',
        'views/purchase_order_views.xml',
        'wizard/account_move_import_csv_wizard_view.xml',
    ],
    'license': 'OEEL-1',
}
