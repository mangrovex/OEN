# -*- coding: utf-8 -*-
from odoo import models, fields, api
from operator import attrgetter
import logging


class ScoreWizard(models.TransientModel):
    _name = 'score.wizard'
    _description = 'Score'

    course_id = fields.Many2one('sie.course', string='Course', required=True)

    matrix_name = fields.Char(compute="_compute_matrix_name", store=True)
    selected_report = fields.Selection(string="Type",
                                       selection=[('F', 'Final'), ('FG', 'Final Guest'), ('S', 'Summary'),
                                                  ('D', 'Detail')],
                                       required=True)
    subject_id = fields.Many2one('sie.subject', string='Subject', ondelete='restrict',
                                 domain="[('course_id', '=', course_id)]")
    ordenar = fields.Selection(string='Ordenar por', selection=[('nombre', 'Nombre'), ('promedio', 'Promedio')])

    @api.one
    @api.depends('course_id')
    def _compute_matrix_name(self):
        if self.course_id:
            self.matrix_name = self.course_id.matrix_id.id

    @api.multi
    def print_report(self):
        url = '/web/aguena/report_score?' \
              '&course_id=%s' \
              '&report_type=%s' \
              '&subject_id=%s' \
              '&ordenar=%s' \
              % (self.course_id.id, self.selected_report, self.subject_id.id, self.ordenar)
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }
