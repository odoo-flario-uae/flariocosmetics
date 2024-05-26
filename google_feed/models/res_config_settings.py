from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    google_feed_enabled = fields.Boolean(
        string="Enable Google Feed",
        related='website_id.google_feed_enabled',
        readonly=False)
    google_feed_location_id = fields.Many2one(
        'stock.location',
        string="Location",
        related='website_id.google_feed_location_id',
        readonly=False)
    google_feed_root_category_id = fields.Many2one(
        'product.public.category',
        string="Root Category",
        related='website_id.google_feed_root_category_id',
        readonly=False)
    google_feed_title = fields.Char(
        string="Feed Title",
        related='website_id.google_feed_title',
        readonly=False)
    google_feed_link = fields.Char(
        string="Feed Link",
        related='website_id.google_feed_link',
        readonly=False)
    google_feed_description = fields.Char(
        string="Feed Description",
        related='website_id.google_feed_description',
        readonly=False)
    google_feed_currency = fields.Char(
        string="Feed Currency",
        related='website_id.google_feed_currency',
        readonly=False)
    google_feed_url = fields.Char(
        string="Feed URL",
        related='website_id.google_feed_url',
        readonly=True)
