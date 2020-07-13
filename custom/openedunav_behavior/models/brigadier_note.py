# -*- coding: utf-8 -*

import time
import logging

from odoo import _, models, fields, api

NUM_APORT = [('primer aporte', 'PRIMER APORTE'),
             ('segundo aporte', 'SEGUNDO APORTE'),
             ('tercer aporte', 'TERCER APORTE')]

class SieBrigadier_Note(models.Model):
    _name = 'sie.brigadier.note'
    _description = 'Oficial Notes'

    name = fields.Char(string='Nombre', compute='_compute_display_name', store=True)
    date = fields.Date(string='Fecha', required=True)
    aport = fields.Selection(NUM_APORT, string=u"Número de Aporte", required=True)
    course_id = fields.Many2one('sie.course', string='Curso', domain="[('state', '=', 'running')]",
                                ondelete='restrict', required=True)
    enrollment_id = fields.Many2one('sie.enrollment', string=u'División', ondelete='restrict',
                                    domain="[('course_id.state', '!=', 'finalized')]", readonly=True,
                                    states={'draft': [('readonly', False)]})
    student_ids = fields.One2many('sie.student.brigadier', inverse_name='behavior_id', string='Estudiantes')
    is_readonly = fields.Boolean(string='Is readonly?')

    #validar que la combinación del curso y el aporte no se repitan.
    _sql_constraints = [
        ('name_uk', 'unique(course_id,aport)', _('El aporte en el curso indicado ya ha sido creado'))
    ]

    @api.multi
    @api.depends('course_id', 'date')
    def _compute_display_name(self):
        for record in self:
            if record.course_id and record.date:
                create_date = time.strftime('%Y%m%d%H%M%S')
                name = '%s | %s ' % (record.course_id.name, create_date)
                record.name = name

    @api.onchange('course_id')
    def onchange_course_id(self):
        students = []
        enrollment = self.env['sie.enrollment'].search([('course_id', '=', self.course_id.id)])
        student_ids = enrollment.student_ids
        for student in student_ids:
            if not student.inactive:
                data = {
                    'name': student.ced_ruc,
                    'student_id': student.id,
                }
                students.append(data)
        self.student_ids = students