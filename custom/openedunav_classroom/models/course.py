# -*- coding: utf-8 -*

from dateutil.relativedelta import relativedelta
import logging

from odoo import _, models, fields, api
from odoo.exceptions import ValidationError, Warning
from .misc import COURSE_STATE, PERIOD, ENROLLLMENT

_logger = logging.getLogger(__name__)

PLACE = [('escape','ESCAPE'),('esdeim','ESDEIM')]


class SieCourse(models.Model):
    _name = 'sie.course'
    _description = 'Curso'

    name = fields.Char(string='Nombre', compute='_compute_display_name', store=True)
    course_name = fields.Many2one('sie.course.name', string='Nombre del curso', ondelete='restrict', required=True,
                                  states={'running': [('readonly', True)], 'finalized': [('readonly', True)]})
    lastname = fields.Char(string='LastName')
    year = fields.Char(string=u'Año', required=True, compute='_compute_year')
    period = fields.Selection(PERIOD, string='Periodo', required=True, default='1')
    start_date = fields.Date(string='Fecha Inicio', required=True,
                             states={'running': [('readonly', True)], 'finalized': [('readonly', True)]})
    end_date = fields.Date(string='Fecha Fin', required=True)
    state = fields.Selection(COURSE_STATE, 'Estado', default='planned')
    subject_ids = fields.Many2many('sie.subject', string="Asignaturas", required=True,
                                   domain="[('course_id', '=',False)]", store=True, ondelete='restrict')
    no_of_subject = fields.Integer(compute='_compute_total', string='No. Asignaturas', store=True)
    total_hours = fields.Integer(compute='_compute_total', string='No. Horas', store=True)
    exec_hours = fields.Integer()
    total_credits = fields.Integer(compute='_compute_total', string=u'No Créditos', store=True)
    is_conduct = fields.Boolean(string='Es Conducta?', default=False)
    assigned_officer_id = fields.Many2one('sie.faculty', string='Oficial Asignado', ondelete='restrict')
    promotion_course_id = fields.Many2one('sie.promotion.course', string=u'Promoción del Curso', ondelete='restrict',
                                       required=True,
                                       states={'running': [('readonly', True)], 'finalized': [('readonly', True)]})
    enrollment = fields.Selection(ENROLLLMENT, string=u'División')
    matrix_id = fields.Many2one('sie.matrix', string=u'Parámetros de Evaluación', ondelete='restrict', required=True)
    professional_attitude = fields.Many2many('sie.faculty', string='Professional Attitude', required=True)
    statistician = fields.Many2one('sie.faculty', string='Statistician',
                                   domain="[('statistician', '=', True)]", ondelete='restrict')
    director = fields.Integer(compute='_compute_director', store=True)
    new_table = fields.Boolean(string="2017", defualt=True)
    duration_days = fields.Float(u'Duración días', compute='_compute_duration_days', store = True)
    work_days = fields.Float(u'Días laborables')
    place = fields.Selection(PLACE,string="Lugar/Escuela")

    _sql_constraints = [
        ('name_uk', 'unique(name)', 'No se debe repetir la promocion por curso')
    ]

    @api.constrains('end_date', 'start_date')
    def _check_end_date(self):
        for record in self:
            if record.start_date and record.end_date:
                start_date = fields.Datetime.from_string(record.start_date)
                end_date = fields.Datetime.from_string(record.end_date)
                if end_date < start_date:
                    end_date = start_date + relativedelta(months=+ 3)
                    record.end_date = end_date
                    raise Warning("La fecha de fin de curso tiene que ser mayor a la fecha de inicio")
            else:
                raise ValidationError("Seleccione las fecha de inicio y fin de curso")

    # @api.multi
    # @api.constrains('professional_attitude', 'course_professional')
    # def _check_professional_attitude(self):
    #     for record in self:
    #         if record.professional_attitude and record.course_professional:
    #             if len(record.professional_attitude) == len(record.course_professional):
    #                 pass
    #             else:
    #                 raise ValidationError(_("Check Professional Attitude"))

    # @api.multi
    # @api.constrains('course_professional')
    # def _check_professional_attitude(self):
    #     for record in self:
    #         if not record.course_professional:
    #             raise ValidationError(_("Check Professional Attitude"))

    # @api.multi
    # @api.constrains('parameter_ids')
    # def _check_coefficient(self):
    #     for record in self:
    #         if record.parameter_ids:
    #             total = sum(record.coefficient for record in record.parameter_ids)
    #             if total != 1:
    #                 raise ValidationError("Sum of coefficients must be equal to 1")

    # @api.one
    # @api.depends('course_name')
    # def _compute_director(self):
    #     if self.course_name:
    #         self.director = self.env.ref('openedunav_escape.group_sie_executive').id

    @api.depends('subject_ids.hours','subject_ids.credits')
    def _compute_total(self):
        for record in self:
            if record.subject_ids:
                record.no_of_subject = len(record.subject_ids)
                if record.no_of_subject > 0:
                    record.total_hours = sum(record.hours for record in record.subject_ids)
                    record.total_credits = sum(record.credits for record in record.subject_ids)
                    for subject in record.subject_ids:
                        if record.total_credits:
                            coefficient = float(subject.credits) / float(record.total_credits)
                            subject.write({'coefficient':coefficient})
                else:
                    raise Warning(_("Seleccione al menos una materia"))

    @api.multi
    @api.depends('promotion_course_id', 'course_name', 'enrollment')
    def _compute_display_name(self):
        for record in self:
            if record.promotion_course_id and record.course_name:
                name = _('%s - %s' % (record.course_name.name, record.promotion_course_id.name))
                record.name = name
            if record.promotion_course_id and record.enrollment and record.matrix_id:
                name = _('%s - %s - PARALELO %s' % (record.course_name.name,
                                                    record.promotion_course_id.name, record.enrollment))
                record.name = name

    @api.multi
    @api.depends('start_date', 'end_date')
    def _compute_duration_days(self):
        for record in self:
            if record.start_date and record.end_date:
                start_date = fields.Date.from_string(record.start_date)
                end_date = fields.Date.from_string(record.end_date)
                record.duration_days = (end_date - start_date).days

    @api.multi
    def action_plan(self):
        for record in self:
            record.state = 'planned'
            enrollment = self.env['sie.enrollment'].search([('course_id', '=', record.id)])
            for students_id in enrollment.student_ids:
                student = self.env['sie.student'].search([('id', '=', students_id.id)])
                student.sudo().write({'in_course': False, 'current_course':None})

    @api.multi
    def action_run(self):
        for record in self:
            record.state = 'running'
            enrollment = self.env['sie.enrollment'].search([('course_id', '=', record.id)])
            for students_id in enrollment.student_ids:
                student = self.env['sie.student'].search([('id', '=', students_id.id)])
                student.sudo().write({'in_course': True,'current_course':record.id})

    @api.multi
    def action_done(self):
        for record in self:
            record.state = 'finalized'
            enrollment = self.env['sie.enrollment'].search([('course_id', '=', record.id)])
            for students_id in enrollment.student_ids:
                student = self.env['sie.student'].search([('id', '=', students_id.id)])
                student.sudo().write({'in_course': False,'current_course':None})

    @api.one
    def copy(self, default=None):
        default = dict(default or {})
        copied_count = self.search_count([('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)
        default['name'] = new_name
        default['promotion_course_id'] = self.promotion_course_id.id + 1
        return super(SieCourse, self).copy(default)

    @api.multi
    @api.depends('start_date')
    def _compute_year(self):
        for record in self:
            if record.start_date:
                record.year = fields.Datetime.from_string(record.start_date).year


    @api.multi
    def unlink(self):
        unlink_ids = []
        for record in self:
            if record.state != 'planned':
                raise ValidationError(_(u'No puedes borrar un curso cuando esta en ejecución o finalizado'))
            else:
                enrollment = self.env['sie.enrollment'].search([('course_id', '=', record.id)])
                for students_id in enrollment.student_ids:
                    student = self.env['sie.student'].search([('id', '=', students_id.id)])
                    student.sudo().write({'in_course': False})
                unlink_ids.append(record.id)
        return super(SieCourse, self).unlink()
