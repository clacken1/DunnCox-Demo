# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models

class ShLawMatter(models.Model):
    _name = "sh.law.matter"
    _inherit = ["portal.mixin", "mail.thread",
                "mail.activity.mixin", "utm.mixin"]
    _description = "Law Matter"
    _order = "id desc"

    name = fields.Char(string="Matter", required=True,
                       tracking=True)
    client_id = fields.Many2one(
        "res.partner", string="Client", tracking=True)
    judge_id = fields.Many2one("sh.law.erp.judge", string="Judge")
    open_date = fields.Datetime(string="Open Date")
    matter_type_id = fields.Many2one(
        "sh.law.matter.type", string="Type of Matter",
        tracking=True)
    matter_category_id = fields.Many2one(
        "sh.law.matter.category", string="Category of Matter",
        tracking=True)

    lawyer = fields.Many2one(
        "hr.employee", string="Lawyer", tracking=True)

    other_lawyer = fields.Many2many(
        "hr.employee", string="Lawyer Multy", tracking=True )

    close_date = fields.Datetime(string="Close Date")
    discription = fields.Text("Description", tracking=True)
    victim = fields.Many2many("sh.law.erp.victim", tracking=True)
    act_article = fields.Many2many(
        "sh.law.erp.act.article", tracking=True)

    oposition_line = fields.One2many(
        "sh.law.matter.opposition.line",
        "matter_id", string="Opposition Line")

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("approve", "Approved"),
            ("progress", "In Progress"),
            ("done", "Won"),
            ("lost", "Lost"),
        ], string="Status", default="draft", readonly=True
    )
    evidence_line = fields.One2many(
        "sh.law.erp.evidence", "matter_id", string="Evidence")
    trial_line = fields.One2many("sh.law.erp.trial", "matter", string="Trial")

    evidence_count = fields.Integer(
        string="Evidence Count", compute="_compute_evidence_count")
    trial_count = fields.Integer(
        string="Trials", compute="_compute_trial_count")
    invoice_count = fields.Integer(
        string="Invoice", compute="_compute_invoice_count")
    payment_by = fields.Selection(
        selection=[
            ("trial", "Per Trial"),
            ("case", "Per Case"),
            ("hour", "Per Hour"),
        ], string="Payment By"
    )
    mark_lost = fields.Text("Lost Reason")

    @api.model
    def create(self,vals):
        res = super(ShLawMatter, self).create(vals)
        if res.lawyer:
            if res.lawyer not in res.other_lawyer:
                res['other_lawyer'] = [(4, res.lawyer.id)]
        return res

    @api.onchange('lawyer')
    def lawyer_onchange(self):
        if self.lawyer:
            if self.lawyer not in self.other_lawyer:
                self['other_lawyer'] = [(4, self.lawyer.id)]

    def _compute_evidence_count(self):
        if self:
            for rec in self:
                evidences = self.env["sh.law.erp.evidence"].search(
                    [("matter_id", "=", rec.id)])
                if evidences:
                    rec.evidence_count = len(evidences.ids)
                else:
                    rec.evidence_count = 0

    def evidence_btn(self):
        return{
            "name": "Evidence",
            "type": "ir.actions.act_window",
            "res_model": "sh.law.erp.evidence",
            "view_mode": "tree,form",
            "domain": [("matter_id", "=", self.id)],
            "context": {"default_move_type": "out_invoice",
                        "default_matter_id": self.id,
                        "default_client": self.client_id.id},
            "target": "current",
        }

    def _compute_trial_count(self):
        if self:
            for rec in self:
                trials = self.env["sh.law.erp.trial"].search(
                    [("matter", "=", rec.id)])
                if trials:
                    rec.trial_count = len(trials.ids)
                else:
                    rec.trial_count = 0

    def trial_btn(self):
        return{
            "name": "Trials",
            "type": "ir.actions.act_window",
            "res_model": "sh.law.erp.trial",
            "view_mode": "tree,form",
            "domain": [("matter", "=", self.id)],
            "context": {"default_move_type": "out_invoice",
                        "default_matter": self.id,
                        "default_partner_id": self.client_id.id},
            "target": "current",
        }

    def _compute_invoice_count(self):
        if self:
            for rec in self:
                invoices = self.env["account.move"].search(
                    [("matter_id", "=", rec.id)])
                if invoices:
                    rec.invoice_count = len(invoices.ids)
                else:
                    rec.invoice_count = 0

    def invoice_btn(self):
        return{
            "name": "Invoices",
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "tree,form",
            "domain": [("matter_id", "=", self.id)],
            "context": {"default_move_type": "out_invoice",
                        "default_matter_id": self.id,
                        "default_partner_id": self.client_id.id,
                        "default_lawyer": self.lawyer.id,
                        "default_payment_by": self.payment_by},
            "target": "current",
        }
    # def invoice_btn(self):
    #     return{
    #         "name": "Invoices",
    #         "type": "ir.actions.act_window",
    #         "res_model": "account.move",
    #         "view_mode": "tree,form",
    #         "domain": [("matter_id", "=", self.id)],
    #         "context": {"default_move_type": "out_invoice",
    #                     "default_matter_id": self.id,
    #                     "default_partner_id": self.client_id.id,
    #                     "default_lawyer": self.other_lawyer.ids,
    #                     "default_other_lawyer": self.other_lawyer.ids,
    #                     "default_payment_by": self.payment_by},
    #         "target": "current",
    #     }

    def won_btn(self):
        self.write({"state": "done"})

    def in_progress_btn(self):
        self.write({"state": "progress"})

    def apprpved_btn(self):
        self.write({"state": "approve"})

    def mark_lost_btn(self):
        return

    def add_evidence_btn(self):
        self.ensure_one()
        return{
            "name": "Evidence",
            "type": "ir.actions.act_window",
            "res_model": "sh.law.erp.evidence",
            "view_mode": "form",
            "context": {"default_matter_id": self.id,
                        "default_client": self.client_id.id},
            "target": "new",
        }

    def add_trial_btn(self):
        self.ensure_one()
        return{
            "name": "Trials",
            "type": "ir.actions.act_window",
            "res_model": "sh.law.erp.trial",
            "view_mode": "form",
            "context": {"default_matter": self.id,
                        "default_partner_id": self.client_id.id,
                        "default_judge_id": self.judge_id.id},
            "target": "new",
        }
