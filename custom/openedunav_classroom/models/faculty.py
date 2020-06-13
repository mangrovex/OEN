# -*- coding: utf-8 -*

import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class SieFaculty(models.Model):
    _name = 'sie.faculty'
    _inherit = 'sie.faculty'

    director = fields.Boolean(string='Director')
    planta = fields.Boolean(string='Planta')
    division = fields.Boolean(string=u'División')
    evaluator = fields.Boolean(string='Evaluador')
    judge = fields.Boolean(string='Juez')
    professor = fields.Boolean('Profesor')
    statistician = fields.Boolean(string='Estadistico')
    register_work_ids = fields.Many2many('sie.register.work')
    subject_ids = fields.Many2many('sie.subject')

