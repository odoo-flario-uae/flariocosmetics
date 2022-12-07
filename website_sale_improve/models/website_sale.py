# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class Website(models.Model):
    _inherit = 'website_sale'
    extra_communication_method = fields.Selection(selection=[('whatsapp','WhatsApp'),('email','Email'),('by_phone','By phone')],string='Communication method')

