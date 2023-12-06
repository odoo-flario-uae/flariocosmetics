import base64
import csv
import io
import locale

from odoo import _, fields, models
from odoo.exceptions import ValidationError, UserError
from datetime import datetime


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

        orders = []
        other_transactions = []

        reader = csv.DictReader(data_file, delimiter='\t')
        next(reader, None)

        for row in reader:
            order_id = row['order-id']

            # Обработка для 'other-transaction'
            if row['transaction-type'] == 'other-transaction':
                other_transactions.append({'type': row['amount-description'], 'amount': row['amount']})
                continue  # Переход к следующей записи

            # Поиск или создание новой записи заказа
            existing_order = next((item for item in orders if item['order_id'] == order_id), None)
            if not existing_order:
                existing_order = {'order_id': order_id, 'type': row['transaction-type'], 'products': {}}
                orders.append(existing_order)

            # Добавление информации о продукте
            product_info = existing_order['products'].get(row['sku'], {'price': 0, 'quantity': 0, 'fees': 0})
            if row['amount-description'] == 'Principal':
                product_info['price'] += float(row['amount'])
            else:
                product_info['fees'] = round(product_info['fees'] + float(row['amount']), 2)

            # Для типа транзакции 'Refund' устанавливаем количество равным 0
            if row['transaction-type'] == 'Refund':
                product_info['quantity'] = 0
            else:
                product_info['quantity'] = float(row['quantity-purchased'])

            existing_order['products'][row['sku']] = product_info

        message_parts = []
        invoice_line_ids_commands =[]
        n = 0
        critical_error = False
        all_fees = 0

        for line in orders:
            try:
                if line['type'] != 'Order':
                    for sku, product_info in line['products'].items():
                        all_fees += product_info['fees']
                if line['type'] == 'Order':
                    for sku, product_info in line['products'].items():
                        all_fees += product_info['fees']
                        invoice_line_cmd = {'sequence': n}
                        n += 1
                        product_id = self.sudo().env['product.product'].search([('default_code', '=', sku)],
                                                                               limit=1)
                        if not product_id:
                            message_parts.append(_("Not found product with sku %s", n, sku))
                            message_parts.append(_("<b>Import stopped!</b>"))
                            critical_error = True
                            break
                        invoice_line_cmd.update({'price_unit': product_info['price'], 'quantity': product_info['quantity'], 'product_id': product_id})
                        sale_id = self.env['sale.order'].search([('origin', 'ilike', line['order_id'])])
                        if sale_id:
                            sale_line_ids = sale_id.order_line.filtered(lambda sale_line:
                                                                        sale_line.product_id.id == product_id.id
                                                                        and sale_line.product_uom_qty == product_info['quantity'])
                            if sale_line_ids:
                                invoice_line_cmd['sale_line_ids'] = sale_line_ids[:1]
                                #     sale_line_ids: [(<Command.LINK: 4>, 2, 0)]
                            else:
                                message_parts.append(_("<b>Line #%d</b>. "
                                                       "Not found product with sku %s in Sale order %s", n,
                                                       sku, sale_id.name))
                        else:
                            message_parts.append(_("<b>Line #%d</b>. "
                                                   "Not found Sale order with Source Document %s", n, line['order_id']))

                        invoice_line_ids_commands.append((0, 0, invoice_line_cmd))


                ecommerce_fees = '400067'
                company_id = self.env.company or move.company_id
                fba_fees_account_id = self.env['account.account'].search(
                    [('code', '=', ecommerce_fees), ('company_id', '=', company_id.id)], limit=1)

                if fba_fees_account_id:
                    invoice_line_fba_fees = {
                        'name': _('Ecommerce fees'),
                        'account_id': fba_fees_account_id.id,
                        'price_unit': all_fees,
                        'tax_ids': [],
                        'tax_line_id': False,
                    }
                    invoice_line_ids_commands.append((0, 0, invoice_line_fba_fees))
                else:
                    message_parts.append(
                        _("%s - not found account with code '%s'", company_id.name, ecommerce_fees))
                    message_parts.append(_("<b>Import stopped!</b>"))
                    critical_error = True
            except Exception as e:
                message_parts.append(_("Failed to check file: %s", line['type'], e.args[0]))
                message_parts.append(_("<b>Import stopped!</b>"))
                critical_error = True
                break
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
