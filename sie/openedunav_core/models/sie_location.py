# -*- coding: utf-8 -*-

from odoo import models, fields, _, api
from odoo.osv import expression


class Location(models.Model):
    _name = 'sie.location'
    _description = 'Location'

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
        ("location_unique_code", "UNIQUE (code)", _("The code must be unique!")),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("code", "/") == "/":
                vals["code"] = self.env.ref(
                    "openedunav_core.sequence_location", raise_if_not_found=False
                ).next_by_id()
        return super().create(vals_list)

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if operator == 'ilike' and not (name or '').strip():
            domain = []
        else:
            domain = ['|', ('name', operator, name), ('shortname', operator, name)]
        rec = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return models.lazy_name_get(self.browse(rec).with_user(name_get_uid))

