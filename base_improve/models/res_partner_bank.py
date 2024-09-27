# -*- coding: utf-8 -*-

from odoo.addons.base_iban.models import res_partner_bank
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    acc_type2 = fields.Selection(selection=lambda x: x.env['res.partner.bank'].get_supported_account_types(),
                                compute='_compute_acc_type2', string='Type',
                                help='Bank account type: Normal or IBAN. Inferred from the bank account number.')
    acc_number2 = fields.Char('IBAN Number')

    @api.depends('acc_number2')
    def _compute_acc_type2(self):
        for bank in self:
            bank.acc_type2 = self.retrieve_acc_type(bank.acc_number2)

    def write(self, vals):
        if vals.get('acc_number2'):
            try:
                res_partner_bank.validate_iban(vals['acc_number2'])
                vals['acc_number2'] = res_partner_bank.pretty_iban(res_partner_bank.normalize_iban(vals['acc_number2']))
            except ValidationError:
                pass
        return super(ResPartnerBank, self).write(vals)
