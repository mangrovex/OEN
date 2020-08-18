# -*- coding: utf-8 -*
import time
import logging
from odoo import models, fields, api


class SieTimekeepingCalc(models.Model):
    _name = 'sie.timekeeping.calc'
    _description = 'Timekeeping Calc'

    name = fields.Char(
        string='Name',
        compute='_compute_name',
        store=True
    )
    course_id = fields.Many2one(
        'sie.course',
        string='Course',
        required=True,
        ondelete='restrict'
    )
    division = fields.Char(
        compute='_compute_division',
        string=u'División'
    )
    date_start_course = fields.Date(
        string='Fecha de Inicio'
    )
    date = fields.Date(
        string='Fecha del Reporte'
    )
    semana = fields.Char(string='Semana')
    line_ids = fields.One2many(
        'sie.timekeeping.line.calc',
        inverse_name='timeKeeping_line'
    )

    @api.depends('course_id', 'date')
    def _compute_display_name(self):
        for record in self:
            if record.course_id and record.date:
                create_date = time.strftime('%Y%m%d%H%M%S')
                name = '%s | %s ' % (record.course_id.name, create_date)
                record.name = name

    @api.depends('course_id')
    def _compute_division(self):
        for record in self:
            if record.course_id:
                record.division = record.course_id.enrollment

    @api.onchange('course_id')
    def onchange_course_id(self):
        sub1 = []
        a = self.env['sie.subject'].search([('course_id', '=', self.course_id.name)])
        sub = a
        for subject in sub:
            data = {
                'subject_id': subject.id
            }
            sub1.append(data)
        self.line_ids = sub1


