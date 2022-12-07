from odoo import models, fields
from telebot import telebot
import logging
_logger = logging.getLogger(__name__)

# TOKEN = '1998721499:AAEANtp7-E7JwRk0D3esngYflc_n-tu1qWk' # Ponemos nuestro Token generado con el @BotFather
# tb = telebot.TeleBot(TOKEN)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    # change create method
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('website_id'):
                website = self.env['website'].browse(vals['website_id'])
                _logger.debug(vals)
                # if 'company_id' in vals:
                #     company = self.env['res.company'].browse(vals['company_id'])
                #     if website.company_id.id != company.id:
                #         raise ValueError(_("The company of the website you are trying to sale from (%s) is different than the one you want to use (%s)") % (website.company_id.name, company.name))
                # else:
                #     vals['company_id'] = website.company_id.id

        return super().create(vals_list)