# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SieScoreStudent(models.Model):
    _name = 'sie.score.student'
    _description = 'Student\'s Score'
    _rec_name = 'student_id'
    _order = 'seq'

    student_id = fields.Many2one(
        'sie.student',
        string='Estudiante',
        ondelete='restrict',
        required=True,
        store=True
    )
    score = fields.Float(
        'Nota',
        digits='Score'
    )
    score_id = fields.Many2one(
        'sie.score',
        string='Score ID',
        ondelete='cascade'
    )
    first_name = fields.Char(
        "Primer Nombre",
        related='student_id.first_name',
        store=True
    )
    middle_name = fields.Char(
        "Segundo Nombre",
        related='student_id.middle_name',
        store=True
    )
    last_name = fields.Char(
        "Primer Apellido",
        related='student_id.last_name',
        store=True
    )
    mother_name = fields.Char(
        "Segundo Apellido",
        related='student_id.mother_name',
        store=True
    )
    full_name = fields.Char(
        "Nombre",
        related='student_id.full_name',
        store=True
    )
    seq = fields.Integer('No.')

    # _order = 'last_name,mother_name,first_name,middle_name'

    # @api.onchange('score')
    # def onchange_score(self):
    #     for record in self:
    #         if record.score:
    #             if '.' not in record.score:
    #                 data = record.score.replace(',', '.')
    #             else:
    #                 data = record.score
    #             score_data = str('%.3f' % Decimal(data))
    #             record.score = score_data.replace('.', ',')

    @api.constrains('score')
    def validate_score(self):
        for record in self:
            if record.score < 0.0 or record.score > 20:
                raise ValidationError(record.student_id.name + ' revisar Nota ' + str(record.score))

    @api.onchange('score')
    def onchange_score(self):
        for record in self:
            if record.score < 0.0 or record.score > 20:
                raise ValidationError(record.student_id.name + ' revisar Nota ' + str(record.score))

