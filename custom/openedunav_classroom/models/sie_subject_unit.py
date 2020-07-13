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
    number = fields.Integer(
        'Número',
        required=True
    )
    description = fields.Text(
        'Descripción'
    )
    parent_id = fields.Many2one(
        'sie.subject.unit',
        'Padre',
        ondelete='cascade'
    )
    child_ids = fields.One2many(
        'sie.subject.unit',
        'parent_id',
        'Unidades de Aprendizaje'
    )
    subject_id = fields.Many2one(
        'sie.subject',
        'Asignatura',
        ondelete='cascade'
    )
    hours = fields.Integer(
        'No. Horas',
        default=0
    )
    total_hours = fields.Integer(
        compute='_total_hours',
        string='Total Horas',
        store=True
    )
    last_child = fields.Boolean(
        compute='_compute_last_child',
        string=u'Último hijo',
        default=True, store=True
    )
    subject_ref = fields.Char(
        string='Asignatura ref',
        compute='_compute_subject_ref',
        store=True
    )

    _sql_constraints = [
        ('number_uk', 'unique(number, parent_id)', u'Número debe ser único por unidad de aprendizaje'),
        ('hours_ck', 'check(hours >= 0)', u'Número de horas debe ser mayor o igual a 0'),
    ]

    @api.depends('child_ids')
    def _total_hours(self):
        for record in self:
            if record.child_ids:
                record.total_hours = sum(o.hours for o in record.child_ids)
            else:
                record.total_hours = 0

    @api.onchange('total_hours')
    def _onchange_total_hours(self):
        for record in self:
            if record.total_hours > 0:
                record.hours = record.total_hours
                record.last_child = False
            else:
                record.hours = 0
                record.last_child = True

    @api.depends('total_hours')
    def _compute_last_child(self):
        for record in self:
            if record.total_hours > 0:
                record.last_child = False
            else:
                record.last_child = True

    @api.depends('parent_id', 'subject_id')
    def _compute_subject_ref(self):
        for record in self:
            if record.parent_id:
                record.subject_ref = record.parent_id.subject_ref
            else:
                record.subject_ref = record.subject_id.id
