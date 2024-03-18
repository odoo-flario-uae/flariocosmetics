import base64
import csv
import io
import locale

from odoo import _, fields, models
from odoo.exceptions import ValidationError, UserError
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

class AccountMoveImportCsvWizard(models.TransientModel):
    _name = 'account.move.import.csv.wizard'
    _description = 'Import CSV'

    file = fields.Binary(string="File", required=True)
    message = fields.Text('Information')

    def action_import_csv(self):
        if not self.file:
            raise ValidationError(_("Please Upload CSV File to Import!"))

        if self._context.get('active_model') != 'account.move' or not self._context.get('active_ids'):
            raise ValidationError(_('This can only be used on account.move records'))

        move = self.env['account.move'].browse(self._context.get('active_ids'))
        if move.state != 'draft':
            raise UserError(_('You cannot import a move not in the draft state.\nPlease reset to draft it first.'))

        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        # read csv
        csv_data = base64.b64decode(self.file)
        data_file = io.StringIO(csv_data.decode("utf-8"))
        data_file.seek(0)
        
        # Пропускаем первую строку с заголовками
        header_line = next(data_file)
    
        # Чтение второй строки для определения применяемого налога
        second_line = next(data_file).lower()  # Приводим строку к нижнему регистру для упрощения поиска
        vat_tax = self.env['account.tax'].search([('amount', '=', 5), ('type_tax_use', '=', 'sale')], limit=1)
        
        # Проверяем наличие валюты и устанавливаем соответствующий налог
        apply_tax = True
        if 'gbp' in second_line or 'usd' in second_line:
            apply_tax = False
            
        data_file.seek(0)
        start_from_line = 0
        for index, line in enumerate(data_file):
            if "sku" in line.lower():
                start_from_line = index
                break
    
        # Если не нашли "sku", выводим сообщение об ошибке
        if start_from_line == 0:
            raise UserError(_("The CSV file does not contain a 'sku' header."))
            
        # Сбрасываем указатель файла и пропускаем строки до найденной с "sku"
        data_file.seek(0)
        for item in range(start_from_line):
            next(data_file, None)

        csv_reader = csv.DictReader(data_file, delimiter=',')
        file_reader = []
        file_reader.extend(csv_reader)

        message_parts = []
        invoice_line_ids_commands =[]
        n = 0
        critical_error = False

        for line in file_reader:
            invoice_line_cmd = {'sequence': n}
            n += 1

            if line['type'] != 'Order':
                continue
            try:
                origin = line['order id']
                default_code = line['sku']
                price_unit = float(line['product sales']) / float(line['quantity'])
                # total = float(line['total'])
                # line_comission = price_unit - total
                quantity = float(line['quantity'])
            except Exception as e:
                message_parts.append(_("<b>Line #%d</b>. "
                                       "Failed to read: %s", n, e.args[0]))
                message_parts.append(_("<b>Import stopped!</b>"))
                critical_error = True
                break
                #continue

            product_id = self.env['product.product'].search([('default_code', '=', default_code)])
            if not product_id:
                message_parts.append(_("<b>Line #%d</b>. "
                                       "Not found product with sku %s", n, default_code))
                message_parts.append(_("<b>Import stopped!</b>"))
                critical_error = True
                break
                #continue

            invoice_line_cmd.update({
                'price_unit': price_unit, 
                'quantity': quantity, 
                'product_id': product_id.id, 
                'tax_ids': [(6, 0, [vat_tax.id])] if apply_tax else []
            })

            sale_id = self.env['sale.order'].search([('origin', 'ilike', origin)])
            if sale_id:
                sale_line_ids = sale_id.order_line.filtered(lambda sale_line:
                                                           sale_line.product_id.id == product_id.id
                                                           and sale_line.product_uom_qty == quantity)
                if sale_line_ids:
                    invoice_line_cmd['sale_line_ids'] = sale_line_ids[:1]
                    #     sale_line_ids: [(<Command.LINK: 4>, 2, 0)]
                else:
                    message_parts.append(_("<b>Line #%d</b>. "
                                           "Not found product with sku %s in Sale order %s", n, default_code, sale_id.name))
            else:
                message_parts.append(_("<b>Line #%d</b>. "
                                       "Not found Sale order with Source Document %s", n, origin))

            invoice_line_ids_commands.append((0, 0, invoice_line_cmd))

        if not critical_error:
            move.invoice_line_ids.unlink()
            move.write({'line_ids': invoice_line_ids_commands})

        self.message = 'Done<br /><br />'
        self.message += '<br />'.join(message_parts)

        return self.open_dialog(title='Import result')



    def open_dialog(self, title):
        """ Open dialog box procedure
        """
        return {
            'type': 'ir.actions.act_window',
            'name': title,
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'res_model': 'account.move.import.csv.wizard',
            'views': [(False, 'form')],
            'domain': [],
            'context': self.env.context,
            'target': 'new',
            'flags': {
                'form': {'action_buttons': False},
            }
        }
