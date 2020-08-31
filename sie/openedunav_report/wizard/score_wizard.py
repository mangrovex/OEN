# -*- coding: utf-8 -*-
from odoo import models, fields, api
from operator import attrgetter
import logging


class ScoreWizard(models.TransientModel):
    _name = 'score.wizard'
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
    selected_report = fields.Selection(
        string="Type",
        selection=[
            ('F', 'Final'),
            ('FG', 'Final Guest'),
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
    ordenar = fields.Selection(
        string='Ordenar por',
        selection=[
            ('nombre', 'Nombre'),
            ('promedio', 'Promedio')
        ]
    )

    @api.depends('course_id')
    def _compute_matrix_name(self):
        for record in self:
            if record.course_id:
                record.matrix_name = record.course_id.matrix_id.id

    def print_report(self):
        for record in self:
            url = '/web/aguena/report_score?' \
                  '&course_id=%s' \
                  '&report_type=%s' \
                  '&module_id=%s' \
                  '&ordenar=%s' \
                  % (record.course_id.id, record.selected_report, record.module_id.id, record.ordenar)
            return {
                'type': 'ir.actions.act_url',
                'url': url,
                'target': 'self',
            }
