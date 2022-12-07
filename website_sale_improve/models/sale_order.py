from odoo import models, fields, api
from telebot import telebot
import logging
_logger = logging.getLogger(__name__)

TOKEN = '5867719962:AAHz_CUbJS5lwNptB-Ryiz8YD6qYqsKIeBI' 
tb = telebot.TeleBot(TOKEN)
# chat_id = -648259220

class SaleOrder(models.Model):
    _inherit = "sale.order"

    # change create method
    @api.model_create_multi
    def create(self, vals_list):
        __logger.debug(self)
        tb.send_message('-648259220', 'Created order')
        for vals in vals_list:
            _logger.debug(vals)
            # if vals.get('website_id'):
            #     website = self.env['website'].browse(vals['website_id'])
                # if 'company_id' in vals:
                #     company = self.env['res.company'].browse(vals['company_id'])
                #     if website.company_id.id != company.id:
                #         raise ValueError(_("The company of the website you are trying to sale from (%s) is different than the one you want to use (%s)") % (website.company_id.name, company.name))
                # else:
                #     vals['company_id'] = website.company_id.id

        return super().create(vals_list)