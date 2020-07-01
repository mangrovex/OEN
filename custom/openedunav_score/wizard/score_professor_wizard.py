# -*- coding: utf-8 -*-
from odoo import models, fields, api
from operator import attrgetter
import logging


class ScoreProfessorWizard(models.TransientModel):
    _name = 'score.professor.wizard'
    _description = 'Score'

    course_id = fields.Many2one(
        'sie.course',
        string='Course',
        required=True
    )
    matrix_name = fields.Char(
        compute="_compute_matrix_name",
        store=True
    )
    subject_id = fields.Many2one(
        'sie.subject',
        string='Subject',
        ondelete='restrict',
        required=True,
        domain="[('course_id', '=', course_id),('faculty_id.user_id','=',uid)]"
    )

    @api.depends('course_id')
    def _compute_matrix_name(self):
        for record in self:
            if record.course_id:
                record.matrix_name = record.course_id.matrix_id.id
                record.subject_id = None

    def print_report(self):
        for record in self:
            url = '/web/aguena/report_score?' \
                  '&course_id=%s' \
                  '&report_type=D' \
                  '&subject_id=%s' \
                  '&ordenar=nombre' \
                  % (record.course_id.id, record.subject_id.id)
            return {
                'type': 'ir.actions.act_url',
                'url': url,
                'target': 'self',
            }
