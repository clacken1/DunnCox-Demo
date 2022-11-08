# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models


class ShLawMatterOppositionLine(models.Model):
    _name = "sh.law.matter.opposition.line"
    _description = "Law Opposition Line"

    party_name_id = fields.Many2one(
        "sh.law.erp.opposition.parties", string="Party Name")
    party_contact = fields.Char(string="Contact No. ")
    Lawyer_name_id = fields.Many2one(
        "sh.law.erp.opposition.lawyer", string="Lawyer Name")
    lawyer_contact = fields.Char(string="Contact No.")
    matter_id = fields.Many2one("sh.law.matter", string="Matter")

    @api.onchange("party_name_id")
    def party_contact_change(self):
        if self:
            if self.party_name_id and self.party_name_id.contact:
                self.party_contact = self.party_name_id.contact
            else:
                self.party_contact = False

    @api.onchange("Lawyer_name_id")
    def lawyer_contact_change(self):
        if self:
            if self.Lawyer_name_id and self.Lawyer_name_id.contact:
                self.lawyer_contact = self.Lawyer_name_id.contact
            else:
                self.lawyer_contact = False
