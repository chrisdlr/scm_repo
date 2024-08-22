# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class StudentsContractPayment(models.Model):
    _name = "students.contract.payment"
    _description = "Students Contract"
    _rec_name = "payment_number"

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            if val.get('payment_number', _('New')) == _('New'):
                val['payment_number'] = self.env['ir.sequence'].next_by_code('students.contract.payment.sequence') or _('New')
        return super(StudentsContractPayment, self).create(vals)

    payment_number = fields.Char(string="Payment Number", required=True, copy=False, readonly=True, index=True, default=lambda self: _("New"))
    contract_id = fields.Many2one("students.contract", string="Contract", required=True)
    payment_date = fields.Date(string="Payment Date", required=True, default=fields.Date.today())
    payment_amount = fields.Monetary(string="Payment Amount", required=True)
    payment_method = fields.Selection([
        ("cash", "Cash"),
        ("bank", "Bank"),
        ("credit_card", "Credit Card"),
    ], string="Payment Method", required=True, default="cash")
    payment_note = fields.Text(string="Payment Note")
    currency_id = fields.Many2one("res.currency", string="Currency", default=lambda self: self.env.company.currency_id.id)
