# -*- coding: utf-8 -*
from odoo import models, fields, api

TYPE_NEWS = [('puntualidad', 'PUNTUALIDAD'),
             ('presencia_personal', 'PRESENCIA PERSONAL'),
             ('conservacion_areas', 'CONSERVACION AREAS ASIGNADAS')]


class SieNews(models.Model):
    _name = 'sie.news'
    _description = 'News of students'

    name = fields.Char()
    course_id = fields.Many2one('sie.course', string='Curso', required=True, ondelete='restrict')
    student_id = fields.Many2one('sie.student', string='Estudiante', required=True,
                                 domain="[('current_course','=',course_id)]", ondelete='restrict')

    name_type = fields.Selection(TYPE_NEWS, string="Tipo de Novedades", required=True)
    date = fields.Datetime(string='Fecha', required=True)
    notes = fields.Text(string=u'Descripción', required=True)