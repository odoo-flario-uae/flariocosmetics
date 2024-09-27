# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    fee_delivery = fields.Text(
        'For manager delivery', translate=True,
        help="Use this text if you need to change badge of delivery carrier")
    #
    # payments_containts = fields.Many2Many('')