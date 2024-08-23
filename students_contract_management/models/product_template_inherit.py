# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ProductTemplateInherit(models.Model):
    _inherit = "product.template"

    is_subject = fields.Boolean(string="Is Subject", default=False)
    course_credits = fields.Integer(string="Course Credits")
    course_teacher_ids = fields.Many2many("res.partner", domain="[('role', '=', 'teacher')]", string="Teacher")
