# -*- coding: utf-8 -*-
from odoo import fields, models, api


class CoursesByStudents(models.Model):
    _name = "courses.by.students.lines"
    _description = "Courses By Students Lines"

    @api.depends("subject_id")
    def _get_subject_info(self):
        for line in self:
            line.course_name = line.subject_id.name
            line.course_code = line.subject_id.default_code
            line.course_credits = line.subject_id.course_credits

    course_id = fields.Many2one("courses.by.students", string="Course")
    subject_id = fields.Many2one("product.template", domain="[('is_subject', '=', True)]", string="Subject", required=True)
    course_name = fields.Char(string="Course Name", compute="_get_subject_info", readonly=False, required=True)
    course_code = fields.Char(string="Course Code", compute="_get_subject_info", readonly=False, required=True)
    course_credits = fields.Float(string="Course Credits", compute="_get_subject_info", readonly=False, required=True)
    available_teacher_ids = fields.Many2many("res.partner", domain="[('role', '=', 'teacher')]", string="Available Teachers")
    course_teacher_id = fields.Many2one("res.partner", domain="[('id', 'in', available_teacher_ids)]", string="Teacher", required=True)

    @api.onchange("subject_id")
    def _onchange_subject_id(self):
        if self.subject_id:
            self.available_teacher_ids = False
            self.available_teacher_ids = self.subject_id.course_teacher_ids
