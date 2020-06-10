# -*- coding: utf-8 -*-

from odoo import models, fields


class SieReligion(models.Model):
    _name = 'sie.religion'
    _description = 'SieReligion'

    name = fields.Char(
        string='Nombre',
        required=True
    )
    code = fields.Char(
        u'Código',
        size=4,
        required=True
    )

    _sql_constraints = [
        ('name_uk', 'unique(name)', u'Nombre debe ser único')
    ]
