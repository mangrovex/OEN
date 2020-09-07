# -*- coding: utf-8 -*-

import logging
from operator import attrgetter

import icu

from odoo import _, models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SieScoreContent(models.Model):
    _name = 'sie.score.content'
    _description = 'Essential content'
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
    knowledge_id = fields.Many2one(
        'sie.knowledge',
        string=u'Àrea de conocimiento',
        ondelete='restrict',
        domain="[('module_id', '=',module_id) ]",
        required=True
    )
    content_id = fields.Many2one(
        'sie.content',
        string=u'Contenido imprescindible',
        ondelete='restrict',
        domain="[('knowledge_id', '=',knowledge_id) ]",
        required=True
    )
    score_content_student_line = fields.One2many(
        'sie.score.content.student',
        'score_content_id',
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
    content_name = fields.Char(
        compute='_compute_content_name'
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
    record_name = fields.Char(compute='_compute_record_name')

    _sql_constraints = [
        ('name_uk', 'unique(name)', u'Registro debe ser único'),
    ]

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
            record.score_content_student_line = self.env['sie.score.content.student'].create(students)

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

    @api.depends('content_id')
    def _compute_content_name(self):
        for record in self:
            if record.content_id:
                record.content_name = record.content_id.code
            else:
                record.content_name = '999'

    def get_course(self, record):
        course_id = self.sudo().env['sie.course'].search([('id', '=', record.course_id.id)])
        return course_id

    def action_publish(self):
        self.state = 'published'

    def action_reject(self):
        self.state = 'draft'

    def action_for_review(self):
        self.state = 'for_review'

    def action_approve(self):
        self.state = 'approved'

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
            record.state = 'published'

    # def unlink(self):
    #     unlink_ids = []
    #     for obj in self:
    #         name = ''
    #         final = ''
    #         if obj.parameter_id:
    #             name = obj.parameter_id.param_name.code
    #             final = obj.parameter_id.parent_ref
    #         module_id = self.sudo().env['sie.module'].search([('id', '=', obj.module_id.id)])
    #         module_ids = self.sudo().env['sie.score'].search([('module_id', '=', obj.module_id.id)])
    #         coefficient = module_id.sudo().coefficient - len(module_ids)
    #         module_id.sudo().write({'coefficient': coefficient})
    #
    #         module_ids = self.sudo().env['sie.score'].search([('module_id', '=', obj.module_id.id)])
    #         # count_2 = self.search([('module_id','=',obj.module_id.id)])
    #         # count = len(self.search([('module_id','=',obj.module_id.id)]))
    #         count = 0
    #         for obj_count in self:
    #             if obj_count.module_id == obj.module_id:
    #                 count += 1
    #         if len(module_ids) == count:
    #             module_id = self.sudo().env['sie.module'].search([('id', '=', obj.module_id.id)])
    #             module_id.sudo().write({'plus_exec_hours': False})
    #     for record in self:
    #         if record.state not in 'draft':
    #             raise ValidationError(_('You can not delete an record which was settled'))
    #         else:
    #             unlink_ids.append(record.id)
    #         if record.score_number:
    #             if not record.score_number == "1":
    #                 data = self.env['sie.score'].search(
    #                     [('course_id', '=', record.course_id.id), ('parameter_id', '=', record.parameter_id.id),
    #                      ('module_id', '=', record.module_id.id), ('teacher_id', '=', record.teacher_id.id)
    #                      ]
    #                 )
    #                 if data:
    #                     raise ValidationError("Debes borrar primero la nota " + str(int(record.score_number) + 1))
    #     return super(SieScoreContent, self).unlink()

    @api.depends('course_id', 'knowledge_id', 'module_id', 'teacher_id', 'content_id')
    def _compute_name(self):
        for record in self:
            if record.course_id and record.module_id and record.knowledge_id and record.content_id and record.teacher_id:
                name = '%s,%s,%s,%s,%s' % (record.course_id.id, record.module_id.id, record.knowledge_id.id,
                                           record.content_id.id, record.teacher_id.id)
                record.name = name
            else:
                record.name = ''

    @api.depends('name')
    def _compute_record_name(self):
        for record in self:
            if record.content_id:
                record.record_name = record.content_id.name

    def print_act(self):
        for record in self:
            return self.env['report'].get_action(record, 'openedunav_core_report.report_score_content_act')

    def sort_by_name(self):
        for record in self:
            collator = icu.Collator.createInstance(icu.Locale('es'))
            # score_student_line = sorted(record.score_student_line,key=attrgetter('last_name',
            # 'mother_name','first_name','middle_name'),cmp=collator.compare)
            score_content_student_line = record.score_content_student_line.sorted(key=attrgetter('full_name'))
            seq = 0
            for student in score_content_student_line:
                seq += 1
                student.write({'seq': seq})

    def sort_by_score_content(self):
        for record in self:
            score_content_student_line = record.score_content_student_line.sorted(
                key=attrgetter('score'))
            seq = 0
            for student in score_content_student_line:
                seq += 1
                student.write({'seq': seq})
