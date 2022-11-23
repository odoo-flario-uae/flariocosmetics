
from odoo import models, fields


class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = "product.product"

    #### BEGIN Могилевец 23.11.2022  ####
    pricelist_price = fields.Float(
        'Pricelist Price', compute='_compute_product_pricelist_price', digits='Product Price')

    def _compute_product_pricelist_price(self):
        for product in self:
            pricelist_items = product.env['product.pricelist.item'].search(
                ['&', '&', '|',
                 '&', ('product_tmpl_id', '=', product.product_tmpl_id.id), ('applied_on', '=', '1_product'),
                 '&', ('product_id', '=', product.id), ('applied_on', '=', '0_product_variant'),
                 '|', ['company_id', '=', self.env.company.id], ['company_id', '=', False],
                 ['currency_id', '=', product.currency_id.id]
                 ]
            )
            if len(pricelist_items) == 1:
                # prices = product.with_context(pricelist=pricelist_items[0].pricelist_id.id)._compute_product_price()
                # product.pricelist_price = prices.get(product.id, 0.0)
                #product.pricelist_price = product.with_context(pricelist=pricelist_items[0].pricelist_id.id).price
                #product.pricelist_price = 222
                pricelist_rule = pricelist_items[0].pricelist_id
                date = fields.Date.today()
                #product = product.with_context(**product._get_product_price_context())
                qty = 1.0
                uom = product.uom_id
                price = pricelist_rule._compute_price(product, qty, uom, date, currency=product.currency_id)
                product.pricelist_price = price
            else:
                product.pricelist_price = 0.0

    #### END Могилевец 23.11.2022  ####

