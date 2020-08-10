# -*- coding: utf-8 -*

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SieRegisterDirectors(models.Model):
    _name = 'sie.register.directors'
    _description = 'Register Directors'

    name = fields.Char(
        string=u'Nombre',
        compute='_compute_name',
        store=True
    )
    display_name = fields.Char(
        string='Nombre',
        compute='_compute_display_name',
        required=True
    )
    course_id = fields.Many2one(
        'sie.course',
        string='Curso',
        required=True,
        ondelete='restrict'
    )
    # promotion_course_id = fields.Many2one('sie.promotion.course', string='Promotion', required=True)
    year = fields.Char(
        string=u'Año',
        compute='_compute_year',
        store=True
    )
    director_id = fields.Many2one(
        'sie.faculty',
        string='Director',
        required=True,
        domain="[('director', '=', True)]",
        ondelete='restrict'
    )
    statistician_id = fields.Many2one(
        'sie.faculty',
        string=u'Jefe Estadístico',
        required=True,
        domain="['|',('planta', '=', True),('division', '=', True)]",
        ondelete='restrict'
    )
    position_director = fields.Char(
        string='Cargo Director',
        required=True
    )
    position_statistician = fields.Char(
        string=u'Cargo Estadístico',
        required=True
    )

    _sql_constraints = [
        ('name_uk', 'unique(course_id)', 'No puede repetir el curso')
    ]

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            if record.name:
                prefix = u"Promoción"
                record.display_name = '%s %s' % (prefix, record.name)

    @api.depends('course_id')
    def _compute_name(self):
        for record in self:
            if record.course_id:
                year = record.course_id.start_date.year
                record.name = '%s %s' % (record.course_id.name, year)

    @api.depends('course_id')
    def _compute_year(self):
        for record in self:
            if record.course_id:
                record.year = record.course_id.start_date.year

    # @api.onchange('name')
    # def _check_digit(self):
    #     if self.name:
    #         unicodestring = self.name
    #         s = str(unicodestring).encode("utf-8")
    #         try:
    #             float(s)
    #         except ValueError:
    #             raise ValidationError(_(u'Not a number'))

    @api.depends('display_name')
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, '%s' % record.display_name))
        return result
