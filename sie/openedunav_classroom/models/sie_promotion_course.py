# -*- coding: utf-8 -*


from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SiePromotionCourse(models.Model):
    _name = 'sie.promotion.course'
    _description = 'Promotion Course'

    name = fields.Char(
        string='Nombre',
        required=True
    )
    display_name = fields.Char(
        string='Nombre completo',
        compute='_compute_display_name'
    )

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            if record.name:
                prefix = u"Promoción"
                record.display_name = '%s %s' % (prefix, record.name)

    @api.depends('display_name')
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, '%s' % record.display_name))
        return result
