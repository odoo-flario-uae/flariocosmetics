# -*- coding: utf-8 -*-
from odoo import http, api,_
from odoo.http import request
import telebot  # Import telegram
TOKEN = '5867719962:AAHz_CUbJS5lwNptB-Ryiz8YD6qYqsKIeBI'
tb = telebot.TeleBot(TOKEN)

class SendCoupons(http.Controller):
    @http.route('/amazon_coupons/', type='http', auth="public", website=True)
    def index(self, **post):
        try:
            if post:
                if post.get('email'):
                    partner_objs = request.env['res.partner'].sudo().search([('email', '=', post.get('email'))], limit=1)
                    partner_id = partner_objs.id if partner_objs else False
                    loyalty_card = request.env['loyalty.card'].sudo().search([('partner_id', '=', partner_id)], limit=1) if partner_id else False

                    if partner_objs and loyalty_card:
                        return request.render("send_coupons.send_coupons_form", {
                            'success': False,
                            'message': 'Customer with current email exist and code was send to your Email.',
                        })
                    else:
                        partner = partner_objs if partner_id else request.env['res.partner'].sudo().create({
                            'name': post.get('name'),
                            'email': post.get('email'),
                            'phone': post.get('phone')
                        })

                        loyalty_program = request.env['loyalty.program'].sudo().search([('for_amazon', '=', True)], limit=1)
                        if not loyalty_program:
                            tb.send_message('-648259220', "Не найдены купоны для клиентов Амазон")
                        if loyalty_program.coupon_count - loyalty_program.order_count <= 5:
                            tb.send_message('-648259220', "Заканчиваются купоны для Амазона")

                        loyalty_card = request.env['loyalty.card'].sudo().search(
                            [('partner_id', '=', False), ('program_id', '=', loyalty_program.id)], limit=1)
                        loyalty_card.partner_id = partner.id
                        template = loyalty_card.env.ref('loyalty.mail_template_loyalty_card')
                        template.email_to = partner.email
                        template.send_mail(loyalty_card.id, force_send=True)

                        return request.render("send_coupons.send_coupons_form", {
                            'success': True,
                            'message': 'Coupon code has been send to your Email'
                        })
            else:
                return request.render("send_coupons.send_coupons_form", {
                    'success': False,
                    'message': '',
                })
        except (RuntimeError, TypeError, NameError) as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return request.render("send_coupons.send_coupons_form", {
                'success': False,
                'message': 'Something went wrong',
            })
            pass