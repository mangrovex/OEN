# -*- coding: utf-8 -*


import time
import re
import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

SUBJECT_TYPE = [('common','Asignaturas comunes'),('professional',u'Capacitación Profesional')]


class SieSubject(models.Model):
    _name = 'sie.subject'
    _description = 'Subject'

    @api.model
    def _get_teacher_domain(self):
        id = self.env.ref('openedunav_school.group_faculty').id
        return [('user_id.groups_id', '=', id)]

    name = fields.Char(u'Módulo', size=96, required=True, search='_search_name')
    code = fields.Char(u'Código', search='_search_code', required=True)

    course_id = fields.Many2many('sie.course', string="Curso", store=True)
    version = fields.Float(u'Versión', digits=(2, 1), required=True, default=1.0)
    last_review = fields.Date(u'Última Revisión', readonly=True, default=time.strftime('%Y-%m-%d'))
    senescyt_code = fields.Char(u'Código SENESCYT', size=64, search='_search_senescyt_code')
    shaft_id = fields.Many2one('sie.training.shaft', string='Ejes de Estudios', ondelete='set null',
                               required=True)

    unit_ids = fields.One2many('sie.subject.unit', inverse_name='subject_id',
                               string='Unidades de Aprendizaje', required=True)
    hours = fields.Integer(compute='_compute', string='No. Horas', store=True)
    credits = fields.Integer(compute='_compute', string=u'Créditos', store=True)
    acronym = fields.Char(string='Acronimo', required=True)
    coefficient = fields.Float(string="Coeficiente")
    running_hours = fields.Integer(string='Horas Ejecutadas')
    start_date = fields.Date(string='Fecha Inicio')
    end_date = fields.Date(string='Fecha Fin')
    state = fields.Selection(string="Estado", selection=[('p', 'Planificado'),
                                                        ('r', u'Ejecucion'), ('f', 'Finalizado'), ],
                             default='p', required=True)
    faculty_id = fields.Many2one('sie.faculty', string='Docente', required=True,
                                 ondelete='restrict')

    plus_exec_hours = fields.Boolean()
    validator_score = fields.Integer(default=0)
    subject_type = fields.Selection(SUBJECT_TYPE,string="Tipo de asignatura")

    pre_requirement = fields.Text(string='Pre-requisitos')
    co_requisites = fields.Text(string='Co-requisitos')
    description = fields.Text(u'Descripción')
    competences = fields.Text('Competencias')
    competition_unit = fields.Text('Unidades de Competencia')
    element_of_competition = fields.Text('Elementos de Competicion')
    learning_outcome = fields.Text('Resultado de aprendizaje')
    contribution_of_the_subject = fields.Text(u'Contribución de la Materia')
    additional_data = fields.Text(string=u'Información Adicional')

    subject_content_ids = fields.One2many('sie.subject.content', inverse_name='subject_id')

    _order = 'code, shaft_id'

    _sql_constraints = [
        ('subject_uk', 'unique(name, senescyt_code, version)', u'Asignatura debe ser unica'),
        ('code_uk', 'unique(code)', u'Código debe ser único'),
        ('version_ck', 'check(version >= 1)', u'La versión debe ser mayor a 1'),
    ]

    @api.multi
    @api.depends('unit_ids')
    def _compute(self):
        for record in self:
            if record.unit_ids:
                record.hours = sum(record.hours for record in record.unit_ids)
                record.credits = record.hours / 16
                _logger.info(record.credits)

    @api.multi
    @api.depends('name', 'version', 'senescyt_code')
    def _compute_display_name(self):
        for record in self:
            record.display_name = '%s (v%.1f)' % (record.name, record.version)
            if record.senescyt_code:
                record.display_name = '%s [%s]' % (record.display_name, record.senescyt_code)

    def _search_name(self, operator, value):
        if operator == 'like':
            operator = 'ilike'
        if self.name:
            return [('name', operator, value)]

    def _search_code(self, operator, value):
        if operator == 'like':
            operator = 'ilike'
        if self.code:
            pattern = re.compile(r'^[0-9]+$')
            match = pattern.match(self.code)
            if match:
                if match.group() == self.code:
                    return [('code', operator, value)]

    def _search_senescyt_code(self, operator, value):
        if operator == 'like':
            operator = 'ilike'
        if self.senescyt_code:
            pattern = re.compile(r'^[0-9]+$')
            match = pattern.match(self.senescyt_code)
            if match:
                if match.group() == self.senescyt_code:
                    return [('senescyt_code', operator, value)]

    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        for record in self:
            default = dict(default or {})
            copied_count = self.search_count([('code', '=like', u"Copy of {}%".format(record.code))])
            if not copied_count:
                new_code = u"Copy of {}".format(record.code)
            else:
                new_code = u"Copy of {} ({})".format(record.code, copied_count)
            version_count = record.version
            if not version_count:
                new_version = 1
            else:
                new_version = version_count + 0.1
            # new_units_ids.append(new_unit.id)
            # default['unit_ids'] = (0, 0,  new_unit)
            # default['unit_ids'] = new_units_ids
            default['course_id'] = None
            default['version'] = new_version
            default['code'] = new_code
            new_subject = super(SieSubject, self).copy(default)
            units_ids = self.env['sie.subject.unit'].search([('subject_id', '=', record.id)])
            new_units_ids = self.env['sie.subject.unit']
            for unit in units_ids:
                new_unit = new_units_ids.create({'name': unit.name,
                                                 'number': unit.number,
                                                 'hours': unit.hours,
                                                 'subject_id': new_subject.id,
                                                 'last_child': unit.last_child})
                SieSubject._create_children(self, unit, new_unit)
            return new_subject

    @staticmethod
    def _create_children(self, unit, new_unit):
        if unit.last_child:
            return
        new_unit_ids = self.env['sie.subject.unit']
        for new_unit_child in unit.child_ids:
            new = new_unit_ids.create({'name': new_unit_child.name,
                                       'number': new_unit_child.number,
                                       'parent_id': new_unit.id,
                                       'hours': new_unit_child.hours,
                                       'last_child': new_unit.last_child})
            if not new_unit_child.last_child:
                SieSubject._create_children(self, new_unit_child, new)
        return

    @api.multi
    @api.onchange('name')
    def do_stuff(self):
        for record in self:
            if record.name:
                record.name = record.name.upper()

    @api.multi
    @api.onchange('course_id')
    def _teacher_id_domain(self):
        for record in self:
            if record.course_id and record.rol:
                res = {}
                domain = [('last_child', '=', True), ('parent_ref', 'like', '025'),
                          ('course_ref', '=', self.course_id.matrix_id.id)]
                param_name = []
                if record.rol == '029' or record.is_professor:
                    param_name_id = self.env['sie.param.name']. \
                        search([('code', '=', '029')]).id
                    # parameter_id = self.env['sie.matrix.parameter'].\
                    #     search([('last_child', '=', True), ('parent_ref', 'like', '025'),
                    #             ('param_name', '=', param_name.id),
                    #             ('course_ref', '=', self.course_id.matrix_id.id)])
                    param_name.append(int(param_name_id))
                    # domain = domain + [('param_name', '=', param_name.id)]
                if record.rol == '030':
                    param_name_id = record.env['sie.param.name']. \
                        search([('code', '=', '030')]).id
                    # parameter_id = self.env['sie.matrix.parameter'].\
                    #     search([('last_child', '=', True), ('parent_ref', 'like', '025'),
                    #             ('param_name', '=', param_name.id),
                    #             ('course_ref', '=', self.course_id.matrix_id.id)])
                    param_name.append(int(param_name_id))
                    # domain = domain + [('param_name', '=', param_name.id)]
                if record.rol == '026':
                    param_name_id = self.env['sie.param.name']. \
                        search([('code', '=', '026')]).id
                    # parameter_id = self.env['sie.matrix.parameter'].\
                    #     search([('last_child', '=', True), ('parent_ref', 'like', '025'),
                    #             ('param_name', '=', param_name.id),
                    #             ('course_ref', '=', self.course_id.matrix_id.id)])
                    param_name.append(int(param_name_id))
                    # domain = domain + [('param_name', '=', param_name.id)]
                if record.rol == '028':
                    param_name_id = self.env['sie.param.name']. \
                        search([('code', '=', '028')]).id
                    # parameter_id = self.env['sie.matrix.parameter'].\
                    #     search([('last_child', '=', True), ('parent_ref', 'like', '025'),
                    #             ('param_name', '=', param_name.id),
                    #             ('course_ref', '=', self.course_id.matrix_id.id)])
                    param_name.append(int(param_name_id))
                    # domain = domain + [('param_name', '=', param_name.id)]
                if record.rol == '027':
                    param_name_id = self.env['sie.param.name']. \
                        search([('code', '=', '027')]).id
                    # parameter_id = self.env['sie.matrix.parameter'].\
                    #     search([('last_child', '=', True), ('parent_ref', 'like', '025'),
                    #             ('param_name', '=', param_name.id),
                    #             ('course_ref', '=', self.course_id.matrix_id.id)])
                    param_name.append(int(param_name_id))
                    # domain = domain + [('param_name', '=', param_name.id)]
                domain = domain + [('param_name', '=', param_name)]
                res['domain'] = {'teacher_id': domain}
                return res
