# -*- coding: utf-8 -*-
from odoo import models, fields, api


class IngratorProductWizard(models.TransientModel):
    _name = 'report.integrator.product.wizard'
    _description = 'Report Integrator Product'

    course_id = fields.Many2one('sie.course', string='Course', required=True)

    parameter_id = fields.Many2one('sie.matrix.parameter', string='Parameter', ondelete='restrict')

    matrix_id = fields.Char(compute="_compute_matrix", store=True)
    selected_report = fields.Selection(string="Type", selection=[('S', 'Summary'), ('D', 'Detail')], required=True)
    judge_id = fields.Many2one("sie.faculty", string="Judge", domain="[('war_games_ids','=', war_games_id)]")
    war_games_id = fields.Many2one('sie.war.games', string='War Games',
                                   domain="[('course_id', '=', course_id)]")
    war_games_report = fields.Boolean(default=False)
    param_name_code = fields.Char(compute='_compute_param_name_code')
    ordenar = fields.Selection(string='Ordenar por', selection=[('nombre', 'Nombre'), ('promedio', 'Promedio')])
    direction_work_id = fields.Many2one('sie.register.work', string='Direction work',
                                        domain="[('course_id', '=', course_id), ('work_type', '=','direction')]")

    @api.one
    @api.depends('course_id')
    def _compute_matrix(self):
        if self.course_id:
            self.matrix_id = self.course_id.matrix_id.id

    @api.onchange('course_id')
    def _get_domain(self):
        if self.course_id:
            res = {}
            param_name = self.env['sie.param.name'].search([('code', '=', '013')])
            parameter = self.env['sie.matrix.parameter'].search(
                [('course_ref', '=', self.matrix_id), ('param_name', '=', param_name.id)])
            res['domain'] = {'parameter_id': [('parent_id', '=', parameter.id)]}
            return res

    @api.multi
    @api.depends('parameter_id')
    def _compute_param_name_code(self):
        if self.parameter_id:
            self.param_name_code = self.parameter_id.param_name.code

    @api.multi
    def print_report(self):

        url = '/web/aguena/report_integrator?' \
              '&course_id=%s' \
              '&report_type=%s' \
              '&parameter_id=%s' \
              '&war_games_report=%s' \
              '&war_games_id=%s' \
              '&judge_id=%s' \
              '&direction_work_id=%s' \
              '&ordenar=%s' \
              % (self.course_id.id, self.selected_report, self.parameter_id.id, self.war_games_report,
                 self.war_games_id.id,
                 self.judge_id.id, self.direction_work_id.id, self.ordenar)
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }
