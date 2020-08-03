# -*- coding: utf-8 -*
import logging

from odoo import models, fields, api
_logger = logging.getLogger(__name__)


class SieSubjectUnit(models.Model):
    _name = 'sie.subject.unit'
    _description = 'Learning Unit'

    name = fields.Char(
        'Title',
        size=128,
        required=True
    )
    total_hours = fields.Integer(
        string='Total Horas',
        store=True
    )

    child_ids = fields.One2many(
        'sie.subject.content',
        inverse_name='parent_id',
        string='Contenido imprescindible',
        required=True,
        store=True
    )
    subject_id = fields.Many2one(
        'sie.subject',
        string='Módulo',
        required=True,
        store=True,
        ondelete='cascade'
    )

    _sql_constraints = [
        ('name_uk', 'unique(name, parent_id)', u'Número debe ser único por área de conocimiento'),
        ('hours_ck', 'check(hours >= 0)', u'Número de horas debe ser mayor o igual a 0'),
    ]

    def calculate_total_hours(self, hour):
        for record in self:
            if record.child_ids:
                record.total_hours = sum(o.hours for o in record.child_ids)
                subject_id = self.env['sie.subject'].search([('id', '=', record.subject_id.id)])
                subject_id.calculate_total_hours(record.total_hours)
            else:
                record.total_hours = 0
