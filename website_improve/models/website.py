# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import  models


class Website(models.Model):
    _inherit = "website"

    def get_pricelist_available(self, show_visible=False):
        pls = super(Website, self).get_pricelist_available(show_visible)
        partner_sudo = self.env.user.partner_id
        add_pricelist = partner_sudo.additional_pricelist
        if add_pricelist and add_pricelist not in pls:
            add_pls = pls + add_pricelist
            pls = add_pls
        return pls
