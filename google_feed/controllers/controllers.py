from odoo import http
from odoo.http import request
import re

class GoogleFeedController(http.Controller):

    @http.route('/google_feed.xml', type='http', auth='public', website=True)
    def google_feed(self):
        website = request.env['website'].get_current_website()
        if not website.google_feed_enabled:
            return request.not_found()

        location_id = website.google_feed_location_id.id
        root_category_id = website.google_feed_root_category_id.id
        title = website.google_feed_title
        link = website.google_feed_link
        description = website.google_feed_description
        currency = website.google_feed_currency

        products = self.get_products(location_id, root_category_id)
        feed = self.generate_feed(products, title, link, description, currency)
        clean_feed = self.clean_xml(feed)
        return request.make_response(clean_feed, headers=[('Content-Type', 'application/xml')])

    def get_products(self, location_id, root_category_id):
        ProductTemplate = request.env['product.template']
        products = ProductTemplate.search([('sale_ok', '=', True)]).read([
            'name', 'description', 'image_1920', 'product_variant_ids', 'default_code', 'barcode', 'public_categ_ids'
        ])
        product_list = []
        for product in products:
            product_data = {
                'name': product['name'],
                'description': self.strip_html(product['description']),
                'image_url': self.get_image_url(product['id']),
                'link': self.get_product_url(product['id']),
                'price': self.get_product_price(product['product_variant_ids'][0], request.website.google_feed_currency),
                'availability': self.get_product_stock(product['product_variant_ids'][0], location_id),
                'item_group_id': self.get_category_id(product['public_categ_ids'], root_category_id),
                'product_type': self.get_category_name(product['public_categ_ids']),
                'id': product['default_code'],
                'gtin': product['barcode'],
                'inventory': self.get_product_inventory(product['product_variant_ids'][0], location_id)
            }
            product_list.append(product_data)
        return product_list

    def strip_html(self, text):
        if not text:
            return ''
        # Remove all HTML tags and scripts
        clean_text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL)
        clean_text = re.sub(r'<.*?>', '', clean_text)
        return clean_text

    def get_image_url(self, product_id):
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return f'{base_url}/web/image/product.product/{product_id}/image_1024'

    def get_product_url(self, product_id):
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        product = request.env['product.template'].browse(product_id)
        categories = product.public_categ_ids.mapped('name')
        return f"{base_url}/shop/product/{product_id}?category={'&category='.join(categories)}"

    def get_product_price(self, product_variant_id, currency):
        product = request.env['product.product'].browse(product_variant_id)
        return f"{product.list_price:.2f} {currency}"

    def get_product_stock(self, product_variant_id, location_id):
        stock_quant = request.env['stock.quant'].sudo().search([
            ('product_id', '=', product_variant_id),
            ('location_id', '=', location_id)
        ], limit=1)
        return 'in stock' if stock_quant.quantity > 0 else 'out of stock'

    def get_product_inventory(self, product_variant_id, location_id):
        stock_quant = request.env['stock.quant'].sudo().search([
            ('product_id', '=', product_variant_id),
            ('location_id', '=', location_id)
        ], limit=1)
        return stock_quant.quantity if stock_quant.quantity > 0 else None

    def get_category_id(self, public_categ_ids, root_category_id):
        if not public_categ_ids:
            return root_category_id
        return public_categ_ids[0]

    def get_category_name(self, public_categ_ids):
        if not public_categ_ids:
            return 'Uncategorized'
        category = request.env['product.public.category'].browse(public_categ_ids[0])
        category_chain = [category.name]
        while category.parent_id:
            category_chain.append(category.parent_id.name)
            category = category.parent_id
        category_chain.reverse()
        return 'Home > ' + ' > '.join(category_chain)

    def generate_feed(self, products, title, link, description, currency):
        xml_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
        <rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">
            <channel>
                <title>{title}</title>
                <link>{link}</link>
                <description>{description}</description>
                {self.generate_items(products)}
            </channel>
        </rss>"""
        return xml_content

    def generate_items(self, products):
        item_template = """
            <item>
                <title>{name}</title>
                <link>{link}</link>
                <description>{description}</description>
                <g:price>{price}</g:price>
                <g:image_link>{image_url}</g:image_link>
                <g:availability>{availability}</g:availability>
                <g:item_group_id>{item_group_id}</g:item_group_id>
                <g:product_type>{product_type}</g:product_type>
                <g:id>{id}</g:id>
                <g:gtin>{gtin}</g:gtin>
                {inventory}
                <g:condition>new</g:condition>
            </item>
        """
        items = ''.join([
            item_template.format(
                name=product['name'],
                link=product['link'],
                description=product['description'],
                price=product['price'],
                image_url=product['image_url'],
                availability=product['availability'],
                item_group_id=product['item_group_id'],
                product_type=product['product_type'],
                id=product['id'],
                gtin=product['gtin'],
                inventory=f"<g:inventory>{product['inventory']}</g:inventory>" if product['inventory'] else ""
            )
            for product in products
        ])
        return items

    def clean_xml(self, xml_content):
        # Remove all <script> tags
        clean_content = re.sub(r'<script.*?>.*?</script>', '', xml_content, flags=re.DOTALL)
        return clean_content
