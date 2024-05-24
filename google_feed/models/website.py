from odoo import models, fields

class Website(models.Model):
    _inherit = "website"

    google_feed_enabled = fields.Boolean(string="Enable Google Feed")
    google_feed_location_id = fields.Many2one('stock.location', string="Location")
    google_feed_root_category_id = fields.Many2one('product.public.category', string="Root Category")
    google_feed_title = fields.Char(string="Feed Title")
    google_feed_link = fields.Char(string="Feed Link")
    google_feed_description = fields.Char(string="Feed Description")
    google_feed_currency = fields.Char(string="Feed Currency")
    google_feed_url = fields.Char(string="Feed URL", compute="_compute_google_feed_url")

    def _compute_google_feed_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for website in self:
            website.google_feed_url = f"{base_url}/google_feed.xml"
