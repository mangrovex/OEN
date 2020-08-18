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

    course_id = fields.Many2one(
        'sie.course',
        domain=_get_course_domain,
        string='Course',
        required=True
    )
    matrix_name = fields.Char(
        compute="_compute_matrix_name",
        store=True
    )
    selected_report = fields.Selection(
        string="Type",
        selection=[
            ('F', 'Final'),
            ('S', 'Summary'),
            ('D', 'Detail')
        ],
        required=True
    )
    module_id = fields.Many2one(
        'sie.module',
        string='module',
        ondelete='restrict',
        domain="[('course_id', '=', course_id)]"
    )

    @api.depends('course_id')
    def _compute_matrix_name(self):
        for record in self:
            if record.course_id:
                record.matrix_name = record.course_id.matrix_id.id

    def print_report(self):
        for record in self:
            student_id = record.env['sie.student'].search([('user_id', '=', record.env.uid)]).id
            url = '/web/aguena/report_score?' \
                  '&course_id=%s' \
                  '&report_type=%s' \
                  '&module_id=%s' \
                  '&student_id=%s' \
                  % (record.course_id.id, record.selected_report, record.module_id.id, student_id)
            return {
                'type': 'ir.actions.act_url',
                'url': url,
                'target': 'self',
            }
