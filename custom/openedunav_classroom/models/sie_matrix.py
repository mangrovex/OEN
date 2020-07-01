# -*- coding: utf-8 -*

import datetime
import logging

from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SieMatrix(models.Model):
    _name = 'sie.matrix'
    _description = 'Matrix'
    _order = 'year'

    @api.model
    def year_selection(self):
        year = 2000 # replace 2000 with your a start year
        year_list = []
        while year != 2030: # replace 2030 with your end year
            year_list.append((str(year), str(year)))
            year += 1
        return year_list

    name = fields.Char(
        string='Nombre',
        requeried=True,
        store=True
    )
    display_name = fields.Char(
        string=u'Descripción',
        compute='_compute_display_name',
        store=True
    )
    parameter_ids = fields.One2many(
        'sie.matrix.parameter',
        inverse_name='matrix_id',
        string='Parameters',
        store=True,
        ondelete='cascade'
    )
    promotion_course = fields.Many2one(
        'sie.promotion.course',
        string=u'Promoción del Curso',
        ondelete='restrict'
    )
    year = fields.Selection(
        year_selection,
        string='Year',
        default="2020"
    )
    min_aprovechamiento = fields.Integer(
        string="Min score Aprovechamiento ",
        default=14
    )
    min_integrador = fields.Integer(
        string="Min score Integrador ",
        default=14
    )
    min_trabajo = fields.Integer(
        string="Min score Trabajo ",
        default=14
    )
    min_aprendizaje = fields.Integer(
        string="Min score Aprendizaje ",
        default=14
    )
    min_productividad = fields.Integer(
        string="Min score Productividad",
        default=14
    )
    min_actitud = fields.Integer(
        string="Min score Profesional",
        default=14
    )
    minimum_score = fields.Integer(
        string='Overall Average to Pass',
        default=15
    )

    _sql_constraints = [
        ('name_uk', 'unique(name)', u'Nombre debe ser único'),
    ]

    @api.depends('name', 'promotion_course', 'year')
    def _compute_display_name(self):
        for record in self:
            if record.name and record.promotion_course and record.year:
                display_name = '%s-%s-%s' % (record.name, record.promotion_course.name, record.year)
                record.display_name = display_name

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        new_matrix = None
        for record in self:
            default = dict(default or {})
            copied_count = record.search_count(
                [('name', '=like', u"Copy of {}%".format(record.name))])
            if not copied_count:
                new_name = u"Copy of {}".format(record.name)
            else:
                new_name = u"Copy of {} ({})".format(record.name, copied_count)
            default['name'] = new_name
            new_matrix = super(SieMatrix, self).copy(default)
            parameter_ids = self.env['sie.matrix.parameter'].search([('matrix_id', '=', record.id)])
            new_parameter_ids = self.env['sie.matrix.parameter']
            for parameter in parameter_ids:
                new_parameter = new_parameter_ids.create({'coefficient': parameter.coefficient,
                                                          'param_name': parameter.param_name.id,
                                                          'matrix_id': new_matrix.id})
                SieMatrix._create_children(record, parameter, new_parameter)
        return new_matrix

    @staticmethod
    def _create_children(self, parameter, new_parameter):
        if parameter.last_child:
            return
        new_parameter_ids = self.env['sie.matrix.parameter']
        for new_parameter_child in parameter.child_ids:
            new = new_parameter_ids.create({'coefficient': new_parameter_child.coefficient,
                                            'param_name': new_parameter_child.param_name.id,
                                            'parent_id': new_parameter.id})
            if not new_parameter_child.last_child:
                SieMatrix._create_children(self, new_parameter_child, new)
        return

    @api.onchange('name')
    def do_stuff(self):
        for record in self:
            if record.name:
                record.name = record.name.upper()

    @api.constrains('parameter_ids')
    def _check_coefficient(self):
        for record in self:
            if record.parameter_ids:
                total = sum(record.coefficient for record in record.parameter_ids)
                if str("%.3f" % total) != '1.000':
                    raise ValidationError("Sum of coefficients must be equal to 1")
                for obj in record.parameter_ids:
                    record.validate_sum_children(obj)

    def validate_sum_children(self, child_ids):
        for record in self:
            if child_ids.child_ids:
                total = sum(record.coefficient for record in child_ids.child_ids)
                if str("%.3f" % total) != '1.000':
                    raise ValidationError("Sum of coefficients must be equal to 1 " + child_ids.name)
                for child_id in child_ids.child_ids:
                    record.validate_sum_children(child_id)
            return True
