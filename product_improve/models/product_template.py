from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = "product.template"
    directions = fields.Char(string="Directions")
    ingredients = fields.Char(string="Ingredients")

    #### BEGIN Могилевец 23.11.2022  ####
    #pricelist_price = fields.Float('Pricelist Price', compute='_compute_template_pricelist_price', digits='Product Price')

    def _compute_template_pricelist_price(self):
        for template in self:
            pricelist_items = template.env['product.pricelist.item'].search(
                ["&", "&",
                 "|", ["product_tmpl_id", "=", template.id], ["product_id", "in", template.product_variant_ids.ids],
                 "|", ["company_id", "=", self.env.company.id], ["company_id", "=", False],
                 ["currency_id", "=", template.currency_id.id]
                 ]
            )
            if len(pricelist_items) == 1:
                # prices = template.with_context(
                #     pricelist=pricelist_items[0].pricelist_id.id)._compute_template_price_no_inverse()()
                # template.pricelist_price = prices.get(template.id, 0.0)
                # template.pricelist_price = template.with_context(pricelist=pricelist_items[0].pricelist_id.id).price
                pricelist_rule = pricelist_items[0]
                date = fields.Date.today()
                # template = template.with_context(**template._get_product_price_context())
                qty = 1.0
                uom = template.uom_id
                price = pricelist_rule._compute_price(template, qty, uom, date, currency=template.currency_id)
                template.pricelist_price = price
            else:
                template.pricelist_price = 0.0

    # Изменение вычисления поля 'template.currency_id'
    @api.depends('company_id')
    def _compute_currency_id(self):
        main_company = self.env['res.company']._get_main_company()
        for template in self:
            # template.currency_id = template.company_id.sudo().currency_id.id or main_company.currency_id.id
            template.currency_id = template.company_id.sudo().currency_id.id or self.env.company.currency_id.id or main_company.currency_id.id
    #### END Могилевец 23.11.2022  ####
