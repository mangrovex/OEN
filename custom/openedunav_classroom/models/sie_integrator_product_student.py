from odoo import models, fields, api
from decimal import *


class SieIntegratorProductStudent(models.Model):
    _name = 'sie.integrator.product.student'
    _description = 'Student\'s Score Integrator Product'
    _order = 'full_name'

    name = fields.Char(
        string='ID',
        store=True)
    student_id = fields.Many2one(
        comodel_name='sie.student',
        string='Student',
        ondelete='restrict',
        required=True,
        store=True
    )
    score = fields.Char('Score')
    score_id = fields.Many2one(
        comodel_name='sie.integrator.product',
        string='Score Integrator Product ID',
        ondelete='cascade'
    )
    full_name = fields.Char(
        compute='_compute_full_name',
        store=True
    )
    last_name_1 = fields.Char(
        compute='_compute_last_name',
        store=True
    )
    last_name_2 = fields.Char(
        compute='_compute_last_name',
        store=True
    )

    @api.depends('student_id')
    def _compute_last_name(self):
        for record in self:
            record.last_name_1 = record.student_id.last_name_1
            record.last_name_2 = record.student_id.last_name_2

    @api.depends('student_id')
    def _compute_full_name(self):
        for record in self:
            record.full_name = record.student_id.full_name

    @api.onchange('score')
    def onchange_score(self):
        for record in self:
            if record.score:
                if '.' not in record.score:
                    data = record.score.replace(',', '.')
                else:
                    data = record.score
                score_data = str('%.3f' % Decimal(data))
                record.score = score_data.replace('.', ',')
