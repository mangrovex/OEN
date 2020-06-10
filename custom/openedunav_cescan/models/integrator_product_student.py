from odoo import models, fields, api
from decimal import *


class SieIntegratorProductStudent(models.Model):
    _name = 'sie.integrator.product.student'
    _description = 'Student\'s Score Integrator Product'

    name = fields.Char(string='ID', store=True)
    student_id = fields.Many2one(comodel_name='sie.student', string='Student', ondelete='restrict',
                                 required=True, store=True)
    score = fields.Char('Score')
    score_id = fields.Many2one(comodel_name='sie.integrator.product', string='Score Integrator Product ID',
                               ondelete='cascade')
    full_name = fields.Char(compute='_compute_full_name', store=True)
    last_name_1 = fields.Char(compute='_compute_last_name', store=True)
    last_name_2 = fields.Char(compute='_compute_last_name', store=True)

    _order = 'full_name'

    @api.one
    @api.depends('student_id')
    def _compute_last_name(self):
        self.last_name_1 = self.student_id.last_name_1
        self.last_name_2 = self.student_id.last_name_2

    @api.one
    @api.depends('student_id')
    def _compute_full_name(self):
        self.full_name = self.student_id.full_name

    @api.multi
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
