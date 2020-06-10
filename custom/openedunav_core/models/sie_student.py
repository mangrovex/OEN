# -*- coding: utf-8 -*-
# Copyright (C) 2009-TODAY Manexware S.A.

import base64
import logging
from datetime import date

from dateutil.relativedelta import relativedelta
from stdnum.ec import ruc, ci

from odoo import _, models, fields, api
from odoo.exceptions import ValidationError
from odoo.modules import get_module_resource

_logger = logging.getLogger(__name__)


class SieStudent(models.Model):
    _name = "sie.student"
    _description = "Student"
    _inherit = "mail.thread"
    _inherits = {"res.partner": "partner_id"}

    @api.model
    def _default_image(self):
        image_path = get_module_resource('sie', 'static/src/img', 'default_image.png')
        return base64.b64encode(open(image_path, 'rb').read())

    partner_id = fields.Many2one(
        'res.partner',
        'Partner',
        required=True,
        ondelete="cascade"
    )
    name = fields.Char(
        string="Student Name",
        store=True, 
        readonly=False, 
        tracking=True
    )
    active = fields.Boolean("Active")
    color = fields.Integer('Color Index', default=0)
    work_phone = fields.Char('Work Phone')
    mobile_phone = fields.Char('Work Mobile')
    work_email = fields.Char('Work Email')
    user_id = fields.Many2one('res.users')
    full_name = fields.Char(
        string="Fullname",
        compute='_compute_name',
        store=True,
        index=True,
    )
    first_name = fields.Char(
        'First Name',
        size=128,
        translate=True
    )
    middle_name = fields.Char(
        'Middle Name',
        size=128,
        translate=True
    )
    last_name = fields.Char(
        'Last Name',
        size=128,
        translate=True
    )
    mother_name = fields.Char(
        "Mother Name",
        size=128,
        translate=True
    )
    nationality = fields.Char(
        "Nationality",
        size=128,
        translate=True
    )
    guest = fields.Boolean(
        'Invitado'
    )
    # Address
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    parish_id = fields.Many2one(
        "res.city.parish",
        string='parish',
        ondelete='restrict',
        domain="[('city_id', '=?', city_id)]"
    )
    city_id = fields.Many2one(
        "res.state.city",
        string='city',
        ondelete='restrict',
        domain="[('state_id', '=?', state_id)]"
    )
    state_id = fields.Many2one(
        "res.country.state",
        string='State',
        ondelete='restrict',
        domain="[('country_id', '=?', country_id)]"
    )
    country_id = fields.Many2one(
        'res.country', 
        'Nationality (Country)', 
        groups="openedunav_core.group_user", 
        tracking=True
    )
    gender = fields.Selection(
        [
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other')
        ], 
        groups="openedunav_core.group_user", 
        default="male", 
        tracking=True
    )
    blood_group = fields.Selection(
        [
            ('A+', 'A+ve'),
            ('B+', 'B+ve'),
            ('O+', 'O+ve'),
            ('AB+', 'AB+ve'),
            ('A-', 'A-ve'),
            ('B-', 'B-ve'),
            ('O-', 'O-ve'),
            ('AB-', 'AB-ve')
        ],
        string='Blood Group'
    )
    marital = fields.Selection(
        [
            ('single', 'Single'),
            ('married', 'Married'),
            ('cohabitant', 'Legal Cohabitant'),
            ('widower', 'Widower'),
            ('divorced', 'Divorced')
        ], 
        string='Marital Status', 
        groups="openedunav_core.group_user", 
        default='single', 
        tracking=True
    )
    spouse_complete_name = fields.Char(
        string="Spouse Complete Name", 
        groups="openedunav_core.group_user", 
        tracking=True
    )
    spouse_birthdate = fields.Date(
        string="Spouse Birthdate", 
        groups="openedunav_core.group_user", 
        tracking=True
    )
    children = fields.Integer(
        string='Number of Children', 
        groups="openedunav_core.group_user", 
        tracking=True
    )
    place_of_birth = fields.Char(
        'Place of Birth', 
        groups="openedunav_core.group_user", 
        tracking=True
    )
    country_of_birth = fields.Many2one(
        'res.country', 
        string="Country of Birth", 
        groups="openedunav_core.group_user", 
        tracking=True
    )
    birthday = fields.Date(
        'Date of Birth', 
        groups="openedunav_core.group_user", 
        tracking=True
    )
    ssnid = fields.Char(
        'SSN No', 
        help='Social Security Number', 
        groups="openedunav_core.group_user", 
        tracking=True
    )
    sinid = fields.Char(
        'SIN No', 
        help='Social Insurance Number', 
        groups="openedunav_core.group_user", 
        tracking=True
    )
    identification_id = fields.Char(
        string='Identification No', 
        groups="openedunav_core.group_user", 
        tracking=True
    )
    passport_id = fields.Char(
        'Passport No', 
        groups="openedunav_core.group_user", 
        tracking=True
    )
    visa_no = fields.Char(
        'Visa No', 
        groups="openedunav_core.group_user", 
        tracking=True
    )
    visa_expire = fields.Date(
        'Visa Expire Date', 
        groups="openedunav_core.group_user", 
        tracking=True
    )
    additional_note = fields.Text(
        string='Additional Note', 
        groups="openedunav_core.group_user", 
        tracking=True
    )
    certificate = fields.Selection(
        [
            ('bachelor', 'Bachelor'),
            ('master', 'Master'),
            ('other', 'Other'),
        ], 
        'Certificate Level', 
        default='other', 
        groups="openedunav_core.group_user", 
        tracking=True
    )
    study_field = fields.Char(
        "Field of Study", 
        groups="openedunav_core.group_user", 
        tracking=True
    )
    study_school = fields.Char(
        "School Name",
        groups="openedunav_core.group_user", 
        tracking=True
    )
    emergency_contact = fields.Char(
        "Emergency Contact", 
        groups="openedunav_core.group_user", 
        tracking=True
    )
    emergency_phone = fields.Char(
        "Emergency Phone", 
        groups="openedunav_core.group_user", 
        tracking=True
    )
    image_1920 = fields.Image(default=_default_image)
    title = fields.Many2one(
        'sie.person.title',
        string=u'Título',
        ondelete='restrict'
    )
    grade_id = fields.Many2one(
        'sie.grade',
        string=_('Grado'),
        ondelete='restrict'
    )
    specialty_id = fields.Many2one(
        'sie.specialty',
        string="Especialidad",
        ondelete='restrict'
    )
    sub_specialty_id = fields.Many2one(
        'sie.sub.specialty',
        string="Sub Especialidad",
        domain="[('specialty_id','=',specialty_id)]",
        ondelete='restrict'
    )
    age = fields.Char(
        string="Age"
    )
    religion = fields.Many2one(
        'sie.religion',
        'Religion',
        ondelete='restrict'
    )
    acronym = fields.Char(
        string='Acronimo'
    )
    foreign = fields.Boolean(
        string='Extranjero?'
    )
    serial_navy = fields.Char(
        string="Serial Naval"
    )
    study_level = fields.Selection(
        [
            ('first', 'Primer Nivel'),
            ('second', 'Segundo Nivel'),
            ('third', 'Tercer Nivel'),
            ('fourth', 'Cuarto Nivel'),
            ('fifth', 'Quinto Nivel')
        ],
        string=u"Eduación",
        default='first'
    )
    phone = fields.Char(
        string="Private Phone",
        groups="openedunav_core.group_user"
    )
    mobile = fields.Char(
        string="Mobile Phone",
        groups="openedunav_core.group_user"
    )
    email = fields.Char()
    email_formatted = fields.Char(
        'Formatted Email',
        compute='_compute_email_formatted',
        help='Format email address "Name <email@domain>"'
    )
    category_ids = fields.Many2many(
        'sie.student.category', 
        'student_category_rel',
        'student_id', 
        'category_id', 
        groups="sie.group_sie_manager",
        string='Tags'
    )
    admission_date = fields.Date(
        string='F.de ingreso Armada'
    )
    academic_title_ids = fields.Many2many(
        'sie.academic.title',
        string='Academic Titles'
    )
    promotion_id = fields.Many2one(
        comodel_name='sie.promotion',
        string=u"Promoción del Estudiante",
        ondelete='restrict'
    )
    force_years = fields.Integer(
        compute='_compute_force_years',
        string=u'Años en Fuerzas'
    )
    # CONADIS
    physical_exoneration = fields.Selection(
        [
            ('lactation', 'Lactancia'),
            ('discapacity', 'Discapacidad'),
        ],
        string=u"Exoneración Física"
    )
    conadis = fields.Char(
        string="CONADIS"
    )
    conadis_percent = fields.Float(
        string="Porcentaje"
    )
    observation_physical = fields.Char(
        u'Observación'
    )
    # origin
    location_id = fields.Many2one(
        'sie.location',
        string='Origin'
    )
    # Parents
    father_complete_name = fields.Char(
        string="Father Complete Name",
        groups="hr.group_hr_user",
        tracking=True
    )
    mother_complete_name = fields.Char(
        string="Mother Complete Name",
        groups="hr.group_hr_user",
        tracking=True
    )
    # misc
    notes = fields.Text(
        'Notes', 
        groups="openedunav_core.group_user"
    )
    barcode = fields.Char(
        string="Badge ID", 
        help="ID used for student identification.", 
        groups="openedunav_core.group_user", 
        copy=False
    )
    
    _sql_constraints = [
        (
            'email_unique',
            'UNIQUE(email)',
            u'Email debe ser único'
        ),
        (
            'identification_unique',
            'UNIQUE(identification_id)',
            u'Identificación debe ser única'
        ),
        (
            'check_name',
            'CHECK(1=1)',
            'Contacto requiere un nombre'
        ),
        (
            'unique_serial_navy',
            'unique(serial_navy)',
            'Serial Navy must be unique per student!'
        )
    ]

    @api.depends('grade_id', 'specialty_id', 'title', 'first_name', 'last_name', 'mother_name', 'middle_name')
    def _compute_name(self):
        prefix = self._compute_prefix()
        display_name = self._compute_full_name()
        self.full_name = display_name
        if len(prefix) > 0 and len(display_name):
            display_name = '%s %s' % (prefix, display_name)
            self.name = display_name.upper()

    def _compute_prefix(self):
        prefix = ''
        if self.grade_id:
            prefix = '%s' % self.grade_id.acronym
        if self.specialty_id:
            prefix = '%s-%s' % (prefix, self.specialty_id.acronym)
        if len(prefix) == 0 and self.title:
            prefix = '%s' % self.title.acronym
        return prefix

    def _compute_full_name(self):
        display_name = ''
        if self.first_name and self.last_name and self.mother_name:
            if self.middle_name:
                display_name = '%s %s %s %s' % (self.last_name, self.mother_name,
                                                self.first_name, self.middle_name)
            else:
                display_name = '%s %s %s' % (self.last_name,
                                             self.mother_name, self.first_name)
        return display_name.upper()

    @api.onchange('first_name', 'middle_name', 'last_name', 'mother_name')
    def _onchange_name(self):
        self._compute_full_name()

    @api.onchange('birthday')
    def onchange_employee_birthday(self):
        if self.birthday:
            today = date.today()
            age = today.year - self.birthday.year - ((today.month, today.day) <
                                                     (self.birthday.month, self.birthday.day))
            self.age = str(age)

    @api.constrains('birthday')
    def _check_birthday(self):
        for record in self:
            if record.birthday:
                if record.birthday > fields.Date.today():
                    raise ValidationError(_("Birth Date can't be greater than current date!"))

    @api.constrains('identification_id', 'type_ced_ruc')
    def check_vat(self):
        for record in self:
            if record.type_nuc and record.identification_id:
                if record.type_nuc == 'cedula' and not ci.is_valid(record.identification_id):
                    raise ValidationError('CI [%s] no es valido !' % record.identification_id)
                elif record.type_nuc == 'ruc' and not ruc.is_valid(record.identification_id):
                    raise ValidationError('RUC [%s] no es valido !' % record.identification_id)

    @api.depends('admission_date')
    def _compute_force_years(self):
        for record in self:
            if record.admission_date:
                admission_date = fields.Datetime.from_string(record.admission_date)
                _logger.warning("in Year: %s" % admission_date)
                today = fields.Datetime.from_string(fields.Datetime.now())
                _logger.warning("Hoy: %s" % today)
                if today >= admission_date:
                    calculate_age = relativedelta(today, admission_date)
                    # _logger.warning(calculate_age)
                    record.force_years = calculate_age.years
                    # _logger.warning("Force in year: %s " % self.force_years)

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Students'),
            'template': '/sie/static/xls/sie_student.xls'
        }]

