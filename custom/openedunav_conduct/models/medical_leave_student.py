from odoo import models, fields


class SieMedicalLeaveStudent(models.Model):
    _name = 'sie.medical.leave.student'
    _description = 'Student\'s Medical'

    name = fields.Char(string='ID', store=True)
    student_id = fields.Many2one(comodel_name='sie.student', string='Student', ondelete='restrict', required=True,
                                 store=True)
