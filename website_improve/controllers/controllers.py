# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
import telebot  # Import telegram

TOKEN = '5867719962:AAHz_CUbJS5lwNptB-Ryiz8YD6qYqsKIeBI'
tb = telebot.TeleBot(TOKEN)


class WebsiteInherit(WebsiteSale):
    @staticmethod
    def validateParams(p1, p2):
        return p1 if p1 != '' else p2

    def msgToTg(self, order, subject, name="", phone="", email=""):
        method_com_arr = {
            "wa": "WhatsApp",
            "phone": "phone",
            "email": "email"
        }
        # method_com = method_com_arr[request.session.get('communication_method', 'wa')] if method_com_arr[request.session.get('communication_method', 'wa')] else "Не указан"
        tx = order.get_portal_last_transaction()
        amout_total = order.amount_total
        order_name = order.display_name
        partner_name = self.validateParams(name, order.partner_id.name)
        partner_phone = self.validateParams(phone, order.partner_id.phone)
        partner_email = self.validateParams(email, order.partner_id.email)
        provide_name = tx.provider_id.name if tx.provider_id.name else "Не указан"

        tgText = subject + ": " + order_name + " на сумму: " + str(amout_total) + "\n"
        tgText = tgText + "Заказчик: " + partner_name + "\n"
        # tgText = tgText + "Метод связи: " + method_com + "\n"
        tgText = tgText + "Телефон: " + str(partner_phone) + "\n"
        tgText = tgText + "Email: " + str(partner_email) + "\n"
        tgText = tgText + "Метод оплаты: " + provide_name + "\n"
        tgText = tgText + "\n Товары: " + "\n"

        if (order.order_line):
            for idx, line in enumerate(order.order_line):
                product = line.product_id
                product_name = product.name
                product_code = ''
                if (type(product.code) == bool):
                    product_code = "не указан артикул"
                else:
                    product_code = product.code

                tgText = tgText + str(idx + 1) + " " + str(product_name) + "(" + str(product_code) + ")" + "\n"
        return tgText

    @http.route(['/fastbuy/form/submit'], type='http', auth="public", website=True)
    def one_click_buy(self, **post):
        sale_order_id = request.session.data.get('sale_order_id')
        order = request.env['sale.order'].sudo().browse(sale_order_id)
        tgMessage = self.msgToTg(order, "Быстрый заказ", post.get("name"), post.get("phone"), post.get("email"))
        tb.send_message('-648259220', tgMessage)
        order.with_context().action_confirm()
        request.website.sale_reset()
        return request.redirect('/thank-you')

    @http.route(['/shop/confirmation'], type='http', auth="public", website=True, sitemap=False)
    def shop_payment_confirmation(self, **post):
        res = super(WebsiteInherit, self).shop_payment_confirmation(**post)
        order = res.qcontext.get('order')

        partner_name = order.partner_id.name
        partner_phone = order.partner_id.phone
        partner_email = order.partner_id.email
        message = self.msgToTg(order, "Order (auto)", partner_name, partner_phone, partner_email)
        tb.send_message('-648259220', message)

        return res
