import logging
from odoo import http
from odoo.http import request
import re
from xml.sax.saxutils import escape

_logger = logging.getLogger(__name__)

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

        _logger.info(f"Generating Google feed for website: {website.name}")
        _logger.info(f"Location ID: {location_id}, Root Category ID: {root_category_id}")

        products = self.get_products(location_id, root_category_id)
        feed = self.generate_feed(products, title, link, description, currency)
        return request.make_response(self.remove_scripts(feed), headers=[('Content-Type', 'application/xml')])

    def get_products(self, location_id, root_category_id):
        ProductTemplate = request.env['product.template']
        products = ProductTemplate.search([
            ('website_published', '=', True),
            ('sale_ok', '=', True)
        ]).read([
            'name', 'description_sale', 'image_1920', 'product_variant_ids', 'default_code', 'public_categ_ids', 'barcode'
        ])
        product_list = []
        for product in products:
            item_group_id, product_type, category_link = self.get_category_info(product['public_categ_ids'], root_category_id)
            product_data = {
                'name': product['name'],
                'description': self.strip_html(product['description_sale']),
                'image_url': self.get_image_url(product['id']),
                'link': self.get_product_url(product['id'], category_link),
                'price': self.get_product_price(product['product_variant_ids'][0]),
                'availability': self.get_product_stock(product['product_variant_ids'][0], location_id),
                'id': product['default_code'] if product['default_code'] else product['id'],
                'gtin': product['barcode'],
                'item_group_id': item_group_id,
                'product_type': product_type,
                'location_id': location_id  # Add location_id here
            }
            product_list.append(product_data)
        return product_list

    def strip_html(self, text):
        if not text:
            return ''
        return re.sub(r'<.*?>', '', text)

    def clean_title(self, title):
        return title.replace('&', 'and')

    def get_image_url(self, product_id):
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return f'{base_url}/web/image/product.product/{product_id}/image_1024'

    def get_product_url(self, product_id, category_link):
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if category_link:
            return f"{base_url}/shop/product/{product_id}?category={category_link}"
        else:
            return f"{base_url}/shop/product/{product_id}"

    def get_product_price(self, product_variant_id):
        product = request.env['product.product'].browse(product_variant_id)
        return f"{product.list_price:.2f}"

    def get_product_stock(self, product_variant_id, location_id):
        stock_quant = request.env['stock.quant'].sudo().search([
            ('product_id', '=', product_variant_id),
            ('location_id', '=', location_id)
        ], limit=1)
        return 'in stock' if stock_quant.quantity > 0 else 'out of stock'

    def get_category_info(self, public_categ_ids, root_category_id):
        categories = request.env['product.public.category'].search([('id', 'child_of', root_category_id)], order='sequence asc')
        for category in categories:
            if category.id in public_categ_ids:
                child_category = self.get_child_category(category)
                parent_path = self.get_category_path(child_category)
                return child_category.id, parent_path, child_category.id
        return None, None, None

    def get_child_category(self, category):
        child_categories = category.child_id
        if child_categories:
            return child_categories[0]
        return category

    def get_category_path(self, category):
        path = [category.name]
        while category.parent_id:
            category = category.parent_id
            path.append(category.name)
        return ' > '.join(reversed(path))

    def remove_scripts(self, xml_content):
        return re.sub(r'<script.*?</script>', '', xml_content, flags=re.DOTALL)

    def generate_feed(self, products, title, link, description, currency):
        xml_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
        <rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">
            <channel>
                <title>{title}</title>
                <link>{link}</link>
                <description>{description}</description>
                {self.generate_items(products, currency)}
            </channel>
        </rss>"""
        return xml_content

    def generate_items(self, products, currency):
        item_template = """
            <item>
                <title>{name}</title>
                <link>{link}</link>
                <description>{description}</description>
                <g:price>{price} {currency}</g:price>
                <g:image_link>{image_url}</g:image_link>
                <g:availability>{availability}</g:availability>
                <g:id>{id}</g:id>
                {gtin_tag}
                {inventory_tag}
                <g:condition>new</g:condition>
                {item_group_id_tag}
                {product_type_tag}
            </item>
        """
        items = ''
        for product in products:
            gtin_tag = f"<g:gtin>{product['gtin']}</g:gtin>" if product['gtin'] else ''
            inventory_tag = f"<g:inventory>{self.get_inventory(product)}</g:inventory>" if product['availability'] == 'in stock' else ''
            item_group_id_tag = f"<g:item_group_id>{product['item_group_id']}</g:item_group_id>" if product['item_group_id'] else ''
            product_type_tag = f"<g:product_type>{product['product_type']}</g:product_type>" if product['product_type'] else ''
            items += item_template.format(
                name=escape(product['name']),
                link=product['link'],
                description=escape(product['description']),
                price=product['price'],
                image_url=product['image_url'],
                availability=product['availability'],
                id=product['id'],
                gtin_tag=gtin_tag,
                inventory_tag=inventory_tag,
                item_group_id_tag=item_group_id_tag,
                product_type_tag=product_type_tag,
                currency=currency
            )
        return items

    def get_inventory(self, product):
        stock_quant = request.env['stock.quant'].sudo().search([
            ('product_id', '=', product['id']),
            ('location_id', '=', product['location_id'])
        ], limit=1)
        return stock_quant.quantity if stock_quant else 0
