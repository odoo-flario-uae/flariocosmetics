# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Users(models.Model):
    _inherit = 'res.users'

    is_new_user = fields.Boolean(string='Is New User', readonly=True, default=True)
