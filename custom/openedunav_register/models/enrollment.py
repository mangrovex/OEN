# -*- coding: utf-8 -*

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, Warning


class SieEnrollment(models.Model):
    _name = 'sie.enrollment'
    _description = 'Enrollment'

    name = fields.Char(string='Nombre', compute='_compute_fullname', store=True)
    course_id = fields.Many2one('sie.course', string='Curso', ondelete='restrict', required=True,
                                domain=[('state', '=', 'planned')])
    student_ids = fields.Many2many('sie.student', string="Estudiantes", domain="[('in_course','=',False)]", store=True, ondelete='restrict')
    no_of_students = fields.Integer(string='No. de Estudiantes', store=True, compute='_compute_no_studentes')
    course_state = fields.Char(string='Estado del curso', compute='_compute_course_state')

    _sql_constraints = [
        ('name_uk', 'unique(name)', u'Nombre debe ser único')
    ]

    @api.multi
    @api.constrains('student_ids')
    def _check_student(self):
        for record in self:
            if not record.student_ids:
                raise ValidationError("Debe registrar al menos un estudiante")
                # else:
                #     # for record in self.student_ids:
                #     #     query = """ SELECT
                #     #             sie_course.name as course,
                #     #             sie_student.id as student,
                #     #             count(*) as total
                #     #         FROM
                #     #             sie_enrollment_sie_student_rel,
                #     #             public.sie_enrollment,
                #     #             public.sie_course,
                #     #             public.sie_student
                #     #         WHERE
                #     #             sie_enrollment_sie_student_rel.sie_enrollment_id = sie_enrollment.id AND
                #     #             sie_enrollment_sie_student_rel.sie_student_id = sie_student.id AND
                #     #             sie_enrollment.course_id = sie_course.id AND
                #     #             sie_enrollment_sie_student_rel.sie_student_id = %s AND
                #     #             sie_course.state = 'planned'
                #     #         GROUP BY course, student
                #     #     """
                #     #     self._cr.execute(query, (record.id,))
                #     #     for course, student, total in self._cr.fetchall():
                #     #         if total > 1:
                #     #             raise Warning(student + ' ya se encuentra enrrolado en el curso ' + course)
                #     #self.no_of_students = len(self.student_ids)
                #     pass

    @api.multi
    @api.depends('name', 'course_id', 'student_ids')
    def _compute_no_studentes(self):
        for record in self:
            if record.student_ids:
                record.no_of_students = len(record.student_ids)

    @api.multi
    @api.depends('course_id')
    def _compute_fullname(self):
        for record in self:
            if record.course_id:
                fullname = '%s' % record.course_id.name
                record.name = fullname

    @api.multi
    @api.depends('course_id')
    def _compute_course_state(self):
        for record in self:
            if record.course_id:
                record.course_state = record.course_id.state
            else:
                record.course_state = 'planned'

    @api.multi
    def unlink(self):
        unlink_ids = []
        for record in self:
            if record.course_id.state != 'planned':
                raise ValidationError(u'No puedes borrar el registro cuando el curso esta en ejecución')
            else:
                for students_id in record.student_ids:
                    student = self.env['sie.student'].search([('id', '=', students_id.id)])
                    student.sudo().write({'in_course': False})
                unlink_ids.append(record.id)
        return super(SieEnrollment, self).unlink()

    @api.model
    def create(self, vals):
        students_ids = vals['student_ids']
        for students_id in students_ids[0][2]:
            student = self.env['sie.student'].search([('id', '=', students_id)])
            student.sudo().write({'in_course': True,'current_course':vals['course_id']})
        return super(SieEnrollment, self).create(vals)

    @api.multi
    def write(self, vals):
        students_ids = vals['student_ids']
        for students_id in students_ids[0][2]:
            student = self.env['sie.student'].search([('id', '=', students_id)])
            student.sudo().write({'in_course': True})
        for student_old in self.student_ids:
            flag_remove = True
            for students_id in students_ids[0][2]:
                if student_old.id == students_id:
                    flag_remove = False
            if flag_remove:
                student_old_write = self.env['sie.student'].search([('id', '=', student_old.id)])
                student_old_write.sudo().write({'in_course': False})
        return super(SieEnrollment, self).write(vals)
