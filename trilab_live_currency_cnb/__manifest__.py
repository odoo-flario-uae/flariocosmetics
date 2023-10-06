{
    'name': 'Trilab Live Currency Exchange Rate for CNB (Czech)',
    'author': 'Trilab',
    'website': "https://trilab.pl",
    'support': 'odoo@trilab.pl',
    'version': '16.0.2',
    'category': 'Accounting',
    'summary': """
        Import exchange rates from the Internet. CNB (Czech National Bank)""",
    'description': """
        Module extends built-in live currency module to use CNB (Česká národní banka) API to
        download current exchange rates.

        It uses CZK (Kč) as a base currency.

        Module fetches rate table that is active at the moment of download.

    """,
    'depends': [
        'currency_rate_live'
    ],
    'data': [
    ],
    'demo': [
    ],
    'images': [
        'static/description/banner.png'
    ],
    'installable': True,
    'auto_install': True,
    'application': True,
    'license': 'OPL-1',
}
