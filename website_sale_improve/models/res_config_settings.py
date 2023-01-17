from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    telegram_token = fields.Char(
        string='Telegram tolen',
        related='website_id.telegram_token',
        readonly=False)
    telegram_chat_id = fields.Char(
        string='Telegram chat ID',
        related='website_id.telegram_chat_id',
        readonly=False)
