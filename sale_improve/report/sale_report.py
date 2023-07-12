# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'

    ### Задача № 230001 ###
    ### Могилевец 17.01.2023 ###
    cost_price = fields.Float('Cost Price', readonly=True)

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['cost_price'] = f"""CASE WHEN l.product_id IS NOT NULL THEN SUM(l.purchase_price
                * {self._case_value_or_one('s.currency_rate')}
                * {self._case_value_or_one('currency_table.rate')}
                * l.product_uom_qty) ELSE 0
            END """
        return res
