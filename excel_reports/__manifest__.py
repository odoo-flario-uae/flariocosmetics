# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    "name": "Excel Import/Export module",
    "version": "16.0.1.0.0",
    "author": "Ecosoft,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/server-tools",
    "category": "Tools",
    "depends": ["excel_import_export", "sale_management"],
    "data": [
        "import_sale_order/actions.xml",
        "import_sale_order/templates.xml",
    ],
    "installable": True,
    "development_status": "Beta",
    "maintainers": ["kittiu"],
}
