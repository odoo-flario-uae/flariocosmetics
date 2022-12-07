# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class Website(models.Model):
    _inherit = 'website'

    extra_communication_method = fields.Selection(selection=[('whatsapp','WhatsApp'),('email','Email'),('by_phone','By phone')],string='Communication method')
    telegram_token = fields.Char(string='Telegram tolen')
    telegram_chat_id = fields.Char(string='Telegram chat ID')