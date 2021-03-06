# -*- coding: utf-8 -*
from datetime import datetime

from dateutil.relativedelta import relativedelta
import logging

from docutils.nodes import field

from odoo import _, models, fields, api
from odoo.exceptions import ValidationError, Warning

_logger = logging.getLogger(__name__)


class SieCourse(models.Model):
    _name = 'sie.course'
    _description = 'Course'

    name = fields.Char(
        string='Nombre',
    )
    display_name = fields.Char(
        string='Nombre completo',
        compute='_compute_display_name',
        store=True
    )
    course_name = fields.Many2one(
        'sie.course.name',
        string='Nombre del curso',
        ondelete='restrict',
        required=True,
        states={'running': [('readonly', True)], 'finalized': [('readonly', True)]}
    )
    year = fields.Char(
        string=u'Año',
        required=True,
        compute='_compute_year'
    )
    period = fields.Selection(
        [
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6', '6'),
        ],
        string='Periodo',
        required=True,
        default='1'
    )
    start_date = fields.Date(
        string='Fecha Inicio',
        required=True,
        states={'running': [('readonly', True)], 'finalized': [('readonly', True)]}
    )
    end_date = fields.Date(
        string='Fecha Fin',
        required=True
    )
    state = fields.Selection(
        [
            ('planned', _('Planned')),
            ('running', _('Running')),
            ('finalized', _('Finalized'))
        ],
        'Status',
        copy=False,
        default='planned'
    )
    module_ids = fields.Many2many(
        'sie.module',
        string="Module",
        required=True,
        # domain="[('course_ids', '=', False)]",
        store=True,
        ondelete='restrict'
    )
    no_of_module = fields.Integer(
        compute='_compute_total',
        string='No. Módulos',
        store=True
    )
    total_hours = fields.Integer(
        compute='_compute_total',
        string='No. Hours',
        store=True
    )
    exec_hours = fields.Integer()
    total_credits = fields.Integer(
        compute='_compute_total',
        string=u'No Créditos',
        store=True
    )
    is_conduct = fields.Boolean(
        string='Is Conduct?',
        default=False
    )
    assigned_officer_id = fields.Many2one(
        'sie.faculty',
        string='Assigned Faculty',
        ondelete='restrict'
    )
    promotion_course_id = fields.Many2one(
        'sie.promotion.course',
        string=u'Promoción del Curso',
        ondelete='restrict',
        required=True,
        states={'running': [('readonly', True)], 'finalized': [('readonly', True)]}
    )
    # enrollment = fields.Many2one(
    #     'sie.nato',
    #     string=u'Paralelo'
    # )
    enrollment = fields.Char(
        string=u'Paralelo'
    )
    enrollment_div = fields.Many2one(
        'sie.division',
        string=u'División'
    )
    matrix_id = fields.Many2one(
        'sie.matrix',
        # string=u'Parámetros de Evaluación',
        # ondelete='restrict',
        # required=True
    )
    professional_attitude = fields.Many2many(
        'sie.faculty',
        string='Professional Attitude',
        required=True
    )
    statistician = fields.Many2one(
        'sie.faculty',
        string='Statistician',
        domain="[('statistician', '=', True)]",
        ondelete='restrict'
    )
    director = fields.Integer(
        compute='_compute_director',
        store=True
    )
    duration_days = fields.Float(
        'Duración días',
        compute='_compute_duration_days',
        store=True
    )
    work_days = fields.Float('Días laborables')
    place = fields.Char(
        string="Lugar/Escuela",
        compute='_compute_place',
        store=True
    )

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

    @api.constrains('professional_attitude', 'course_professional')
    def _check_professional_attitude(self):
        for record in self:
            if record.professional_attitude and record.course_professional:
                if len(record.professional_attitude) == len(record.course_professional):
                    pass
                else:
                    raise ValidationError(_("Check Professional Attitude"))

    @api.constrains('course_professional')
    def _check_professional_attitude(self):
        for record in self:
            if not record.course_professional:
                raise ValidationError(_("Check Professional Attitude"))

    @api.constrains('parameter_ids')
    def _check_coefficient(self):
        for record in self:
            if record.parameter_ids:
                total = sum(record.coefficient for record in record.parameter_ids)
                if total != 1:
                    raise ValidationError("Sum of coefficients must be equal to 1")

    @api.depends('course_name')
    def _compute_director(self):
        for record in self:
            if record.course_name:
                record.director = record.env.ref('openedunav_core.group_director').id

    @api.depends('module_ids.hours', 'module_ids.credits')
    def _compute_total(self):
        for record in self:
            if record.module_ids:
                record.no_of_module = len(record.module_ids)
                if record.no_of_module > 0:
                    record.total_hours = sum(record.hours for record in record.module_ids)
                    record.total_credits = sum(record.credits for record in record.module_ids)
                    for module in record.module_ids:
                        if record.total_credits:
                            coefficient = float(module.credits) / float(record.total_credits)
                            module.write({'coefficient': coefficient})
                else:
                    raise Warning(_("Seleccione al menos una materia"))

    @api.depends('promotion_course_id', 'course_name', 'enrollment')
    def _compute_display_name(self):
        for record in self:
            if record.promotion_course_id:
                if record.course_name:
                    if record.enrollment:
                        display_name = _('%s - %s - PARALELO %s' % (record.course_name.name,
                                                                    record.promotion_course_id.name, record.enrollment))
                    else:
                        display_name = _('%s - %s - %s' % (
                        record.course_name.name, record.promotion_course_id.name, record.enrollment_div))
                    record.display_name = display_name
                    record.name = display_name.upper()

    @api.depends('start_date', 'end_date')
    def _compute_duration_days(self):
        for record in self:
            if record.start_date and record.end_date:
                start_date = fields.Date.from_string(record.start_date)
                end_date = fields.Date.from_string(record.end_date)
                record.duration_days = (end_date - start_date).days

    @api.depends('course_name')
    def _compute_place(self):
        for record in self:
            company_id = self.env.user.company_id
            record.place = company_id.school_id.code

    def action_plan(self):
        for record in self:
            record.state = 'planned'
            enrollment = self.get_enrollment(record)
            for students_id in enrollment.student_ids:
                student = self.env['sie.student'].search([('id', '=', students_id.id)])
                student.sudo().write({'in_course': False, 'current_course': None})

    def get_enrollment(self, record):
        enrollment = self.env['sie.enrollment'].search([('course_id', '=', record.id)])
        return enrollment

    def action_run(self):
        for record in self:
            record.state = 'running'
            enrollment = self.get_enrollment(record)
            for students_id in enrollment.student_ids:
                student = self.env['sie.student'].search([('id', '=', students_id.id)])
                student.sudo().write({'in_course': True, 'current_course': record.id})

    def action_done(self):
        for record in self:
            record.state = 'finalized'
            enrollment = self.get_enrollment(record)
            for students_id in enrollment.student_ids:
                student = self.env['sie.student'].search([('id', '=', students_id.id)])
                student.sudo().write({'in_course': False, 'current_course': None})

    def copy(self, default=None):
        for record in self:
            default = dict(default or {})
            copied_count = record.search_count([('name', '=like', u"Copy of {}%".format(record.name))])
            if not copied_count:
                new_name = u"Copy of {}".format(record.name)
            else:
                new_name = u"Copy of {} ({})".format(record.name, copied_count)
            default['name'] = new_name
            default['promotion_course_id'] = record.promotion_course_id.id + 1
            return super(SieCourse, record).copy(default)

    @api.depends('start_date')
    def _compute_year(self):
        current_year = datetime.now().year
        for record in self:
            if record.start_date:
                current_year = fields.Datetime.from_string(record.start_date).year
            record.year = current_year

    def unlink(self):
        unlink_ids = []
        for record in self:
            if record.state != 'planned':
                raise ValidationError(_(u'No puedes borrar un curso cuando esta en ejecución o finalizado'))
            else:
                enrollment = self.get_enrollment(record)
                for students_id in enrollment.student_ids:
                    student = self.env['sie.student'].search([('id', '=', students_id.id)])
                    student.sudo().write({'in_course': False})
                unlink_ids.append(record.id)
        return super(SieCourse, self).unlink()
