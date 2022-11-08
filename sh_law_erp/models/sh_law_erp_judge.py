# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ShLawErpJudge(models.Model):
    _name = "sh.law.erp.judge"
    _description = "Law Erp Judge"
    _order = "id desc"

    name = fields.Char(string="Name", required=True)
    contact = fields.Char(string="Contact Number")
