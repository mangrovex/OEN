# -*- coding: utf-8 -*-

from odoo import models, fields


class Location(models.Model):
    _name = 'sie.location'
    _description = 'Location'

    name = fields.Char(
        string='Nombre',
        required=True
    )
    code = fields.Char(
        u'Código',
        size=15,
        required=True
    )

    _sql_constraints = [
        ('name_uk', 'unique(name)', u'Nombre debe ser único')
    ]
