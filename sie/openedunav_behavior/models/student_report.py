# -*- coding: utf-8 -*
from odoo import models, fields, api
from decimal import *
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError

class SieStudetnBehavior(models.Model):
    _name = 'sie.student.behavior.report'
    _description = 'Student\'s Report'

    student_id = fields.Many2one('sie.student', string='Estudiante', ondelete='restrict',
                                 required=True, store=True)
    first_name = fields.Char("Primer Nombre", related='student_id.first_name', store=True)
    middle_name = fields.Char("Segundo Nombre", related='student_id.middle_name', store=True)
    last_name = fields.Char("Primer Apellido", related='student_id.last_name', store=True)
    mother_name = fields.Char("Segundo Apellido", related='student_id.mother_name', store=True)
    report_id = fields.Many2one('sie.report.behavior', string='ID Reporte',
                                  ondelete='cascade')
    # promedio final de comportamiento entre averange y military postage
    note_total = fields.Float(string='Promedio', digits=dp.get_precision('Score'))

    punctuality = fields.Integer(string='Puntualidad')
    presence = fields.Integer(string='Presencia Personal')
    conservation = fields.Integer(string=u'Conservación de áreas asignadas')
    # promedio de las tres notas, puntualidad, presencia personal y conservacion
    average = fields.Float(string='Nota', digits=dp.get_precision('Score'))
    leave = fields.Float(string=u'Cálculo Permisos', digits=dp.get_precision('Score'))
    leave_calc = fields.Float(string='Permisos', digits=dp.get_precision('Score'))
    medical_leave = fields.Float(string=u'Cálculo Descanso Médico', digits=dp.get_precision('Score'))
    medical_calc = fields.Float(string=u'Descanso Médico', digits=dp.get_precision('Score'))
    note_oficial = fields.Many2one('sie.student.brigadier', string='Nota_Oficial')
    note_oficial_1 = fields.Float(string='Brigadieres', digits=dp.get_precision('Score'))
    # promedio de permisos, permisos medicos y nota del oficial
    military_postage = fields.Float(string='Nota', digits=dp.get_precision('Score'))
    full_name = fields.Char("Nombre", related='student_id.full_name', store=True)
    seq = fields.Integer(string='No.')

    _order = 'seq'
