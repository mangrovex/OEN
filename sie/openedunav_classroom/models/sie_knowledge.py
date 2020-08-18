# -*- coding: utf-8 -*
import logging

from odoo import models, fields, api
_logger = logging.getLogger(__name__)


class SieKnowledge (models.Model):
    _name = 'sie.knowledge'
    _description = 'Knowledge Area'

    name = fields.Char(
        'Title',
        size=128,
        required=True
    )
    total_hours = fields.Integer(
        string='Total Horas',
        store=True
    )

    content_ids = fields.One2many(
        'sie.content',
        inverse_name='knowledge_id',
        string='Contenido imprescindible',
        required=True,
        store=True
    )
    module_id = fields.Many2one(
        'sie.module',
        string='Módulo',
        required=True,
        store=True,
        ondelete='cascade'
    )

    _sql_constraints = [
        ('name_uk', 'unique(name, module_id)', u'Número debe ser único por área de conocimiento'),
        ('hours_ck', 'check(total_hours >= 0)', u'Número de horas debe ser mayor o igual a 0'),
    ]

    def calculate_total_hours(self, hour):
        for record in self:
            if record.content_ids:
                record.total_hours = sum(o.hours for o in record.content_ids)
                module_id = self.env['sie.module'].search([('id', '=', record.module_id.id)])
                module_id.calculate_total_hours(record.total_hours)
            else:
                record.total_hours = 0
