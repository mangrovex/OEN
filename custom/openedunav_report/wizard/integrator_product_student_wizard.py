# -*- coding: utf-8 -*-
from odoo import models, fields, api


class IntegratorProductStudentWizard(models.TransientModel):
    _name = 'report.integrator.product.student.wizard'
    _description = 'Report Integrator Product Student'

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
    parameter_id = fields.Many2one(
        'sie.matrix.parameter',
        string='Parameter',
        ondelete='restrict'
    )
    matrix_id = fields.Char(
        compute="_compute_matrix",
        store=True
    )
    selected_report = fields.Selection(
        string="Type",
        selection=[
            ('S', 'Summary'),
            ('D', 'Detail')
        ],
        required=True
    )
    judge_id = fields.Many2one(
        "sie.faculty",
        string="Judge",
        domain="[('war_games_ids','=', war_games_id)]"
    )
    war_games_id = fields.Many2one(
        'sie.war.games',
        string='War Games',
        domain="[('course_id', '=', course_id)]"
    )
    war_games_report = fields.Boolean(
        default=False
    )
    param_name_code = fields.Char(
        compute='_compute_param_name_code'
    )
    direction_work_id = fields.Many2one(
        'sie.register.work',
        string='Direction work',
        domain="[('course_id', '=', course_id), ('work_type', '=','direction')]"
    )

    @api.depends('course_id')
    def _compute_matrix(self):
        for record in self:
            if record.course_id:
                record.matrix_id = record.course_id.matrix_id.id

    @api.onchange('course_id')
    def _get_domain(self):
        if self.course_id:
            res = {}
            param_name = self.env['sie.param.name'].search([('code', '=', '013')])
            parameter = self.env['sie.matrix.parameter'].search(
                [('course_ref', '=', self.matrix_id), ('param_name', '=', param_name.id)])
            res['domain'] = {'parameter_id': [('parent_id', '=', parameter.id)]}
            return res

    @api.depends('parameter_id')
    def _compute_param_name_code(self):
        for record in self:
            if record.parameter_id:
                record.param_name_code = record.parameter_id.param_name.code

    def print_report(self):
        for record in self:
            student_id = record.env['sie.student'].search([('user_id', '=', record.env.uid)]).id
            url = '/web/sie/report_integrator?' \
                  '&course_id=%s' \
                  '&report_type=%s' \
                  '&parameter_id=%s' \
                  '&war_games_report=%s' \
                  '&war_games_id=%s' \
                  '&judge_id=%s' \
                  '&student_id=%s' \
                  '&direction_work_id=%s' \
                  % (record.course_id.id, record.selected_report, record.parameter_id.id, record.war_games_report,
                     record.war_games_id.id,
                     record.judge_id.id, student_id, record.direction_work_id.id)
            return {
                'type': 'ir.actions.act_url',
                'url': url,
                'target': 'self',
            }
