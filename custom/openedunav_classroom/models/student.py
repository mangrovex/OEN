# -*- coding: utf-8 -*

import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class SieStudent(models.Model):
    _name = 'sie.student'
    _inherit = 'sie.student'

    enrollment_ids = fields.Many2many('sie.enrollment',string="Cursos Registrados")
    in_course = fields.Boolean(default=False, string="En curso?")
    current_course = fields.Many2one('sie.course', string="Curso Actual")
