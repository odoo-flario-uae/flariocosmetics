# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
import csv
import io
from collections import defaultdict
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import _, fields, models, api
from odoo.exceptions import ValidationError, UserError
from odoo.tools import formatLang, format_date
import locale



class AccountMove(models.Model):
    _inherit = 'account.move'

    # commission = fields.Monetary(string='Reseller Commission', compute='_compute_commission')

    # @api.depends('invoice_line_ids.commission')
    # def _compute_commission(self):
    #     self.commission = 0
    #     for move in self:
    #         move.commission = sum([invoice_line.commission for invoice_line in move.mapped('invoice_line_ids')])

    #commission_po_line_id = fields.Many2one('purchase.order.line', 'Referrer Purchase Order line', copy=False)

    # def _get_commission_purchase_order_domain(self):
    #     self.ensure_one()
    #
    #     domain = [
    #         ('partner_id', '=', self.partner_id.id),
    #         ('company_id', '=', self.company_id.id),
    #         ('state', '=', 'draft'),
    #         ('currency_id', '=', self.currency_id.id),
    #         ('purchase_type', '=', 'commission'),
    #     ]
    #
    #     return domain
    #
    # def _get_commission_purchase_order(self):
    #     self.ensure_one()
    #     purchase = self.env['purchase.order'].sudo().search(self._get_commission_purchase_order_domain(), limit=1)
    #
    #     if not purchase:
    #         sales_rep = self._get_sales_representative()
    #         purchase = self.env['purchase.order'].with_context(mail_create_nosubscribe=True).sudo().create({
    #             'partner_id': self.partner_id.id,
    #             'currency_id': self.currency_id.id,
    #             'company_id': self.company_id.id,
    #             'fiscal_position_id': self.env['account.fiscal.position'].with_company(self.company_id)._get_fiscal_position(self.partner_id).id,
    #             'payment_term_id': self.partner_id.with_company(self.company_id).property_supplier_payment_term_id.id,
    #             'user_id': sales_rep and sales_rep.id or False,
    #             'dest_address_id': self.partner_id.id,
    #             'origin': self.name,
    #             'purchase_type': 'commission',
    #         })
    #
    #     return purchase
    #
    # def _make_commission(self):
    #     for move in self.filtered(lambda m: m.move_type in ['out_invoice', 'in_invoice', 'out_refund']):
    #         if move.move_type in ['out_invoice', 'in_invoice']:
    #             sign = 1
    #             # if move.commission_po_line_id:
    #             #     continue
    #         else:
    #             sign = -1
    #             # if not move.commission_po_line_id:
    #             #     continue
    #
    #         if not self.commission:
    #             continue
    #
    #         # product = self.env.ref('partner_commission_flario.product_commission')
    #
    #         # build description lines
    #         #desc = f"{_('Commission on %s') % (move.name)}, {move.partner_id.name}, {formatLang(self.env, move.amount_untaxed, currency_obj=move.currency_id)}"
    #
    #         #purchase = move._get_commission_purchase_order()
    #         # line = self.env['purchase.order.line'].sudo().create({
    #         #     'name': desc,
    #         #     'product_id': product.id,
    #         #     'product_qty': 1,
    #         #     'price_unit': self.commission * sign,
    #         #     'product_uom': product.uom_id.id,
    #         #     'date_planned': fields.Datetime.now(),
    #         #     #'order_id': purchase.id,
    #         #     'qty_received': 1,
    #         # })
    #         # purchase.button_confirm()
    #
    #         # if move.move_type in ['out_invoice', 'in_invoice']:
    #         #     # link the purchase order line to the invoice
    #         #     #move.commission_po_line_id = line
    #         #     msg_body = 'New commission. Invoice: %s. Amount: %s.' % (
    #         #         move._get_html_link(),
    #         #         formatLang(self.env, self.commission, currency_obj=move.currency_id),
    #         #     )
    #         # else:
    #         #     msg_body = 'Commission refunded. Invoice: %s. Amount: %s.' % (
    #         #         move._get_html_link(),
    #         #         formatLang(self.env, self.commission, currency_obj=move.currency_id))
    #         # purchase.message_post(body=msg_body)

    # def _reverse_moves(self, default_values_list=None, cancel=False):
    #     if not default_values_list:
    #         default_values_list = [{} for move in self]
    #     for move, default_values in zip(self, default_values_list):
    #         default_values.update({
    #             #'referrer_id': move.referrer_id.id,
    #             'commission_po_line_id': move.commission_po_line_id.id,
    #         })
    #     return super(AccountMove, self)._reverse_moves(default_values_list=default_values_list, cancel=cancel)

    # def action_post(self):
    #     res = super(AccountMove, self).action_post()
    #     self._make_commission()
    #     return res

    # def _invoice_paid_hook(self):
    #     res = super()._invoice_paid_hook()
    #     self.filtered(lambda move: move.move_type == 'out_refund')._make_commission()
    #     self.filtered(lambda move: move.move_type == 'out_invoice')._make_commission()
    #     return res

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # commission = fields.Monetary(string='Reseller Commission')

    # def _get_commission(self):
    #     return self.commission

    # def _get_commission_rule(self):
    #     self.ensure_one()
    #     template = self.subscription_id.sale_order_template_id
    #     # check whether the product is part of the subscription template
    #     template_products = template.sale_order_template_line_ids.product_id.mapped('product_tmpl_id')
    #     template_id = template.id if template and self.product_id.product_tmpl_id in template_products.ids else None
    #     sub_pricelist = self.subscription_id.pricelist_id
    #     pricelist_id =  sub_pricelist and sub_pricelist.id or self.sale_line_ids.mapped('order_id.pricelist_id')[:1].id
    #
    #     # a specific commission plan can be set on the subscription, taking predence over the referrer's commission plan
    #     plan = self.move_id.referrer_id.commission_plan_id
    #     if self.subscription_id:
    #         plan = self.subscription_id.commission_plan_id
    #
    #     if not plan:
    #         return self.env['commission.rule']
    #
    #     return plan._match_rules(self.product_id, template_id, pricelist_id)
