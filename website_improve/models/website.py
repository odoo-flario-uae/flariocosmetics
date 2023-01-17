# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import  models, fields


class Website(models.Model):
    _inherit = "website"

    fast_puchasing = fields.Boolean(string="Fast purchasing for website")
    def get_pricelist_available(self, show_visible=False):
        pls = super(Website, self).get_pricelist_available(show_visible)
        partner_sudo = self.env.user.partner_id
        add_pricelist = partner_sudo.additional_pricelist
        website = self.with_company(self.company_id)
        website_pricelists = website.sudo().pricelist_ids
        if add_pricelist and add_pricelist not in pls and add_pricelist in website_pricelists:
            add_pls = pls + add_pricelist
            pls = add_pls
        return pls
