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
    # professor = fields.Boolean(compute='_compute_professor', store=True)
    statistician = fields.Boolean(string='Estadistico')
    register_work_ids = fields.Many2many('sie.register.work')
    subject_ids = fields.Many2many('sie.subject')

    def get_grade(self):
        for record in self:
            if record.grade_id and record.specialty_id:
                prefix = '%s-%s' % (record.grade_id.acronym, record.specialty_id.acronym)
            elif record.grade_id:
                prefix = '%s' % record.grade_id.acronym
            elif record.specialty_id:
                if record.title:
                    prefix = '%s' % record.title.acronym
                else:
                    prefix = ''
            else:
                if record.title:
                    prefix = '%s' % record.title.acronym
                else:
                    prefix = ''
            return prefix
