# -*- coding: utf-8 -*
import locale
from datetime import date, datetime

import pytz

from odoo import models, fields, api


def get_format_date():
    if date:
        locale.setlocale(locale.LC_TIME, "es_EC.utf-8")
        fecha = datetime.strptime(date, '%Y-%m-%d').strftime('%d de %B del %Y')
        return pytz.unicode(fecha.decode('UTF-8'))


class SieSubjectContent(models.Model):
    _name = 'sie.subject.content'
    _description = 'Subject Content'

    name = fields.Char(
        'Nombre',
        size=96,
        required=True
    )
    code = fields.Char(
        'Código',
        size=20,
        required=True
    )
    parent_id = fields.Many2one(
        'sie.subject.unit',
        'Área de conocimiento',
        ondelete='cascade'
    )
    faculty_ids = fields.Many2many(
        'sie.faculty',
        string='Docente',
        required=True,
        ondelete='restrict'
    )
    faculty_id = fields.Many2one(
        'sie.faculty',
        string='Docente principal',
        required=True,
        ondelete='restrict',
        domain="[('id', 'in', faculty_ids)]"
    )
    date_start = fields.Date('Fecha Inicio')
    date_end = fields.Date('Fecha Final')
    hours = fields.Integer('Horas')

    @api.onchange('name')
    def do_stuff(self):
        for record in self:
            if record.name:
                record.name = record.name.upper()

    def current_date(self):
        my_tz = pytz.timezone(self._context.get('tz') or 'UTC')
        return datetime.now(my_tz).strftime('Guayaquil, %d de %m/ del %Y')

    @api.model
    def create(self, val):
        record = super(SieSubjectContent, self).create(val)
        parent_id = self.env['sie.subject.unit'].search([('id', '=', record.parent_id.id)])
        parent_id.calculate_total_hours(record.hours)
        return record

    def write(self, vals):
        flag = super(SieSubjectContent, self).write(vals)
        for record in self:
            parent_id = self.env['sie.subject.unit'].search([('id', '=', record.parent_id.id)])
            parent_id.calculate_total_hours(record.hours)
        return flag
