from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'loyalty.program'

    for_amazon = fields.Boolean(string='Coupons for amazon?',
                                help="This flag for amazon discount. Checked this if you want use coupons for users",
                                default=False)

