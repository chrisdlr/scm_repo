# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from dateutil.relativedelta import relativedelta


class StudentsContract(models.Model):
    _name = "students.contract"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Students Contract"
    _rec_name = "contract_number"
    _order = "id asc, contract_number desc"

    @api.depends("contract_lines.price_subtotal")
    def _compute_amount_all(self):
        for contract in self:
            amount_untaxed = 0.0
            for line in contract.contract_lines:
                amount_untaxed += line.price_subtotal
            contract.amount_total = amount_untaxed

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            if val.get('contract_number', _('New')) == _('New'):
                val['contract_number'] = self.env['ir.sequence'].next_by_code('students.contract.sequence') or _('New')
        return super(StudentsContract, self).create(vals)

    contract_number = fields.Char(string="Contract Number", required=True, copy=False, readonly=True, index=True, default=lambda self: _("New"))
    student_id = fields.Many2one("res.partner", domain="[('role', '=', 'student')]", string="Student", tracking=True, required=True)
    state = fields.Selection([
        ("draft", "Draft"),
        ("confirmed", "Confirmed"),
        ("done", "Done"),
        ("cancelled", "Cancelled"),
    ], string="State", default="draft", copy=False, tracking=True)
    payment_state = fields.Selection([
        ("not_paid", "Not Paid"),
        ("partially_paid", "Partially Paid"),
        ("paid", "Paid"),
    ], string="Payment State", copy=False, default="not_paid")
    terms = fields.Text(string="Terms and Conditions")
    contract_lines = fields.One2many("students.contract.lines", "contract_id", string="Contract Lines")
    payment_lines = fields.One2many("students.contract.payment", "contract_id", string="Payment Lines")
    date_start = fields.Datetime("Start Date", required=True, default=fields.Date.today())
    date_end = fields.Datetime("Finish Date", required=True, default=fields.Date.today() + relativedelta(years=1))
    currency_id = fields.Many2one("res.currency", string="Currency", default=lambda self: self.env.company.currency_id.id)
    amount_total = fields.Monetary(string="Total", store=True, compute="_compute_amount_all", tracking=4)

    def confirm_contract(self):
        self.write({
            "state": "confirmed",
            "payment_state": "not_paid",
        })

    def cancel_contract(self):
        self.write({
            "state": "cancelled",
            "payment_state": "not_paid",
        })

    def set_to_draft(self):
        self.write({
            "state": "draft",
            "payment_state": "not_paid",
        })

    def check_payment_total_paid(self):
        for rec in self:
            total_paid = sum(rec.payment_lines.mapped("payment_amount"))
            if total_paid >= rec.amount_total:
                rec.write({
                    "payment_state": "paid",
                    "state": "done",
                })
            elif total_paid > 0:
                rec.write({
                    "payment_state": "partially_paid"
                })
            else:
                rec.write({
                    "payment_state": "not_paid"
                })
