# -*- coding: utf-8 -*
import time
import logging
from operator import attrgetter
from odoo import models, fields, api, _
import icu
from .misc import SCORE_STATE, SCORE_NUMBER

NUM_APORT = [('primer aporte', 'PRIMER APORTE'),
             ('segundo aporte', 'SEGUNDO APORTE'),
             ('tercer aporte', 'TERCER APORTE')]


class SieLicense(models.Model):
    _name = 'sie.report.behavior'
    _description = 'Average Behavior'

    name = fields.Char(string='Nombre', compute='_compute_display_name', store=True)
    date = fields.Datetime(string='Fecha', required=True)
    date_in = fields.Datetime(string='Fecha de Inicio', required=True)
    date_out = fields.Datetime(string='Fecha de Fin', required=True)
    course_id = fields.Many2one('sie.course', string='Curso', required=True, ondelete='restrict')
    aport = fields.Selection(NUM_APORT, string=u"Número de aporte", required=True)
    # enrollment_id = fields.Integer(compute='_compute_student')
    enrollment_id = fields.Many2one('sie.enrollment', string=u'División', ondelete='restrict',
                                    domain="[('course_id.state', '!=', 'finalized')]", readonly=True,
                                    states={'draft': [('readonly', False)]})
    student_ids = fields.One2many('sie.student.behavior.report', inverse_name='report_id', string='Estudiantes')
    is_readonly = fields.Boolean(string='Is readonly?')
    score_number = fields.Selection(SCORE_NUMBER, string='No. Noa')



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
        seq = 0
        for student in student_ids:
            if not student.inactive:
                data = {
                    'name': student.ced_ruc,
                    'student_id': student.id,
                    'seq': seq
                }
                students.append(data)
        self.student_ids = students

    @api.multi
    def generate_report(self):
        for record in self:
            for student in record.student_ids:
                puntualidad = self.env['sie.news'].search(
                    [('date','>=',record.date_in),('date','<=',record.date_out),
                     ('name_type','=','puntualidad'),('student_id','=',student.student_id.id)])
                if puntualidad:
                    student.punctuality = len(puntualidad)
                presencia = self.env['sie.news'].search(
                    [('date', '>=', record.date_in), ('date', '<=', record.date_out),
                     ('name_type', '=', 'presencia_personal'), ('student_id', '=', student.student_id.id)])
                if presencia:
                    student.presence = len(presencia)
                conservacion = self.env['sie.news'].search(
                    [('date', '>=', record.date_in), ('date', '<=', record.date_out),
                     ('name_type', '=', 'conservacion_areas'), ('student_id', '=', student.student_id.id)])
                if conservacion:
                    student.conservation = len(conservacion)
                student.average = (20 - ((student.punctuality + student.presence + student.conservation) * 0.05))

                licencia = self.env['sie.license'].search(
                    [('date','>=',record.date_in), ('date','<=',record.date_out),
                     ('name_type','=','permiso'),('student_id', '=', student.student_id.id)])
                if licencia:
                    lic = 0
                    for a in licencia:
                        lic = lic + a.hours
                    student.leave = lic

                descanso = self.env['sie.license'].search(
                    [('date', '>=', record.date_in), ('date', '<=', record.date_out),
                     ('name_type', '=', 'descanso'), ('student_id', '=', student.student_id.id)])
                if descanso:
                    des = 0
                    for b in descanso:
                        des = des + b.hours
                    student.medical_leave = des

                dias = record.course_id.work_days
                student.leave_calc = ((20*(dias - student.leave))/dias)
                student.medical_calc = ((20*(dias - student.medical_leave))/dias)

                brig = self.env['sie.brigadier.note'].search(
                    [('date', '>=', record.date_in), ('date', '<=', record.date_out),
                     ('course_id', '=', record.course_id.id), ('aport','=',record.aport)])
                if brig:
                    for c in brig:
                        for d in brig.student_ids:
                            if student.student_id.id == d.student_id.id:
                                student.note_oficial_1 = d.note_brigadier

                student.military_postage = ((student.leave_calc+student.medical_calc+student.note_oficial_1)/3)
                student.note_total = ((student.average+student.military_postage)/2)

    @api.multi
    def sort_by_name(self):
        for record in self:
            collator = icu.Collator.createInstance(icu.Locale('es'))
            # student_ids = sorted(record.student_ids,key=attrgetter('last_name','mother_name','first_name','middle_name'),cmp=collator.compare)
            student_ids = sorted(record.student_ids, key=attrgetter('full_name'), cmp=collator.compare)
            seq = 0
            for student in student_ids:
                seq += 1
                student.write({'seq': seq})

    @api.multi
    def sort_by_score(self):
        for record in self:
            student_ids = record.student_ids.sorted(
                key=attrgetter('note_total'), reverse=True)
            seq = 0
            for student in student_ids:
                seq += 1
                student.write({'seq': seq})


