# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError


class AddContractPayment(models.TransientModel):
    _name = "add.contract.payment"
    _description = "Add Contract Payment"

    @api.depends("contract_id.amount_total")
    def _compute_total_to_pay(self):
        for record in self:
            record.total_to_pay = record.contract_id.amount_total - sum(record.contract_id.payment_lines.mapped("payment_amount"))

    @api.onchange("payment_amount")
    def _check_amount_to_pay(self):
        if self.payment_amount > self.total_to_pay:
            raise UserError(_("Payment amount is greater than total to pay."))

    contract_id = fields.Many2one("students.contract", string="Contract", required=True)
    currency_id = fields.Many2one("res.currency", related="contract_id.currency_id", string="Currency", readonly=True)
    total_to_pay = fields.Monetary(string="Total to Pay", compute="_compute_total_to_pay", store=True, readonly=True)
    payment_amount = fields.Monetary(string="Payment Amount", required=True)
    payment_date = fields.Date(string="Payment Date", required=True)
    payment_method = fields.Selection([
        ("cash", "Cash"),
        ("bank", "Bank"),
        ("credit_card", "Credit Card"),
    ], string="Payment Method", default="cash")
    notes = fields.Text(string="Notes")

    def button_add_contract_payment(self):
        self._check_amount_to_pay()

        self.env["students.contract.payment"].create({
            "contract_id": self.contract_id.id,
            "payment_amount": self.payment_amount,
            "payment_date": self.payment_date,
            "payment_method": self.payment_method,
            "payment_note": self.notes,
            "currency_id": self.currency_id.id,
        })
        self.contract_id.message_post(
            body=_("Payment of %s %s added.") % (self.payment_amount, self.currency_id.name),
            message_type='comment',
            subtype_id=self.env.ref('mail.mt_note').id,
        )

        self.contract_id.check_payment_total_paid()
        return {"type": "ir.actions.act_window_close"}
