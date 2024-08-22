# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    role = fields.Selection([
        ('student', 'Student'),
        ('teacher', 'Teacher')
    ], string='Role', default='student')
