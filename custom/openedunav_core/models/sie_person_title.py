# -*- coding: utf-8 -*-

from odoo import models, fields


class SiePersonTitle(models.Model):
    _name = 'sie.person.title'
    _description = 'SiePersonTitle'

    name = fields.Char(
        string='Title',
        required=True,
        translate=True)
    shortcut = fields.Char(
        string='Abbreviation',
        translate=True
    )
    acronym = fields.Char(
        'Acronimo',
        size=10,
        required=True,
        search='_search_name'
    )

    _sql_constraints = [
        ('acronym_uk', 'unique(acronym)', u'Acronimo debe ser único'),
        ('name_uk', 'unique(name)', u'Nombre debe ser único'),
    ]
