# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class FirstDiscount(models.TransientModel):
    _inherit = 'res.config.settings'

    discount_percentage = fields.Float(string='Discount Percentage')
    notify_popup_custom = fields.Boolean(string='Use Default Popup')
    custom_message = fields.Html(string='Custom Popup Message')

    @api.model
    def get_values(self):
        res = super(FirstDiscount, self).get_values()
        res.update(discount_percentage=self.env['ir.config_parameter'].sudo().get_param(
            'bi_website_first_order_discount.discount_percentage')),
        res.update(notify_popup_custom=self.env['ir.config_parameter'].sudo().get_param(
            'bi_website_first_order_discount.notify_popup_custom')),
        res.update(custom_message=self.env['ir.config_parameter'].sudo().get_param(
            'bi_website_first_order_discount.custom_message')),
        return res

    def set_values(self):
        super(FirstDiscount, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('bi_website_first_order_discount.discount_percentage',
                                                         self.discount_percentage)
        self.env['ir.config_parameter'].sudo().set_param('bi_website_first_order_discount.notify_popup_custom',
                                                         self.notify_popup_custom)
        self.env['ir.config_parameter'].sudo().set_param('bi_website_first_order_discount.custom_message',
                                                         self.custom_message)
