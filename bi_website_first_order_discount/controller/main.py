# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class DiscountPopup(WebsiteSale):

    @http.route(['/shop/user_orders'], type='json', auth="public", methods=['POST'], website=True)
    def user_orders(self, **kw):
        curr_user_name = request.env.user.name
        curr_user_sale_order = request.env['sale.order'].sudo().search([('partner_id.name', '=', curr_user_name)],
                                                                       limit=1).name
        return curr_user_sale_order

    @http.route(['/shop/disc_popup'], type='json', auth="public", methods=['POST'], website=True)
    def disc_popupp(self, **kw):
        discount = request.env['ir.config_parameter'].sudo().get_param(
            'bi_website_first_order_discount.discount_percentage')
        notify_popup_custom = request.env['ir.config_parameter'].sudo().get_param(
            'bi_website_first_order_discount.notify_popup_custom')
        discount_msg = request.env['ir.config_parameter'].sudo().get_param(
            'bi_website_first_order_discount.custom_message')
        curr_user_name = request.env.user.name
        curr_user_sale_order = request.env['sale.order'].sudo().search([('partner_id.name', '=', curr_user_name)],
                                                                       limit=1).name

        if not curr_user_sale_order:
            values = {
                'discount_msg': discount_msg,
                'notify_popup_custom': notify_popup_custom,
                'discount': discount,
            }
            return request.env['ir.ui.view'].sudo()._render_template("bi_website_first_order_discount.disc_popup", values)

    @http.route(['/shop/cart'], type='http', auth="public", website=True)
    def cart(self, **post):
        '''Unlink product from order in cart page'''
        res = super(DiscountPopup, self).cart()
        get_product_id = request.env.ref('bi_website_first_order_discount.first_discount_product').id
        for line in request.website.sale_get_order().order_line:
            if line.product_id.id == get_product_id:
                line.unlink()
        return res

    @http.route(['/shop/payment'], type='http', auth="public", website=True)
    def shop_payment(self, **post):
        '''Add Discount product line with calculation in order'''
        res = super(DiscountPopup, self).shop_payment()

        # Get discount product
        get_product_id = request.env.ref('bi_website_first_order_discount.first_discount_product').id
        get_product = request.env['product.product'].sudo().browse(get_product_id)
        get_cart_products = request.website.sale_get_order()
        total_untaxed_amount = get_cart_products.amount_total
        get_product_discount = request.env['ir.config_parameter'].sudo().get_param(
            'bi_website_first_order_discount.discount_percentage')
        compute_discount = (total_untaxed_amount * float(get_product_discount) / 100)
        order_line_obj = request.env['sale.order.line'].sudo()
        discount_product_status = order_line_obj.sudo().search(
            [('product_id.name', '=', get_product.name), ('order_id.partner_id', '=', request.env.user.partner_id.id)])
        if not discount_product_status:
            order_line_obj.sudo().create({
                'product_id': get_product.id,
                'name': get_product.name,
                'price_unit': -compute_discount,
                'order_id': get_cart_products.id,
                'tax_id': False,
                'product_uom': get_product.uom_id.id,
            })
        return res
