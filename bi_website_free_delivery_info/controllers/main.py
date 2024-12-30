# -*- coding: utf-8 -*-
from odoo import http
import datetime
from odoo.addons.website_sale_delivery.controllers.main import WebsiteSaleDelivery
from odoo.http import request
from odoo import api, fields, models, _
from datetime import datetime, date

class WebsiteSaleDelivery(WebsiteSaleDelivery):

    def _update_website_sale_delivery_return(self, order, **post):
        res = super(WebsiteSaleDelivery, self)._update_website_sale_delivery_return(order, **post)
        order = request.website.sale_get_order(force_create=True)

        currency = request.website.sudo().company_id.sudo().currency_id._convert(order.carrier_id.amount,request.website.get_current_pricelist().currency_id, request.website.company_id.sudo(),fields.Date.today())
        if currency >=order.amount_total:
            buy_more_amount = currency - order.amount_total
            res['buy_more_amount'] = buy_more_amount
        return res

    @http.route(['/shiiping_method/check'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def shipping_method_check(self, delivery_id):
        shipping_method_type = request.env["delivery.carrier"].search([('id','=',delivery_id),('free_over','=',True),('delivery_type','=','fixed')])
        free_delivery = False
        if shipping_method_type:
            price = shipping_method_type.amount
            currency = request.website.sudo().company_id.sudo().currency_id._convert(shipping_method_type.amount, request.website.get_current_pricelist().currency_id, request.website.company_id.sudo(),fields.Date.today())
            currency_value = {'currency': currency,'free_delivery': True}
            return currency_value
        else:
            return False
        return 0