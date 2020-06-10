# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    signature = fields.Binary(
        'Firma'
    )
    accreditation = fields.Text(
        'Accreditation'
    )
    approval_authority = fields.Text(
        'Approval Authority'
    )
