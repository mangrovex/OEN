from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SieRegisterWorkEnrollment(models.Model):
    _name = 'sie.register.work.enrollment'
    _description = 'register work Enrollment'
    _order = 'name, course_id'

    name = fields.Char(
        string='Name',
        compute='_compute_fullname',
        store=True
    )
    course_id = fields.Many2one(
        'sie.course',
        string='Course',
        ondelete='restrict',
        required=True,
        domain=[('state', '!=', 'finalized')]
    )
    register_work_id = fields.Many2one(
        'sie.register.work',
        string='Register work',
        ondelete='restrict',
        required=True,
        domain="[('course_id', '=', course_id)]"
    )
    student_ids = fields.One2many(
        'sie.register.work.student',
        inverse_name='enrollment_id',
        store=True, ondelete='cascade'
    )
    group_name = fields.Char(
        String='Group Name',
        required=True
    )

    _sql_constraints = [
        ('name_uk', 'unique(name, course_id)', 'Classroom must be unique per course'),
    ]

    @api.constrains('student_ids')
    def _check_student(self):
        for record in self:
            if len(record.student_ids) == 0:
                raise ValidationError(_("Must enroll at least one student"))

    @api.depends('course_id', 'register_work_id', 'group_name')
    def _compute_fullname(self):
        for record in self:
            if record.course_id:
                fullname = '%s-%s-%s' % (record.register_work_id.work_name, record.course_id.name, record.group_name)
                record.name = fullname

    @api.onchange('register_work_id')
    def onchange_register_work_id(self):
        students = []
        count = 0
        enrollment = self.env['sie.enrollment'].search([('course_id', '=', self.course_id.id)])
        studends_register = self.env['sie.register.work.student']. \
            search([('register_work_id', '=', self.register_work_id.id)])
        for student in enrollment.student_ids:
            for student_register in studends_register:
                if student.identification_id == student_register.name:
                    count += 1
            if count == 0:
                data = {
                    'name': student.identification_id,
                    'student_id': student.id,
                    'course_id': self.course_id.id,
                    'register_work_id': self.register_work_id.id,
                }
                students.append(data)
            count = 0
        self.student_ids = students

    @api.depends('group_name')
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, '%s' % record.group_name))
        return result
