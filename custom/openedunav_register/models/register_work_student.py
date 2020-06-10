from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SieDirectionWorkStudent(models.Model):
    _name = 'sie.register.work.student'
    _description = 'Register work student'

    name = fields.Char(string='ID', store=True)
    student_id = fields.Many2one('sie.student', string='Student',
                                 ondelete='restrict', required=True, store=True)
    course_id = fields.Many2one('sie.course', string='Course', ondelete='restrict')
    register_work_id = fields.Many2one('sie.register.work', string='Register Work')
    enrollment_id = fields.Many2one('sie.register.work.enrollment', string='enrollment', ondelete='cascade')
    last_name_1 = fields.Char(compute='_compute_last_name', store=True)
    last_name_2 = fields.Char(compute='_compute_last_name', store=True)

    _order = 'last_name_1, last_name_2'

    @api.one
    @api.depends('student_id')
    def _compute_last_name(self):
        self.last_name_1 = self.student_id.last_name_1
        self.last_name_2 = self.student_id.last_name_2

    @api.multi
    def unlink(self):
        for obj in self:
            productivy = self.env['sie.productivity'].search(
                [('direction_work_enrollment_id', '=', obj.register_work_id.id)])
            if productivy:
                raise ValidationError("Student with grates")

        return super(SieDirectionWorkStudent, self).unlink()
