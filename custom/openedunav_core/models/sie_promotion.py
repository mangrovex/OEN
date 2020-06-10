# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SiePromotion(models.Model):
    _name = 'sie.promotion'
    _description = 'SiePromotion'

    name = fields.Char(
        string='Nombre',
        required=True
    )
    display_name = fields.Char(
        string='Nombre Completo',
        compute='_compute_display_name'
    )

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            if record.name:
                prefix = _(u"Promoción")
                record.display_name = '%s %s' % (prefix, record.name)

    @api.onchange('name')
    def _check_digit(self):
        for record in self:
            if record.name:
                unicodestring = record.name
                s = str(unicodestring).encode("utf-8")
                try:
                    float(s)
                except ValueError:
                    raise ValidationError(_(u'No es un número'))

    @api.depends('display_name')
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, '%s' % record.display_name))
        return result
