from odoo import models
from odoo.exceptions import ValidationError

class SaleOrderXlsx(models.AbstractModel):
    _name = 'report.custom_sale_order_xlsx.report_sale_order_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = "Sale Order Xlsx report"

    def generate_xlsx_report(self, workbook, data, sale):
        for obj in sale:
            order_number = obj.name
            sales_channel = obj.x_studio_sales_channel
            customer_name = obj.partner_id.display_name
            individual_name = obj.partner_shipping_id.name if obj.partner_shipping_id.name else customer_name
            street = obj.partner_shipping_id.street if obj.partner_shipping_id.street else ""
            street2 = obj.partner_shipping_id.street2 if obj.partner_shipping_id.street2 else ""
            city = obj.partner_shipping_id.city if obj.partner_shipping_id.city else ""
            zipcode = obj.partner_shipping_id.zip if obj.partner_shipping_id.zip else ""
            country_code = obj.partner_shipping_id.country_id.code if obj.partner_shipping_id.country_id else ""
            phone = obj.partner_shipping_id.phone if obj.partner_shipping_id.phone else ""
            email = obj.partner_shipping_id.email if obj.partner_shipping_id.email else ""

            # Sheet 1: Address Sheet
            address_sheet_name = f'{order_number} - Address'
            address_sheet = workbook.add_worksheet(address_sheet_name)
            address_sheet.set_column("A:A", 25)
            address_sheet.set_column("B:B", 25)
            address_sheet.set_column("C:C", 25)
            address_sheet.set_column("D:D", 25)
            address_sheet.set_column("E:E", 25)
            address_sheet.set_column("F:F", 25)
            address_sheet.set_column("G:G", 25)
            address_sheet.set_column("H:H", 25)
            address_sheet.set_column("I:I", 25)
            address_sheet.set_column("J:J", 25)
            address_sheet.set_column("K:K", 25)
            address_sheet.set_column("L:L", 25)
            address_sheet.set_column("M:M", 25)
            address_sheet.set_column("N:N", 25)
            bold = workbook.add_format({'bold': True})

            # Headers
            address_sheet.write(0, 0, 'CisloOdesilatele', bold)
            address_sheet.write(0, 1, 'CompanyName', bold)
            address_sheet.write(0, 2, 'Attention_Contact', bold)
            address_sheet.write(0, 3, 'Address1_Street', bold)
            address_sheet.write(0, 4, 'Address2', bold)
            address_sheet.write(0, 5, 'Address3', bold)
            address_sheet.write(0, 6, 'City', bold)
            address_sheet.write(0, 7, 'ZIP', bold)
            address_sheet.write(0, 8, 'Country_constant', bold)
            address_sheet.write(0, 9, 'Phone', bold)
            address_sheet.write(0, 10, 'Email', bold)
            address_sheet.write(0, 11, 'DescriptionOfGoods', bold)
            address_sheet.write(0, 12, 'Reference', bold)
            address_sheet.write(0, 13, 'Sales Channel', bold)

            # Data
            address_sheet.write(1, 0, 'R69100')
            address_sheet.write(1, 1, customer_name)
            address_sheet.write(1, 2, individual_name)
            address_sheet.write(1, 3, f'{street} {street2}')
            address_sheet.write(1, 4, '')
            address_sheet.write(1, 5, '')
            address_sheet.write(1, 6, city)
            address_sheet.write(1, 7, zipcode)
            address_sheet.write(1, 8, country_code)
            address_sheet.write(1, 9, phone)
            address_sheet.write(1, 10, email)
            address_sheet.write(1, 11, 'Cosmetics')
            address_sheet.write(1, 12, order_number)
            address_sheet.write(1, 13, sales_channel)


            # Sheet 2: SKU Sheet
            sku_sheet_name = f'{order_number} - SKU'
            sku_sheet = workbook.add_worksheet(sku_sheet_name)
            sku_sheet.set_column("A:A", 25)
            sku_sheet.set_column("B:B", 25)
            sku_sheet.set_column("C:C", 25)
            bold = workbook.add_format({'bold': True})
            align_center = workbook.add_format({'align': 'center'})
            sku_sheet.write(0, 0, 'SKU', bold)

            index = 1

            sku_sheet.write(0, 1, 'Number of pcs', bold)
            if sales_channel == 'Wholesale':
                sku_sheet.write(0, 2, 'Number of cartons', bold)
            for record in obj.order_line:
                if record.product_id.detailed_type != 'product':
                    continue
                sku_sheet.write(index, 0, record.product_id.default_code)
                sku_sheet.write(index, 1, record.product_uom_qty, align_center)
                if sales_channel == 'Wholesale':
                    sku_sheet.write(index, 2, round(record.product_uom_qty / record.product_id.count_in_box), align_center)
                index += 1
