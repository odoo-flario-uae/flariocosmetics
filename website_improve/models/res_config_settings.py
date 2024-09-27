from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    website_fast_puchasing = fields.Boolean(
        string="Fast purchase",
        related='website_id.fast_puchasing',
        readonly=False)
    telegram_token = fields.Char(
        string='Telegram token',
        related='website_id.telegram_token',
        config_parameter='website_improve.telegram_token',
        readonly=False)
    telegram_chat_id = fields.Char(
        string='Telegram chat ID',
        related='website_id.telegram_chat_id',
        config_parameter='website_improve.telegram_chat_id',
        readonly=False)
    google_gtm = fields.Char(
        related='website_id.google_gtm',
        readonly=False,
    )

    @api.depends('website_id')
    def has_google_gtm(self):
        self.has_google_gtm = bool(self.google_gtm)

    def inverse_has_google_gtm(self):
        if not self.has_google_gtm:
            self.google_gtm = False

    has_google_gtm = fields.Boolean(
        string='Google | Add GTM',
        compute=has_google_gtm,
        inverse=inverse_has_google_gtm,
    )