# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SieTrainingShaft(models.Model):
    _name = 'sie.training.shaft'
    _description = 'Shaft of Training'
    _order = 'name'

    name = fields.Char(
        'Name',
        size=96,
        required=True
    )
    faculty_id = fields.Many2one(
        comodel_name='sie.faculty',
        string='Faculty',
        store=True
    )
    subject_ids = fields.One2many(
        'sie.module',
        'shaft_id',
        'Subjects'
    )

    _sql_constraints = [
        ('name_uk', 'unique(name)', 'Shaft of training must be unique'),
    ]

    @api.model
    def create(self, vals):
        vals['name'] = vals['name'].title()
        return super(SieTrainingShaft, self).create(vals)

    def write(self, vals):
        if vals.get('name'):
            name = vals['name']
        else:
            name = self.name
        vals.update({'name': name.title()})
        return super(SieTrainingShaft, self).write(vals)
