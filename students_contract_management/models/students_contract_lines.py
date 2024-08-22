# -*- coding: utf-8 -*-
from email.policy import default

from odoo import fields, models, api


class StudentsContractLines(models.Model):
    _name = "students.contract.lines"
    _description = "Students Contract Lines"

    @api.depends("quantity", "price_unit")
    def _compute_subtotal(self):
        for record in self:
            record.price_subtotal = record.quantity * record.price_unit

    @api.depends("product_tmpl_id")
    def _compute_description(self):
        for record in self:
            record.description = record.product_tmpl_id.name if record.product_tmpl_id else "New Product"

    contract_id = fields.Many2one("students.contract", string="Contract", ondelete="cascade")
    product_tmpl_id = fields.Many2one("product.template", string="Product", required=True)
    description = fields.Text(string="Description", compute="_compute_description", readonly=False)
    quantity = fields.Float(string="Quantity", default=1, required=True)
    currency_id = fields.Many2one(related="contract_id.currency_id", string="Currency", store=True, readonly=True)
    price_unit = fields.Monetary(string="Unit Price", required=True, currency_field="currency_id")
    price_subtotal = fields.Monetary(string="Subtotal", store=True, readonly=True, compute="_compute_subtotal")

    @api.onchange("product_tmpl_id")
    def _onchange_product_tmpl_id(self):
        if self.product_tmpl_id:
            self.price_unit = self.product_tmpl_id.list_price
