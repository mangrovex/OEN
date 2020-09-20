# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class School(models.Model):
    _name = 'sie.school'
    _description = 'School'

    name = fields.Char(
        string='Nombre',
        required=True
    )
    shortname = fields.Char(
        string='Siglas',
        required=True
    )
    code = fields.Char(
        u'Código',
        default="/",
        readonly=True,
        copy=False,
        required=True
    )

    _sql_constraints = [
        ('name_uk', 'unique(name)', u'Nombre debe ser único'),
        ("school_unique_code", "UNIQUE (code)", _("The code must be unique!")),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("code", "/") == "/":
                vals["code"] = self.env.ref(
                    "openedunav_core.sequence_school", raise_if_not_found=False
                ).next_by_id()
        return super().create(vals_list)
