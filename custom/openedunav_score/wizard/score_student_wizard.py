# -*- coding: utf-8 -*-
from odoo import models, fields, api
from operator import attrgetter
import logging


class ScoreStudentWizard(models.TransientModel):
    _name = 'score.student.wizard'
    _description = 'Score Student'

    @api.model
    def _get_course_domain(self):
        student_id = self.env['sie.student'].search([('user_id', '=', self.env.uid)]).id
        enrollment_ids = self.env['sie.enrollment'].search([('student_ids', '=', student_id)])
        course_ids = []
        for enrollment_id in enrollment_ids:
            course_ids.append(int(enrollment_id.course_id.id))
        return [('id', '=', course_ids)]

    course_id = fields.Many2one('sie.course', domain=_get_course_domain, string='Course', required=True)

    matrix_name = fields.Char(compute="_compute_matrix_name", store=True)
    selected_report = fields.Selection(string="Type", selection=[('F', 'Final'), ('S', 'Summary'), ('D', 'Detail')],
                                       required=True)
    subject_id = fields.Many2one('sie.subject', string='Subject', ondelete='restrict',
                                 domain="[('course_id', '=', course_id)]")

    @api.one
    @api.depends('course_id')
    def _compute_matrix_name(self):
        if self.course_id:
            self.matrix_name = self.course_id.matrix_id.id

    @api.multi
    def print_report(self):
        student_id = self.env['sie.student'].search([('user_id', '=', self.env.uid)]).id
        url = '/web/aguena/report_score?' \
              '&course_id=%s' \
              '&report_type=%s' \
              '&subject_id=%s' \
              '&student_id=%s' \
              % (self.course_id.id, self.selected_report, self.subject_id.id, student_id)
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }
