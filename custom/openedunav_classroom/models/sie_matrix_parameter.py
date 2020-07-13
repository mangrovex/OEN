# -*- coding: utf-8 -*-

from odoo import _, models, fields, api
from odoo.exceptions import ValidationError

TYPE = [
    ('productivity', 'Productivity'),
]


class SieMatrixParameter(models.Model):
    _name = 'sie.matrix.parameter'
    _description = 'Matrix Parameter'
    _order = 'parent_ref'

    name = fields.Char(
        string=u'Codigo',
        compute='_compute_name'
    )
    param_name = fields.Many2one(
        'sie.param.name',
        string=u'Nombre del Parámetro',
        required=True,
        ondelete='restrict'
    )
    coefficient = fields.Float(
        string='Coeficiente',
        digits='Coefficient',
        required=True,
        default=0.1
    )
    parent_id = fields.Many2one(
        'sie.matrix.parameter',
        string='Padre',
        ondelete='cascade',
        index=True
    )
    child_ids = fields.One2many(
        'sie.matrix.parameter',
        'parent_id',
        string=u'Parametros hijos'
    )
    matrix_id = fields.Many2one(
        'sie.matrix',
        string=u'Parámetros de evaluación',
        ondelete='cascade'
    )
    course_ref = fields.Char(
        string='Curso ref',
        compute='_compute_course_ref',
        store=True
    )
    parent_ref = fields.Char(
        string='Nombre del padre',
        compute='_compute_parent_ref',
        store=True
    )
    last_child = fields.Boolean(
        string=u'Último hijo?',
        compute='_compute_last_child',
        store=True,
        default=True
    )
    total_coefficient = fields.Float(
        string='Suma Coeficientes',
        compute='_compute_total_coefficient',
        digits='Coefficient',
        store=True,
        default=0
    )
    type = fields.Selection(
        TYPE,
        string='Tipo'
    )
    minimun_score = fields.Float(u'Nota Mínima')
    description = fields.Char(u'Descripción')

    _sql_constraints = [
        ('coefficient_ck', 'check(coefficient > 0 and coefficient <= 1)',
         _('Coeficiente debe ser mayor a 1 y menor a 0')),
    ]

    @api.depends('param_name')
    def _compute_name(self):
        for record in self:
            if record.param_name:
                if record.parent_id:
                    if record.parent_ref:
                        if '014' in record.parent_ref:
                            record.name = '%s -> %s -> %s' % (
                            'JUEGOS DE GUERRA', record.parent_id.param_name.name, record.param_name.name)
                        else:
                            record.name = record.parent_id.param_name.name + ' -> ' + record.param_name.name
                else:
                    record.name = record.param_name.name

    @api.depends('child_ids')
    def _compute_total_coefficient(self):
        for record in self:
            if record.child_ids:
                total_coefficient = sum(o.coefficient for o in record.child_ids)
                record.total_coefficient = total_coefficient
            else:
                record.total_coefficient = 0

    @api.depends('total_coefficient')
    def _compute_last_child(self):
        for record in self:
            if record.total_coefficient > 0:
                record.last_child = False
            else:
                record.last_child = True

    @api.depends('parent_id')
    def _compute_course_ref(self):
        x = []
        for obj in self:
            if obj.parent_id:
                if obj.parent_id.matrix_id:
                    obj.parent_id.course_ref = obj.parent_id.matrix_id.id
                    x.append(obj)
        y = []
        for obj in x:
            SieMatrixParameter._create_children(obj.child_ids, y)
        for obj in y:
            x.append(obj)
        if x:
            for obj in x:
                if obj.parent_id:
                    obj.course_ref = obj.parent_id.course_ref
                else:
                    obj.course_ref = obj.matrix_id.id
        else:
            for obj in self:
                if obj.parent_id:
                    obj.course_ref = obj.parent_id.course_ref
                else:
                    obj.course_ref = obj.matrix_id.id

    @api.depends('parent_id', 'course_ref')
    def _compute_parent_ref(self):
        x = []
        for obj in self:
            if obj.parent_id:
                if obj.parent_id.matrix_id:
                    obj.parent_id.parent_ref = obj.parent_id.course_ref
                    x.append(obj)
        y = []
        for obj in x:
            SieMatrixParameter._create_children(obj.child_ids, y)
        for obj in y:
            x.append(obj)
        if x:
            for obj in x:
                if obj.parent_id:
                    obj.parent_ref = '%s-%s' % (obj.parent_id.parent_ref, obj.parent_id.param_name.code)
                else:
                    obj.parent_ref = obj.course_ref
        else:
            for obj in self:
                if obj.parent_id:
                    obj.parent_ref = '%s-%s' % (obj.parent_id.parent_ref, obj.parent_id.param_name.code)
                else:
                    obj.parent_ref = obj.course_ref

    @staticmethod
    def _create_children(child_ids, x):
        for child_id in child_ids:
            x.append(child_id)
        for child_id in child_ids:
            if not child_id.last_child:
                SieMatrixParameter._create_children(child_id.child_ids, x)
        return

    @api.onchange('total_coefficient')
    def _onchange_total_coefficient(self):
        for record in self:
            if record.total_coefficient > 0:
                record.last_child = False
                if record.total_coefficient > 1:
                    raise ValidationError("Sum of coefficients must be equal to 1")
            else:
                record.last_child = True

    @api.constrains('child_ids')
    def _check_coefficient(self):
        x =[]
        for obj in self:
            if obj.parent_id:
                if obj.parent_id.matrix_id:
                    x.append(obj)
        y=[]
        for obj in x:
            SieMatrixParameter._create_children( obj.child_ids, y)
        for obj in y:
            x.append(obj)
        for obj in reversed(x):
            if obj.child_ids:
                total = sum(record.coefficient for record in obj.child_ids)
                if str("%.3f" % total) != '1.000':
                    raise ValidationError("Sum of coefficients must be equal to 1, parameter: " + obj.name)
                else:
                    obj.last_child = False
            else:
                obj.last_child = True
