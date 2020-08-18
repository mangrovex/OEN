# -*- coding: utf-8 -*

from odoo import models, fields, api


class SieRegisterSeminary(models.Model):
    _name = 'sie.register.seminary'
    _rec_name = 'seminary_name'
    _description = 'Redistro de seminarios'

    seminary_name = fields.Char(
        string='Nombre del seminario',
        required=True
    )
    course_id = fields.Many2one(
        'sie.course',
        string='Curso',
        required=True,
        domain=[('state', '!=', 'finalized')],
        ondelete='restrict'
    )
    expositor = fields.Char(
        string='Expositor',
        required=True
    )
    date = fields.Date(
        string='Fecha',
        required=True
    )
    duration = fields.Integer(
        'Duración',
        required=True
    )
    # enrollment_id = fields.Many2one('sie.enrollment',compute='_compute_enrollment',store=True)
    enrollment_id = fields.Many2one(
        'sie.enrollment',
        store=True,
        ondelete='restrict'
    )

    @api.depends('course_id')
    def _compute_enrollment(self):
        if self.course_id:
            enrollment_id = self.env['sie.enrollment'].search([('course', '=', 'DIRECTOR')])
            self.enrollment_id = enrollment_id.id
