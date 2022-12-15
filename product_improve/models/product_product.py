
from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    #### BEGIN Могилевец 23.11.2022  ####
    #pricelist_price = fields.Float('Pricelist Price', compute='_compute_product_pricelist_price', digits='Product Price')

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
                pricelist_rule = pricelist_items[0]
                date = fields.Date.today()
                #product = product.with_context(**product._get_product_price_context())
                qty = 1.0
                uom = product.uom_id
                price = pricelist_rule._compute_price(product, qty, uom, date, currency=product.currency_id)
                product.pricelist_price = price
            else:
                product.pricelist_price = 0.0
    #### END Могилевец 23.11.2022  ####

    #### BEGIN Могилевец 12.12.2022  ####
    weight_brutto = fields.Float(string="Weight brutto", digits='Stock Weight')
    height = fields.Float(string="Height")
    width = fields.Float(string="Width")
    lenght = fields.Float(string="Lenght")

    count_in_box = fields.Integer(string="Count in box")
    weight_box = fields.Float(string="Weight in box")
    count_in_pallet = fields.Integer(string="Box in pallet")
    units_count_in_pallet = fields.Integer(string="Units in pallet")

    @api.onchange('height', 'width', 'lenght')
    def _calc_volume(self):
        for product in self:
            if product.height != 0 and product.width != 0 and product.lenght != 0:
                product.volume = (product.height * product.width * product.lenght) / 1000000000
    #### END Могилевец 12.12.2022  ####