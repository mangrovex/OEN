from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SieDirectionWorkStudent(models.Model):
    _name = 'sie.register.work.student'
    _description = 'Register work student'
    _order = 'last_name_1, last_name_2'

    name = fields.Char(
        string='Work ID',
        store=True
    )
    student_id = fields.Many2one(
        'sie.student',
        string='Student',
        ondelete='restrict',
        required=True,
        store=True
    )
    course_id = fields.Many2one(
        'sie.course',
        string='Course',
        ondelete='restrict'
    )
    register_work_id = fields.Many2one(
        'sie.register.work',
        string='Register Work'
    )
    enrollment_id = fields.Many2one(
        'sie.register.work.enrollment',
        string='enrollment',
        ondelete='cascade'
    )
    last_name_1 = fields.Char(
        compute='_compute_last_name',
        store=True
    )
    last_name_2 = fields.Char(
        compute='_compute_last_name',
        store=True
    )

    @api.depends('student_id')
    def _compute_last_name(self):
        for record in self:
            record.last_name_1 = record.student_id.last_name_1
            record.last_name_2 = record.student_id.last_name_2

    def unlink(self):
        for record in self:
            productivy_record = self.env['sie.productivity'].search(
                [('direction_work_enrollment_id', '=', record.register_work_id.id)])
            if productivy_record:
                raise ValidationError("Student with grates")
        return super(SieDirectionWorkStudent, self).unlink()
