# -*- coding: utf-8 -*
import time
import logging
from odoo import models, fields, api
from decimal import *
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError
from misc import CONTROL_STATE

_logger = logging.getLogger(__name__)

TYPE_LICENSE = [('permiso', 'PERMISO'),
                ('descanso', 'DESCANSO MEDICO')]


class SieLicense(models.Model):
    _name = 'sie.license'
    _description = 'News of students'

    name = fields.Char()
    course_id = fields.Many2one('sie.course', string='Curso', required=True, ondelete='restrict')
    student_id = fields.Many2one('sie.student', string='Estudiante', required=True,
                                 domain="[('current_course','=',course_id)]", ondelete='restrict')

    name_type = fields.Selection(TYPE_LICENSE, string='Tipo de Permiso', required=True)
    date = fields.Datetime(string='Fecha', required=True)
    hours = fields.Float(string=u'Número de horas', required=True,
                         help="Considerar que un dia laboral equivale a 8 horas", digits=dp.get_precision('Score'))
    notes = fields.Text(string=u'Descripción', required=True)
