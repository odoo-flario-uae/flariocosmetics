from odoo import models
from odoo.exceptions import ValidationError

class SaleOrderXlsx(models.AbstractModel):
    _name = 'report.custom_sale_order_xlsx.report_sale_order_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = "Sale Order Xlsx report"

    def generate_xlsx_report(self, workbook, data, sale):
        for obj in sale:
            order_number = obj.name
            customer_name = obj.partner_id.display_name
            company_id = obj.partner_id.company_registry if obj.partner_id.company_registry else ""
            street = obj.partner_shipping_id.street if obj.partner_shipping_id.street else ""
            street2 = obj.partner_shipping_id.street2 if obj.partner_shipping_id.street2 else ""
            city = obj.partner_shipping_id.city if obj.partner_shipping_id.city else ""
            zipcode = obj.partner_shipping_id.zip if obj.partner_shipping_id.zip else ""

            address = f'{street} {street2} {city} {zipcode}'

            sheet = workbook.add_worksheet(obj.name)
            sheet.set_column("A:A", 25)
            sheet.set_column("B:B", 25)
            bold = workbook.add_format({'bold': True})
            align_center = workbook.add_format({'align': 'center'})
            sheet.write(0, 0, 'Order Number', bold)
            sheet.write(0, 1, order_number)
            sheet.write(1, 0, 'Customer', bold)
            sheet.write(1, 1, customer_name)
            sheet.write(2, 0, 'Company ID', bold)
            sheet.write(2, 1, company_id)
            sheet.write(3, 0, 'Address', bold)
            sheet.write(3, 1, address)

            sheet.write(5, 0, 'SKU', bold)
            sheet.write(5, 1, 'Count of Box', bold)

            index = 6
            for record in obj.order_line:
                if record.product_id.detailed_type != 'product':
                   continue
                if record.product_id.count_in_box == 0:
                    raise ValidationError(f"Product with SKU {record.product_id.default_code} is not defined count in box")
                sheet.write(index, 0, record.product_id.default_code)
                sheet.write(index, 1, round(record.product_uom_qty / record.product_id.count_in_box), align_center)
                index += 1

