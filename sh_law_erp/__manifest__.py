# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

{
    "name": "Law Management System",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Extra Tools",
    "version": "16.0.1",
    "license": "OPL-1",
    "summary": """
Legal Case Management,
Law Firm ERP,
Legal & Law Practice Management,
Law ERP Module,
Manage Law Cases App,
Law Matter Management System,
Track Law Cases With Full Step,
Handle Law Acts, Law Articles Management Odoo
""",
    "description": """
Do you want the "Law ERP" system in odoo?
Do you want to manage all "Law Matters" from a single system?
In today"s competition, you need a "Law ERP" system to track
every step of the case/matter quickly.
So we have made a "Law ERP Management" system that provides
the full lifecycle of laws.
You can manage every matter with end to end law process.
Using this module you can handle every type of law matters.
Law Management System Odoo, Law ERP System Odoo,
Legal & Law Practice Management, Law ERP Module, Manage Law Cases,
Law Matter Management System, Legal Case Management, Law Firm ERP,
Track Law Cases With Full Step, Handle Law Acts,
Law Articles Management Odoo, Legal Case Management,
Law Firm ERP, Legal & Law Practice Management,
Law ERP Module, Manage Law Cases App,
Law Matter Management System, Track Law Cases With Full Step,
Handle Law Acts, Law Articles Management Odoo
""",
    "depends": [
        "sale_management",
        "hr",
        "utm",
    ],
    "data": [
        "security/sh_law_erp_security.xml",
        "security/ir.model.access.csv",
        "wizards/sh_law_client_request_reject_wizard_views.xml",
        "wizards/sh_law_matter_mark_lost_wizard_views.xml",
        "wizards/sh_law_matter_invoice_wizard_views.xml",
        "views/sh_law_practise_area_views.xml",
        "views/sh_law_client_request_views.xml",
        "views/sh_law_erp_courts_views.xml",
        "views/sh_law_erp_judge_views.xml",
        "views/sh_law_erp_opposition_lawyer_views.xml",
        "views/sh_law_erp_opposition_parties_views.xml",
        "views/sh_law_erp_victim_views.xml",
        "views/sh_law_erp_act_article_views.xml",
        "views/sh_law_erp_evidence_views.xml",
        "views/sh_law_matter_views.xml",
        "views/sh_law_erp_trial_views.xml",
        "views/sh_law_metter_type_views.xml",
        "views/sh_law_matter_category_views.xml",
        "views/sh_law_erp_favor_views.xml",
        "views/hr_views.xml",
        "views/account_views.xml",
        "views/partner_views.xml",
        "reports/sh_law_erp_report.xml",
    ],
    "demo": [],
    "installable": True,
    "application": True,
    "auto_install": False,
    "images": ["static/description/background.png", ],
    "price": 60,
    "currency": "EUR"
}
