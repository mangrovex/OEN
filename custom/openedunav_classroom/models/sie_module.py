# -*- coding: utf-8 -*


import time
import re
import logging

from docutils.nodes import option

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class SieModule(models.Model):
    _name = 'sie.module'
    _description = 'Module'
    _order = 'code, shaft_id'

    name = fields.Char(
        'Nombre',
        size=96,
        required=True,
        search='_search_name'
    )
    code = fields.Char(
        'Código',
        search='_search_code',
        required=True
    )
    course_ids = fields.Many2many(
        'sie.course',
        string="Curso",
        store=True,
        ondelete='restrict'
    )
    shaft_id = fields.Many2one(
        'sie.training.shaft',
        string='Ejes de Estudios',
        ondelete='cascade',
        required=True
    )
    knowledge_ids = fields.One2many(
        'sie.knowledge',
        inverse_name='module_id',
        string='Áreas de Conocimiento',
        required=True
    )
    hours = fields.Integer(
        string='No. Horas',
        store=True
    )
    plus_exec_hours = fields.Integer(
        string='No. Horas ejecutadas',
        store=True
    )
    credits = fields.Integer(
        string=u'Créditos',
        store=True
    )
    number_module = fields.Integer(
        string='Número',
        required=True
    )
    coefficient = fields.Float(string="Coeficiente")
    running_hours = fields.Integer(string='Horas Ejecutadas')
    state = fields.Selection(
        string="Estado",
        selection=[
            ('p', 'Planificado'),
            ('r', u'Ejecucion'),
            ('f', 'Finalizado'),
        ],
        default='p',
        required=True
    )
    validator_score = fields.Integer(default=0)
    pre_requirement = fields.Text(string='Pre-requisitos')
    co_requisites = fields.Text(string='Co-requisitos')
    description = fields.Text(u'Descripción')
    competences = fields.Text('Competencias')
    competition_unit = fields.Text('Unidades de Competencia')
    element_of_competition = fields.Text('Elementos de Competicion')
    learning_outcome = fields.Text('Resultado de aprendizaje')
    contribution_of_the_module = fields.Text(u'Contribución del Módulo')
    additional_data = fields.Text(string=u'Información Adicional')

    _sql_constraints = [
        ('name_uk', 'unique(name)', u'Módulo debe ser único'),
        ('code_uk', 'unique(code)', u'Código debe ser único'),
    ]

    def calculate_total_hours(self, hours):
        for record in self:
            if record.knowledge_ids:
                record.hours = sum(record.total_hours for record in record.knowledge_ids)

    @api.onchange('hours')
    def calculate_credits(self):
        for record in self:
            if record.hours:
                record.credits = record.hours / 16

    def _search_name(self, operator, value):
        if operator == 'like':
            operator = 'ilike'
        if self.name:
            return [('name', operator, value)]

    def _search_code(self, operator, value):
        if operator == 'like':
            operator = 'ilike'
        if self.code:
            pattern = re.compile(r'^[0-9]+$')
            match = pattern.match(self.code)
            if match:
                if match.group() == self.code:
                    return [('code', operator, value)]
