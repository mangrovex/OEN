# -*- coding: utf-8 -*-

from odoo import models, fields


class SieNato(models.Model):
    _name = 'sie.nato'
    _description = 'Nato'

    name = fields.Char(
        string=u'Código',
        required=True
    )
    display_name = fields.Char(
        string='Nombre'
    )
