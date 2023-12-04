from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = "product.template"
    extra_directions = fields.Html("Directions", translate=True, store=True, readonly=False)
    extra_ingredients = fields.Html(string="Ingredients", translate=True, store=True, readonly=False)
    amazon_link = fields.Char(string="Product's amazon link", default="")

    #### BEGIN Могилевец 12.12.2022  ####
    weight_brutto = fields.Float(string="Weight brutto", digits='Stock Weight',
                                 compute='_compute_weight_brutto', inverse='_set_weight_brutto', store=True)
    height = fields.Float(string="Height", compute='_compute_height', inverse='_set_height', store=True)
    width = fields.Float(string="Width", compute='_compute_width', inverse='_set_width', store=True)
    lenght = fields.Float(string="Lenght", compute='_compute_lenght', inverse='_set_lenght', store=True)

    count_in_box = fields.Integer(string="Count in box", compute='_compute_count_in_box', inverse='_set_count_in_box', store=True)
    weight_box = fields.Float(string="Weight in box", compute='_compute_weight_box', inverse='_set_weight_box', store=True)
    count_in_pallet = fields.Integer(string="Box in pallet", compute='_compute_count_in_pallet', inverse='_set_count_in_pallet', store=True)
    units_count_in_pallet = fields.Integer(string="Units in pallet", compute='_compute_units_count_in_pallet', inverse='_set_units_count_in_pallet', store=True)

    @api.depends('product_variant_ids', 'product_variant_ids.weight_brutto')
    def _compute_weight_brutto(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.weight_brutto = template.product_variant_ids.weight_brutto
        for template in (self - unique_variants):
            template.weight_brutto = 0.0
    def _set_weight_brutto(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.weight_brutto = template.weight_brutto

    @api.depends('product_variant_ids', 'product_variant_ids.height')
    def _compute_height(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.height = template.product_variant_ids.height
        for template in (self - unique_variants):
            template.height = 0.0

    def _set_height(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.height = template.height

    @api.depends('product_variant_ids', 'product_variant_ids.width')
    def _compute_width(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.width = template.product_variant_ids.width
        for template in (self - unique_variants):
            template.width = 0.0

    def _set_width(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.width = template.width

    @api.depends('product_variant_ids', 'product_variant_ids.lenght')
    def _compute_lenght(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.lenght = template.product_variant_ids.lenght
        for template in (self - unique_variants):
            template.lenght = 0.0

    def _set_lenght(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.lenght = template.lenght

    @api.onchange('height', 'width', 'lenght')
    def _calc_volume(self):
        for template in self:
            if template.height != 0 and template.width != 0 and template.lenght != 0:
                template.volume = (template.height * template.width * template.lenght) / 1000000000 #mm to m3

    @api.depends('product_variant_ids', 'product_variant_ids.count_in_box')
    def _compute_count_in_box(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.count_in_box = template.product_variant_ids.count_in_box
        for template in (self - unique_variants):
            template.count_in_box = 0.0
    def _set_count_in_box(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.count_in_box = template.count_in_box

    @api.depends('product_variant_ids', 'product_variant_ids.weight_box')
    def _compute_weight_box(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.weight_box = template.product_variant_ids.weight_box
        for template in (self - unique_variants):
            template.weight_box = 0.0
    def _set_weight_box(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.weight_box = template.weight_box

    @api.depends('product_variant_ids', 'product_variant_ids.count_in_pallet')
    def _compute_count_in_pallet(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.count_in_pallet = template.product_variant_ids.count_in_pallet
        for template in (self - unique_variants):
            template.count_in_pallet = 0.0
    def _set_count_in_pallet(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.count_in_pallet = template.count_in_pallet

    @api.depends('product_variant_ids', 'product_variant_ids.units_count_in_pallet')
    def _compute_units_count_in_pallet(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.units_count_in_pallet = template.product_variant_ids.units_count_in_pallet
        for template in (self - unique_variants):
            template.units_count_in_pallet = 0.0
    def _set_units_count_in_pallet(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.units_count_in_pallet = template.units_count_in_pallet
    #### END Могилевец 12.12.2022  ####


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
