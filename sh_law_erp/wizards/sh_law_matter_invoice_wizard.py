# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ShLawMatterMarkLostWizard(models.TransientModel):
    _name = "sh.law.matter.invoice.wizard"
    _description = "Matter Invoice Wizard"

    def _get_default_currency_id(self):
        return self.env.company.currency_id.id

    client_id = fields.Many2one(
        "res.partner", string="Customer", required=True)
    matter_id = fields.Many2one(
        "sh.law.matter", string="Matter", readonly=True)
    lawyer_id = fields.Many2one("hr.employee", string="Lawyer", readonly=True)

    others_lawyer_id = fields.Many2many("hr.employee", string="Others Lawyer", readonly=True)

    invoice_date = fields.Datetime("Invoice Date", default=fields.Datetime.now)
    payment_term_id = fields.Many2one(
        "account.payment.term", string="Payment Term")
    payment_by = fields.Selection(
        selection=[
            ("trial", "Per Trial"),
            ("case", "Per Case"),
            ("hour", "Per Hour"),
        ], string="Payment By", required=True
    )
    trials_ids = fields.Many2many("sh.law.erp.trial", string="Trials")
    hours = fields.Float("Hours", default=1.0, required=True)
    invoice_amt = fields.Monetary(string="Amount Per Case/Hour/Trial")
    total_invoice_amount = fields.Monetary(string="Total Invoice Amount")
    currency_id = fields.Many2one(
        "res.currency",
        default=_get_default_currency_id, required=True)

    @api.model
    def default_get(self, fields):
        res = super(ShLawMatterMarkLostWizard, self).default_get(fields)
        active_ids = self.env.context.get("active_ids")
        matter = self.env["sh.law.matter"].browse(active_ids)

        if matter:
            values = {
                "matter_id": matter.id,
                "client_id": matter.client_id.id if matter.client_id else False,
                "lawyer_id": matter.lawyer.id if matter.lawyer else False,
                "others_lawyer_id": matter.other_lawyer.ids if matter.other_lawyer else False,
                "payment_by": matter.payment_by,

            }
            if matter.other_lawyer:
                amount = 0
                if matter.payment_by == "trial":
                    for emp in matter.other_lawyer:
                        amount += emp.wage_per_trial

                elif matter.payment_by == "case":
                    for emp in matter.other_lawyer:
                        amount += emp.wage_per_case

                elif matter.payment_by == "hour":
                    for emp in matter.other_lawyer:
                        amount += emp.wage_per_hour

                values.update({
                    "invoice_amt": amount
                })
            res.update(values)
        return res

    def create_invoice(self):
        if self:
            if not self.client_id or not self.matter_id or not self.payment_by or not self.others_lawyer_id:
                raise UserError(
                    _("Please Select Customer and Payment By first"))

        lst_inv=[]
        for lawyer in self.others_lawyer_id:
            quantity=0
            price=0.00

            if self.payment_by=='hour':
                quantity=self.hours
                price=lawyer.wage_per_hour

            if self.payment_by == "trial":
                #    already_emp=[]
                for emp in self.trials_ids._origin:
                    if lawyer==emp.select_lawyer:
                        quantity+=1
                        price=emp.select_lawyer.wage_per_trial

            if self.payment_by == "case":
                quantity=1
                price=lawyer.wage_per_case

            lawyer_detail={
                'name':lawyer.name,
                'quantity':quantity,
                'price_unit':price,
                # 'move_id' : move_id.id,
                'account_id' : 5
            }
            lst_inv.append((0,0,lawyer_detail))
        new_invoice = {
                    'partner_id' : self.client_id.id,
                    'lawyer' : self.lawyer_id.id,
                    'move_type' : 'out_invoice',
                    'invoice_line_ids':lst_inv,
                    'matter_id' : self.matter_id.id,
                    'trial_ids':self.trials_ids.ids if self.trials_ids else False,
                    "payment_by": self.payment_by,
                    "other_lawyer": self.matter_id.other_lawyer.ids if self.others_lawyer_id else False,
                    'to_price_unit' : self.invoice_amt,
                }

        move_id=self.env['account.move'].create(new_invoice)

        action = {
            "name": "Invoices",
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "form",
            "res_id": move_id.id,
        }
        return action

    @api.onchange("payment_by", "hours", "trials_ids",)
    def compute_per_amount_case_hour_trials(self):
        if self:
            amount = 0
            if self.lawyer_id or self.others_lawyer_id:
                amount = 0
                if self.payment_by == "trial":
                    for emp in self.others_lawyer_id:
                        amount += emp.wage_per_trial

                elif self.payment_by == "case":
                    for emp in self.others_lawyer_id:
                        amount += emp.wage_per_case

                elif self.payment_by == "hour":
                    for emp in self.others_lawyer_id:
                        amount += emp.wage_per_hour

            self.invoice_amt = amount

    @api.onchange("invoice_amt", "payment_by", "hours", "trials_ids")
    def compute_total_invoice_amount(self):
        if self:
            amount = 0
            if self.payment_by == "trial":
                for emp in self.trials_ids._origin:
                    amount += emp.select_lawyer.wage_per_trial
                self.total_invoice_amount = amount

            elif self.payment_by == "case":
                self.total_invoice_amount = self.invoice_amt

            elif self.payment_by == "hour":
                amount += self.invoice_amt*self.hours
                self.total_invoice_amount = amount

    @api.constrains("hours")
    def check_value(self):
        for rec in self:
            if rec.hours < 0:
                raise ValidationError(_("Hours cannot be negative"))
            else:
                return rec.hours
