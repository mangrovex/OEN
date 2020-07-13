# -*- coding: utf-8 -*
import locale
from datetime import date, datetime

import pytz

from odoo import models, fields, api


class SieSubjectContent(models.Model):
    _name = 'sie.subject.content'
    _description = 'Subject Content'

    name = fields.Char(
        'Nombre del Módulo',
        size=96,
        required=True
    )
    number_module = fields.Selection(
        [
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6', '6'),
            ('7', '7'),
            ('8', '8'),
            ('9', '9'),
            ('10', '10'),
            ('11', '11'),
            ('12', '12'),
            ('13', '13'),
            ('14', '14'),
            ('15', '15'),
            ('16', '16'),
            ('17', '17'),
            ('18', '18'),
            ('19', '19'),
            ('20', '20'),
        ],
        string='Módulo',
        required=True
    )
    subject_id = fields.Many2one('sie.subject')
    faculty_id = fields.Many2one(
        'sie.faculty',
        string='Docente',
        required=True,
        ondelete='restrict'
    )
    date_start = fields.Date('Fecha Inicio')
    date_end = fields.Date('Fecha Final')
    hours = fields.Integer('Horas Dictadas')
    score = fields.Float(u'Calificación')

    @api.onchange('name')
    def do_stuff(self):
        for record in self:
            if record.name:
                record.name = record.name.upper()

    def get_total_hours(self):
        total_hours = 0
        for content in self:
            total_hours += content.hours
        return total_hours

    def get_format_date(self):
        if date:
            locale.setlocale(locale.LC_TIME, "es_EC.utf-8")
            fecha = datetime.strptime(date, '%Y-%m-%d').strftime('%d de %B del %Y')
            return pytz.unicode(fecha.decode('UTF-8'))

    def current_date(self):
        my_tz = pytz.timezone(self._context.get('tz') or 'UTC')
        return datetime.now(my_tz).strftime('Guayaquil, %d de %m/ del %Y')

    def get_register_director(self, course):
        return self.env['sie.register.directors'].search([('course_id', '=', course.id)], limit=1)

    def get_statistician_name(self):
        register_director = self.get_register_director(self[0].subject_id.course_id)
        return register_director.statistician_id.full_name

    def get_statistician_grade(self):
        register_director = self.get_register_director(self[0].subject_id.course_id)
        return register_director.statistician_id.get_grade()

    def get_statistician_position(self):
        register_director = self.get_register_director(self[0].subject_id.course_id)
        return register_director.position_statistician

    def get_director_name(self):
        register_director = self.get_register_director(self[0].subject_id.course_id)
        return register_director.director_id.full_name

    def get_director_grade(self):
        register_director = self.get_register_director(self[0].subject_id.course_id)
        return register_director.director_id.get_grade()

    def get_director_position(self):
        register_director = self.get_register_director(self[0].subject_id.course_id)
        return register_director.position_director