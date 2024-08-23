# -*- coding: utf-8 -*-
from odoo import fields, models, api


class StudentsContractLines(models.Model):
    _name = "students.contract.lines"
    _description = "Students Contract Lines"

    @api.depends("quantity", "price_unit")
    def _compute_subtotal(self):
        for record in self:
            record.price_subtotal = record.quantity * record.price_unit

    @api.depends("subject_id")
    def _compute_description(self):
        for record in self:
            record.description = record.subject_id.name if record.subject_id else "New Product"

    contract_id = fields.Many2one("students.contract", string="Contract", ondelete="cascade")
    subject_id = fields.Many2one("product.template", string="Subject", required=True)
    teacher_id = fields.Many2one("res.partner", domain="[('role', '=', 'teacher')]", string="Teacher", required=True)
    description = fields.Text(string="Description", compute="_compute_description", readonly=False)
    quantity = fields.Float(string="Quantity", default=1, required=True)
    currency_id = fields.Many2one(related="contract_id.currency_id", string="Currency", store=True, readonly=True)
    price_unit = fields.Monetary(string="Unit Price", required=True, currency_field="currency_id")
    price_subtotal = fields.Monetary(string="Subtotal", store=True, readonly=True, compute="_compute_subtotal")

    @api.onchange("subject_id")
    def _onchange_subject_id(self):
        if self.subject_id:
            self.price_unit = self.subject_id.list_price
