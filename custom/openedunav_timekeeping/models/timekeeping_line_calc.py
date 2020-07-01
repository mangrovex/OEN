# -*- coding: utf-8 -*
from odoo import models, fields, api


class SieTimekeepingLineCalc(models.Model):
    _name = 'sie.timekeeping.line.calc'
    _description = 'Timekeeping Line Calc'

    # _rec_name = "subject_id"
    # subject_id = fields.Many2one('sie.subject', string='Materia', required=True,
    #                              domain="[('course_id', '=', course_id),('state', '=', 'r')]", ondelete='restrict')
    subject_id = fields.Many2one(
        'sie.subject',
        string='Materia',
        required=True,
        ondelete='restrict'
    )
    timeKeeping_line = fields.Many2one(
        'sie.timekeeping.calc',
        ondelete='cascade'
    )
    program_hours = fields.Integer(
        string='Horas Programadas'
    )
    program_hours_week = fields.Integer(
        string='Horas Programadas en la Semana'
    )
    worked_hours_week = fields.Integer(
        string='Horas Ejecutadas en la Semana'
    )
    worked_hours = fields.Integer(
        string='Horas Ejecutadas'
    )
    hours_to_run = fields.Integer(
        string='Horas por Ejecutar'
    )
    advance = fields.Integer(
        string='Porcentaje de Avance'
    )
