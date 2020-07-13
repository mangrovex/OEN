# -*- coding: utf-8 -*-

import time
import logging

from operator import attrgetter
from odoo import _, models, fields, api
# from .misc import SCORE_STATE, SCORE_NUMBER
import icu


_logger = logging.getLogger(__name__)


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
        domain="[('state', '=', 'running')]",# ",('subject_ids.faculty_id.user_id','=',uid)]",
        ondelete='restrict',
        required=True
    )
    subject_id = fields.Many2one(
        'sie.subject',
        string='Asignatura',
        ondelete='restrict',
        domain="["# "('faculty_id', '=', teacher_id),"
               "('course_id', '=', course_id),"
               "('state', '=', 'r')]",
        required=True
    )
    parameter_id = fields.Many2one(
        'sie.matrix.parameter',
        string=u'Parámetro',
        ondelete='restrict',
        domain="[('last_child', '=', True), "
               "('parent_ref', 'like', '002'),"
               "('course_ref', '=',matrix_id)]"
    )
    student_ids = fields.One2many(
        'sie.score.student',
        inverse_name='score_id',
        string='Estudiantes'
    )
    state = fields.Selection(
        [
            ('draft', _('Draft')),
            ('published', _('Published')),
            ('for review', _('For review')),
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
    subject_credits = fields.Integer(
        related='subject_id.credits',
        string=u'Créditos'
    )
    # quiz = fields.Selection(selection=[('is_quiz_p', 'Quiz Producto'),
    #                                    ('is_quiz_v', u'Quiz Verificación')],
    #                         string='Quiz')
    score_number = fields.Selection(
        [
            ('1', 'Note 1'),
            ('2', 'Note 2'),
            ('3', 'Note 3'),
            ('4', 'Note 4'),
            ('5', 'Note 5'),
            ('6', 'Note 6'),
            ('7', 'Note 7'),
            ('8', 'Note 8'),
            ('9', 'Note 9'),
            ('10', 'Note 10'),
            ('11', 'Note 11'),
            ('12', 'Note 12'),
            ('13', 'Note 13'),
            ('14', 'Note 14'),
            ('15', 'Note 15'),
            ('16', 'Note 16'),
            ('17', 'Note 17'),
        ],
        string='No. Noa'
    )
    record_name = fields.Char(compute='_compute_record_name')

    _sql_constraints = [
        ('name_uk', 'unique(name)', u'Registro debe ser único'),
    ]

    # @api.one
    # @api.constrains('subject_credits', 'parameter_id')
    # def _check_credits(self):
    #     if self.subject_credits < 2:
    #         if self.parameter_id:
    #             if '004' in self.parameter_id.param_name.code:
    #                 raise Warning("Cannot score PRODUCTO DE LA UNIDAD, subject only has one credit")
    #
    # @api.one
    # @api.constrains('course_id')
    # def _check_validator_score(self):
    #     if self.course_id:
    #         name = ''
    #         final = ''
    #         if self.parameter_id:
    #             name = self.parameter_id.param_name.code
    #             final = self.parameter_id.parent_ref
    #         if self.quiz == 'is_quiz_v' or '009' in final:
    #             flag = True
    #             validator_score_int = self.env['sie.subject'].search([('id', '=', self.subject_id.id)]).validator_score
    #             if self.quiz == 'is_quiz_v' and validator_score_int == 0:
    #                 validator_score = self.env['sie.subject'].search([('id', '=', self.subject_id.id)])
    #                 validator_score.sudo().write({'validator_score': 3})
    #                 flag = False
    #             if self.parameter_id:
    #                 if '010' in name:
    #                     validator_score_int = self.env['sie.subject'].search(
    #                         [('id', '=', self.subject_id.id)]).validator_score
    #                     validator_score = self.env['sie.subject'].search([('id', '=', self.subject_id.id)])
    #                     if validator_score_int == 1:
    #                         validator_score.sudo().write({'validator_score': 3})
    #                         flag = False
    #                     else:
    #                         if validator_score_int != 3 and validator_score_int != 2:
    #                             validator_score.sudo().write({'validator_score': 2})
    #                             flag = False
    #                 if '011' in name:
    #                     validator_score_int = self.env['sie.subject'].search(
    #                         [('id', '=', self.subject_id.id)]).validator_score
    #                     validator_score = self.env['sie.subject'].search([('id', '=', self.subject_id.id)])
    #                     if validator_score_int == 2:
    #                         validator_score.sudo().write({'validator_score': 3})
    #                         flag = False
    #                     else:
    #                         if validator_score_int != 3 and validator_score_int != 1:
    #                             validator_score.sudo().write({'validator_score': 1})
    #                             flag = False
    #             if flag:
    #                 if validator_score_int == 3:
    #                     raise Warning(" VERIFICACION FINAL is setted")
    #                 if validator_score_int == 2:
    #                     raise Warning("Wait for VERIFICACION FINAL E.O.")
    #                 if validator_score_int == 1:
    #                     raise Warning("Wait for VERIFICACION FINAL T.E.")
    #

    @api.onchange('course_id')
    def onchange_course_id(self):
        for record in self:
            students = []
            enrollment = record.env['sie.enrollment'].search([('course_id', '=', record.course_id.id)])
            # student_ids = enrollment.student_ids.sorted(key=attrgetter('last_name_1', 'last_name_2'))
            student_ids = enrollment.student_ids
            seq = 0
            for student in student_ids:
                if not student.inactive:
                    seq += 1
                    data = {
                        'student_id': student.id,
                        'seq':seq
                    }
                    students.append(data)
            record.student_ids = students
    #
    # @api.one
    # @api.depends('parameter_id')
    # def _compute_parameter_name(self):
    #     if self.parameter_id:
    #         self.parameter_name = self.parameter_id.param_name.code
    #         if '009' in self.parameter_id.parent_id.parent_ref:
    #             self.parameter_name = '009'
    #
    # @api.one
    # def action_publish(self):
    #     self.state = 'published'
    #
    # @api.one
    # def action_reject(self):
    #     self.state = 'for review'
    #
    # @api.one
    # def action_to_published(self):
    #     for obj in self:
    #         subject_ids = self.sudo().env['sie.score'].search(
    #             [('subject_id', '=', obj.subject_id.id), ('state', '=', 'approved')])
    #         count = 0;
    #         for obj_count in self:
    #             if obj_count.subject_id == obj.subject_id:
    #                 count += 1
    #         if len(subject_ids) == count:
    #             subject_id = self.sudo().env['sie.subject'].search([('id', '=', obj.subject_id.id)])
    #             subject_id.sudo().write({'plus_exec_hours': False,
    #                                      'coefficient': 0})
    #
    #         course_id = self.sudo().env['sie.course'].search([('id', '=', obj.course_id.id)])
    #         subject_ids = course_id.subject_ids.filtered("plus_exec_hours")
    #         exec_hours = 0
    #         for subject_id_running_hours in subject_ids:
    #             exec_hours = exec_hours + subject_id_running_hours.running_hours
    #         for subject_id_running_hours in subject_ids:
    #             if exec_hours == 0:
    #                 raise ValidationError("Ingresar primero control de horas")
    #             coefficient = float(float(subject_id_running_hours.running_hours) / float(exec_hours))
    #             subject_id_running_hours.sudo().write({'coefficient': coefficient})
    #         course_id.sudo().write({'exec_hours': exec_hours})
    #         obj.state = 'published'
    #
    # @api.one
    # def action_approve(self):
    #     self.state = 'approved'
    #     subject_id = self.sudo().env['sie.subject'].search([('id', '=', self.subject_id.id)])
    #     subject_id.sudo().write({'plus_exec_hours': True})
    #     course_id = self.sudo().env['sie.course'].search([('id', '=', self.course_id.id)])
    #     subject_ids = course_id.subject_ids.filtered("plus_exec_hours")
    #     exec_hours = 0
    #     for subject_id_running_hours in subject_ids:
    #         exec_hours = exec_hours + subject_id_running_hours.running_hours
    #     for subject_id_running_hours in subject_ids:
    #         if exec_hours == 0:
    #             raise ValidationError("Ingresar primero control de horas")
    #         coefficient = float(float(subject_id_running_hours.running_hours) / float(exec_hours))
    #         subject_id_running_hours.sudo().write({'coefficient': coefficient})
    #     course_id.sudo().write({'exec_hours': exec_hours})
    #
    # @api.multi
    # def unlink(self):
    #     unlink_ids = []
    #     for obj in self:
    #         name = ''
    #         final = ''
    #         if obj.parameter_id:
    #             name = obj.parameter_id.param_name.code
    #             final = obj.parameter_id.parent_ref
    #         if obj.quiz == 'is_quiz_v' or '009' in final:
    #             validator_score_int = self.env['sie.subject'].search([('id', '=', obj.subject_id.id)]).validator_score
    #             if obj.quiz == 'is_quiz_v':
    #                 validator_score = self.env['sie.subject'].search([('id', '=', obj.subject_id.id)])
    #                 validator_score.sudo().write({'validator_score': 0})
    #             if obj.parameter_id:
    #                 if '010' in name:
    #                     validator_score_int = self.env['sie.subject'].search(
    #                         [('id', '=', obj.subject_id.id)]).validator_score
    #                     validator_score = self.env['sie.subject'].search([('id', '=', obj.subject_id.id)])
    #                     if validator_score_int == 3:
    #                         validator_score.sudo().write({'validator_score': 1})
    #                     else:
    #                         if validator_score_int == 2:
    #                             validator_score.sudo().write({'validator_score': 0})
    #                 if '011' in name:
    #                     validator_score_int = self.env['sie.subject'].search(
    #                         [('id', '=', obj.subject_id.id)]).validator_score
    #                     validator_score = self.env['sie.subject'].search([('id', '=', obj.subject_id.id)])
    #                     if validator_score_int == 3:
    #                         validator_score.sudo().write({'validator_score': 2})
    #                     else:
    #                         if validator_score_int != 3 and validator_score_int == 1:
    #                             validator_score.sudo().write({'validator_score': 0})
    #
    #         subject_id = self.sudo().env['sie.subject'].search([('id', '=', obj.subject_id.id)])
    #         subject_ids = self.sudo().env['sie.score'].search([('subject_id', '=', obj.subject_id.id)])
    #         coefficient = subject_id.sudo().coefficient - len(subject_ids)
    #         subject_id.sudo().write({'coefficient': coefficient})
    #
    #         subject_ids = self.sudo().env['sie.score'].search([('subject_id', '=', obj.subject_id.id)])
    #         # count_2 = self.search([('subject_id','=',obj.subject_id.id)])
    #         # count = len(self.search([('subject_id','=',obj.subject_id.id)]))
    #         count = 0;
    #         for obj_count in self:
    #             if obj_count.subject_id == obj.subject_id:
    #                 count += 1
    #         if len(subject_ids) == count:
    #             subject_id = self.sudo().env['sie.subject'].search([('id', '=', obj.subject_id.id)])
    #             subject_id.sudo().write({'plus_exec_hours': False})
    #
    #         course_id = self.sudo().env['sie.course'].search([('id', '=', obj.course_id.id)])
    #         subject_ids = course_id.subject_ids.filtered("plus_exec_hours")
    #         exec_hours = 0
    #         for subject_id_running_hours in subject_ids:
    #             exec_hours = exec_hours + subject_id_running_hours.running_hours
    #         for subject_id_running_hours in subject_ids:
    #             coefficient = float(float(subject_id_running_hours.running_hours) / float(exec_hours))
    #             subject_id_running_hours.sudo().write({'coefficient': coefficient})
    #         course_id.sudo().write({'exec_hours': exec_hours})
    #     for record in self:
    #         if record.state not in 'draft':
    #             raise ValidationError(_('You can not delete an record which was settled'))
    #         else:
    #             unlink_ids.append(record.id)
    #         if record.score_number:
    #             if not record.score_number == "1":
    #                 data = self.env['sie.score'].search(
    #                     [('course_id', '=', record.course_id.id), ('parameter_id', '=', record.parameter_id.id),
    #                      ('subject_id', '=', record.subject_id.id), ('teacher_id', '=', record.teacher_id.id),
    #                      ('quiz', '=', record.quiz), ('score_number', '=', int(record.score_number) + 1)])
    #                 if data:
    #                     raise ValidationError("Debes borrar primero la nota " + str(int(record.score_number) + 1))
    #     return super(SieScore, self).unlink()

    @api.depends('course_id')
    def _compute_matrix(self):
        for record in self:
            if record.course_id:
                record.matrix_id = record.course_id.matrix_id
    #
    # @api.one
    # @api.onchange('course_id')
    # def _compute_teacher(self):
    #     if self.course_id:
    #         self.teacher_id = self.env['sie.faculty'].search([('user_id', '=', self._uid)])
    #
    # @api.one
    # @api.depends('subject_id')
    # def _compute_subject_credits(self):
    #     if self.subject_id:
    #         self.subject_credits = self.subject_id.credits

    @api.depends('course_id', 'parameter_id', 'subject_id', 'teacher_id', 'score_number')
    def _compute_name(self):
        for record in self:
            # name = '%s,%s,%s,%s,%s,%s' % (self.course_id.id, self.parameter_id.id,
            #                               self.subject_id.id, self.teacher_id.id, self.quiz,
            #                               self.score_number)
            name = '%s,%s,%s,%s,%s' % (record.course_id.id, record.parameter_id.id,
                                       record.subject_id.id, record.teacher_id.id,
                                       record.score_number)
            record.name = name

    # @api.one
    # @api.constrains('score_number')
    # def _check_score(self):
    #     if self.score_number:
    #         if not self.score_number == "1":
    #             data = self.env['sie.score'].search(
    #                 [('course_id', '=', self.course_id.id), ('parameter_id', '=', self.parameter_id.id),
    #                  ('subject_id', '=', self.subject_id.id), ('teacher_id', '=', self.teacher_id.id),
    #                  ('quiz', '=', self.quiz), ('score_number', '=', int(self.score_number) - 1)])
    #             if not data:
    #                 raise ValidationError("Falta nota " + str(int(self.score_number) - 1))
    #

    @api.depends('name')
    def _compute_record_name(self):
        for record in self:
            if record.parameter_id:
                record.record_name = record.parameter_id.name
            # if self.quiz == 'is_quiz_v':
            #     self.record_name = u'Verificación final examen'
            # if self.quiz == 'is_quiz_p':
            #     self.record_name = u'Producto de la unidad examen'
    #
    # # @api.model
    # # def create(self, vals):
    # #     subject_id = self.sudo().env['sie.subject'].search([('id', '=', vals['subject_id'])])
    # #     subject_id.sudo().write({'plus_exec_hours': True})
    # #     course_id = self.sudo().env['sie.course'].search([('id', '=', vals['course_id'])])
    # #     # subject_ids = self.sudo().env['sie.subject'].search([('plus_exec_hours', '=', True)])
    # #     subject_ids = course_id.subject_ids.filtered("plus_exec_hours")
    # #     exec_hours = 0
    # #     for subject_id_running_hours in subject_ids:
    # #         exec_hours = exec_hours + subject_id_running_hours.running_hours
    # #     for subject_id_running_hours in subject_ids:
    # #         coefficient = float(float(subject_id_running_hours.running_hours)/float(exec_hours))
    # #         subject_id_running_hours.sudo().write({'coefficient': coefficient})
    # #     course_id.sudo().write({'exec_hours': exec_hours})
    # #     return super(SieScore, self).create(vals)
    #
    # @api.multi
    # def print_act(self):
    #     return self.env['report'].get_action(self, 'openedunav_core_report.report_score_act')
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
             # student_ids = sorted(record.student_ids,key=attrgetter('last_name','mother_name','first_name','middle_name'),cmp=collator.compare)
             student_ids = sorted(record.student_ids,key=attrgetter('full_name'),cmp=collator.compare)
             seq = 0
             for student in student_ids:
                 seq += 1
                 student.write({'seq':seq})

    def sort_by_score(self):
        for record in self:
            student_ids = record.student_ids.sorted(
                key=attrgetter('score'))
            seq = 0
            for student in student_ids:
                seq += 1
                student.write({'seq': seq})
