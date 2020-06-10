# -*- coding: utf-8 -*

from odoo import models, fields, api


class SieRegisterSubject(models.Model):
    _name = 'sie.register.subject'
    _description = 'Register Subject'

    name = fields.Char()
    topic = fields.Char(string='Tema', required=True)
    course_id = fields.Many2one(string='Curso', comodel_name='sie.course', required=True, ondelete='restrict')
    student_id = fields.Many2one(string='Estudiante', comodel_name='sie.student', required=True,
                                 domain="[('enrollment_ids', '=', enrollment_id)]", ondelete='restrict')
    faculty_ids = fields.Many2many('sie.faculty', string='Docentes', required=True,
                                   domain="[('evaluator', '=', True)]", ondelete='restrict')
    type = fields.Selection(string='Tipo',
                            selection=[('tesis', 'Tesis'), ('monografias', 'Monografias'),
                                       ('ensayos', 'Ensayos')], required=True)
    enrollment_id = fields.Integer(compute='_compute_enrollment')

    @api.one
    @api.depends('course_id')
    def _compute_enrollment(self):
        if self.course_id:
            self.enrollment_id = self.env['sie.enrollment'].search([('name', '=', self.course_id.name)]).id
