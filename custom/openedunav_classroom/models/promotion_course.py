# -*- coding: utf-8 -*


from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SiePromotionCourse(models.Model):
    _name = 'sie.promotion.course'
    _description = 'Promotion Course'

    name = fields.Char(string='Nombre', required=True)
    display_name = fields.Char(string='Nombre', compute='_compute_display_name')

    @api.one
    @api.depends('name')
    def _compute_display_name(self):
        if self.name:
            prefix = u"Promoción"
            self.display_name = '%s %s' % (prefix, self.name)

    @api.multi
    @api.depends('display_name')
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, '%s' % record.display_name))
        return result
