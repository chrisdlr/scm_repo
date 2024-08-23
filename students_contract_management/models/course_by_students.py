# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class CoursesByStudents(models.Model):
    _name = "courses.by.students"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Courses By Students"
    _rec_name = "course_name"
    _order = "id asc, course_number desc"

    _sql_constraints = [
        ("course_number_student_period_uniq", "unique(course_number, student_id, period)", "The course number must be unique per student and period!"),
    ]

    @api.depends("course_number", "student_id", "period")
    def _get_course_name(self):
        for course in self:
            if course.course_number and course.student_id and course.period:
                course.course_name = f"{course.course_number.upper()} - {course.student_id.name} - {course.period.title()}"
            else:
                course.course_name = _("New")

    course_name = fields.Char(string="Course Name", compute="_get_course_name", readonly=False, required=True)
    course_number = fields.Selection([
        ("i", "I"),
        ("ii", "II"),
    ], string="Course Number", default="i", copy=False, tracking=True)
    student_id = fields.Many2one("res.partner", domain="[('role', '=', 'student')]", string="Student", tracking=True, required=True)
    period = fields.Selection([
        ("first", "First"),
        ("second", "Second"),
        ("third", "Third"),
        ("fourth", "Fourth"),
        ("fifth", "Fifth"),
        ("sixth", "Sixth"),
        ("seventh", "Seventh"),
        ("eighth", "Eighth"),
        ("ninth", "Ninth"),
        ("tenth", "Tenth"),
    ], string="Period", default="first", copy=False, tracking=True)
    courses_line_ids = fields.One2many("courses.by.students.lines", "course_id", string="Courses")
