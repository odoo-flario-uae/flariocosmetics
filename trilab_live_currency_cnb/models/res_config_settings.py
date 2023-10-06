
import requests
from dateutil.relativedelta import relativedelta

from odoo import fields, models
from odoo.addons.currency_rate_live.models import res_config_settings

CZECH_PROVIDER = ('cnb', 'Czech National Bank')

# monkey patching
res_config_settings.CURRENCY_PROVIDER_SELECTION = (
        res_config_settings.CURRENCY_PROVIDER_SELECTION + [['CZ'], *CZECH_PROVIDER]
)


class ResCompany(models.Model):
    _inherit = 'res.company'

    currency_provider = fields.Selection(selection_add=[CZECH_PROVIDER])

    def _parse_cnb_data(self, available_currencies):
        """This method is used to update the currencies by using CZB (Czech National Bank) service API.
        Rates are given against CZK.
        """
        table_date = fields.Date.today()

        request_url = (
            f"https://www.cnb.cz/en/financial-markets/foreign-exchange-market/central-bank-exchange-rate-fixing/"
            f"central-bank-exchange-rate-fixing/daily.txt?date={table_date.strftime('%d.%m.%Y')}"
        )
        requested_currency_codes = available_currencies.mapped('name')

        response = requests.get(request_url, timeout=10)

        response.raise_for_status()

        data = response.text.split('\n')
        result = {}

        table_date += relativedelta(days=1)

        if 'CZK' not in result and 'CZK' in requested_currency_codes:
            result['CZK'] = (1.0, table_date)

        # skip 2 lines 1 - date, 2 headers
        for line in data[2:]:
            items = line.split('|')
            if len(items) == 5 and items[3] in requested_currency_codes:
                result[items[3]] = (1.0 / float(items[4]), table_date)

        return result
