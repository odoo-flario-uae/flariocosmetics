# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import is_html_empty


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    reclamation = fields.Html(string='Reclamation')

    @api.onchange("reclamation")
    def _onchange_reclamation(self):
        if self.reclamation == "<p><br></p>":
            self.reclamation = False
