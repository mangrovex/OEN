# -*- coding: utf-8 -*-

import logging
from operator import attrgetter

import icu

from odoo import _, models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


def set_data(course_id):
    module_ids = course_id.module_ids.filtered("plus_exec_hours")
    exec_hours = 0
    for module_id_running_hours in module_ids:
        exec_hours = exec_hours + module_id_running_hours.running_hours
    for module_id_running_hours in module_ids:
        if exec_hours > 0:
            coefficient = float(float(module_id_running_hours.running_hours) / float(exec_hours))
            module_id_running_hours.sudo().write({'coefficient': coefficient})
        # else:
        # raise ValidationError("Ingresar primero control de horas")
    course_id.sudo().write({'exec_hours': exec_hours})


class SieScore(models.Model):
    _name = 'sie.score'
    _description = 'Score'
    _rec_name = 'record_name'
    _inherit = ['mail.activity.mixin']

    name = fields.Char(
        string='Nombre',
        compute='_compute_name',
        store=True
    )
    notes = fields.Text(string='Notas')
    course_id = fields.Many2one(
        'sie.course',
        string='Course',
        domain="[('state', '=', 'running')]",
        ondelete='restrict',
        required=True
    )
    # , ('module_ids.faculty_id.user_id', '=', uid)
    module_id = fields.Many2one(
        'sie.module',
        string='Módulo',
        ondelete='restrict',
        domain="[('course_ids', '=' , course_id), ('state', '=' , 'r')]",
        required=False
    )
    parameter_id = fields.Many2one(
        'sie.matrix.parameter',
        string=u'Parámetro',
        ondelete='restrict',
        domain="['&', ('last_child', '=', True), '|', ('course_ref', '=',matrix_id), ('matrix_id', '=',matrix_id) ]",
        required=True
    )
    score_student_line = fields.One2many(
        'sie.score.student',
        'score_id',
        string='Notas de los Estudiantes',
        # domain="[('current_course', '=' , course_id)]",
    )
    state = fields.Selection(
        [
            ('draft', _('Draft')),
            ('published', _('Published')),
            ('for_review', _('For review')),
            ('approved', _('Approved')),
        ],
        string='Estado',
        default='draft'
    )
    parameter_name = fields.Char(
        compute='_compute_parameter_name'
    )
    teacher_id = fields.Many2one(
        'sie.faculty',
        string='Docente',
        store=True,
        ondelete='restrict'
    )
    matrix_id = fields.Many2one(
        "sie.matrix",
        compute='_compute_matrix',
        ondelete='restrict'
    )
    module_credits = fields.Integer(
        related='module_id.credits',
        string=u'Créditos'
    )
    record_name = fields.Char(compute='_compute_record_name')

    _sql_constraints = [
        ('name_uk', 'unique(name)', u'Registro debe ser único'),
    ]

    @api.constrains('module_credits', 'parameter_id')
    def _check_credits(self):
        for record in self:
            if record.module_credits < 2:
                if record.parameter_id:
                    if '004' in record.parameter_id.param_name.code:
                        raise Warning("Cannot score PRODUCTO DE LA UNIDAD, module only has one credit")

    @api.constrains('course_id')
    def _check_validator_score(self):
        for record in self:
            if record.course_id:
                name = ''
                final = ''
                if record.parameter_id:
                    name = record.parameter_id.param_name.code
                    final = record.parameter_id.parent_ref

    @api.onchange('course_id')
    def onchange_course_id(self):
        for record in self:
            students = []
            enrollment = self.env['sie.enrollment'].search([('course_id', '=', record.course_id.id)])
            student_ids = enrollment.student_ids.sorted(key=attrgetter('last_name', 'mother_name'))
            seq = 0
            for student in student_ids:
                if student.active:
                    seq += 1
                    data = {
                        'student_id': student.id,
                        'seq': seq,
                    }
                    students.append(data)
            record.score_student_line = self.env['sie.score.student'].create(students)

    @api.depends('course_id')
    def _compute_matrix(self):
        for record in self:
            if record.course_id:
                record.matrix_id = record.course_id.matrix_id
            else:
                record.matrix_id = ''

    @api.onchange('course_id')
    def _compute_teacher(self):
        for record in self:
            if record.course_id:
                teacher_id = self.env['sie.faculty'].search([('user_id', '=', self._uid)])
                if not teacher_id.id:
                    raise ValidationError('Usted no es un profesor ')
                elif record.course_id.assigned_officer_id == teacher_id:
                    record.teacher_id = teacher_id
                else:
                    raise ValidationError('Usted no es el profesor asignado al curso')

    @api.depends('parameter_id')
    def _compute_parameter_name(self):
        for record in self:
            if record.parameter_id:
                record.parameter_name = record.parameter_id.param_name.code
                # if '009' in record.parameter_id.parent_id.parent_ref:
                #     record.parameter_name = '009'
            else:
                record.parameter_name = '999'

    def get_course(self, record):
        course_id = self.sudo().env['sie.course'].search([('id', '=', record.course_id.id)])
        return course_id

    def action_publish(self):
        self.state = 'published'

    def action_reject(self):
        self.state = 'for review'

    def action_to_published(self):
        for record in self:
            module_ids = self.sudo().env['sie.score'].search(
                [('module_id', '=', record.module_id.id), ('state', '=', 'approved')])
            count = 0
            for obj_count in self:
                if obj_count.module_id == record.module_id:
                    count += 1
            if len(module_ids) == count:
                module_id = self.sudo().env['sie.module'].search([('id', '=', record.module_id.id)])
                module_id.sudo().write({'plus_exec_hours': False,
                                        'coefficient': 0})
            set_data(self.get_course(record))
            record.state = 'published'

    def action_approve(self):
        module_id = self.sudo().env['sie.module'].search([('id', '=', self.module_id.id)])
        module_id.sudo().write({'plus_exec_hours': True})
        set_data(self.get_course(self))
        self.state = 'approved'

    def unlink(self):
        unlink_ids = []
        for obj in self:
            name = ''
            final = ''
            if obj.parameter_id:
                name = obj.parameter_id.param_name.code
                final = obj.parameter_id.parent_ref
            module_id = self.sudo().env['sie.module'].search([('id', '=', obj.module_id.id)])
            module_ids = self.sudo().env['sie.score'].search([('module_id', '=', obj.module_id.id)])
            coefficient = module_id.sudo().coefficient - len(module_ids)
            module_id.sudo().write({'coefficient': coefficient})

            module_ids = self.sudo().env['sie.score'].search([('module_id', '=', obj.module_id.id)])
            # count_2 = self.search([('module_id','=',obj.module_id.id)])
            # count = len(self.search([('module_id','=',obj.module_id.id)]))
            count = 0
            for obj_count in self:
                if obj_count.module_id == obj.module_id:
                    count += 1
            if len(module_ids) == count:
                module_id = self.sudo().env['sie.module'].search([('id', '=', obj.module_id.id)])
                module_id.sudo().write({'plus_exec_hours': False})
            set_data(self.get_course(obj))
        for record in self:
            if record.state not in 'draft':
                raise ValidationError(_('You can not delete an record which was settled'))
            else:
                unlink_ids.append(record.id)
            if record.score_number:
                if not record.score_number == "1":
                    data = self.env['sie.score'].search(
                        [('course_id', '=', record.course_id.id), ('parameter_id', '=', record.parameter_id.id),
                         ('module_id', '=', record.module_id.id), ('teacher_id', '=', record.teacher_id.id)
                         ]
                    )
                    if data:
                        raise ValidationError("Debes borrar primero la nota " + str(int(record.score_number) + 1))
        return super(SieScore, self).unlink()

    @api.depends('module_id')
    def _compute_module_credits(self):
        for record in self:
            if record.module_id:
                record.module_credits = record.module_id.credits

    @api.depends('course_id', 'parameter_id', 'module_id', 'teacher_id')
    def _compute_name(self):
        for record in self:
            if record.parameter_name == '042':
                if record.course_id and record.parameter_id and record.teacher_id:
                    name = '%s,%s,%s' % (record.course_id.id, record.parameter_id.id, record.teacher_id.id)
                    record.name = name
                else:
                    record.name = ''
            else:
                if record.course_id and record.parameter_id and record.module_id and record.teacher_id:
                    name = '%s,%s,%s,%s' % (record.course_id.id, record.parameter_id.id,
                                            record.module_id.id, record.teacher_id.id)
                    record.name = name
                else:
                    record.name = ''

    @api.constrains('score_number')
    def _check_score(self):
        if self.score_number:
            if not self.score_number == "1":
                data = self.env['sie.score'].search(
                    [('course_id', '=', self.course_id.id), ('parameter_id', '=', self.parameter_id.id),
                     ('module_id', '=', self.module_id.id), ('teacher_id', '=', self.teacher_id.id)
                     ]
                )
                if not data:
                    raise ValidationError("Falta nota " + str(int(self.score_number) - 1))

    @api.depends('name')
    def _compute_record_name(self):
        for record in self:
            if record.parameter_id:
                record.record_name = record.parameter_id.name

    @api.model
    def create(self, vals):
        module_id = self.sudo().env['sie.module'].search([('id', '=', vals['module_id'])])
        module_id.sudo().write({'plus_exec_hours': True})
        course_id = self.sudo().env['sie.course'].search([('id', '=', vals['course_id'])])
        set_data(course_id)
        return super(SieScore, self).create(vals)

    def print_act(self):
        for record in self:
            return self.env['report'].get_action(record, 'openedunav_core_report.report_score_act')

    #
    # @api.model
    # def _needaction_domain_get(self):
    #     if self.env.user.groups_id.filtered(lambda r: r.id == self.env.ref('openedunav_core.group_statistician').id):
    #         return [('state', '=', 'published')]
    #     if self.env.user.groups_id.filtered(lambda r: r.id == self.env.ref('openedunav_core.group_faculty').id):
    #         return [('state', '=', 'for review')]
    #     return False

    def sort_by_name(self):
        for record in self:
            collator = icu.Collator.createInstance(icu.Locale('es'))
            # score_student_line = sorted(record.score_student_line,key=attrgetter('last_name',
            # 'mother_name','first_name','middle_name'),cmp=collator.compare)
            score_student_line = record.score_student_line.sorted(key=attrgetter('full_name'))
            seq = 0
            for student in score_student_line:
                seq += 1
                student.write({'seq': seq})

    def sort_by_score(self):
        for record in self:
            score_student_line = record.score_student_line.sorted(
                key=attrgetter('score'))
            seq = 0
            for student in score_student_line:
                seq += 1
                student.write({'seq': seq})
