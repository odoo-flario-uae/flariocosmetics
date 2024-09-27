# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    additional_pricelist = fields.Many2one(
        comodel_name='product.pricelist',
        string="Additional Pricelist",
        company_dependent=False,
        domain=lambda self: [('company_id', 'in', (self.env.company.id, False))])