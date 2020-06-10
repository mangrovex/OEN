# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SieParameters(models.Model):
    _name = 'sie.parameters'
    _description = 'Parameters'

    name = fields.Char(
        string='Nombre',
        required=True
    )
    display_name = fields.Char(
        string='Nombre'
    )

    @api.depends('display_name')
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, '%s' % record.display_name))
        return result
