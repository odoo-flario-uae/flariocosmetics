from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    website_fast_puchasing = fields.Boolean(string="Fast purchase", related='website_id.fast_puchasing', readonly=False)