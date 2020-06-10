# -*- coding: utf-8 -*-

import base64
import logging
from datetime import date

from stdnum.ec import ruc, ci

from odoo import _, models, fields, api
from odoo.exceptions import ValidationError
from odoo.modules import get_module_resource

_logger = logging.getLogger(__name__)


class SieFaculty(models.Model):
    _name = 'sie.faculty'
    _description = "OpenEduNav Faculty"
    _inherit = ['mail.thread', 'image.mixin']
    _inherits = {"res.partner": "partner_id"}
    _order = 'full_name'

    @api.model
    def _default_image(self):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return base64.b64encode(open(image_path, 'rb').read())

    partner_id = fields.Many2one(
        'res.partner',
        'Partner',
        required=True,
        ondelete="cascade"
    )
    name = fields.Char(
        'Name',
    )
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
    place_of_birth = fields.Char(
        'Place of Birth',
        groups="hr.group_hr_user",
        tracking=True
    )
    country_of_birth = fields.Many2one(
        'res.country',
        string="Country of Birth",
        groups="hr.group_hr_user",
        tracking=True
    )
    birthday = fields.Date(
        'Date of Birth',
        groups="hr.group_hr_user",
        tracking=True,
        required=True,
        default='1960-03-09'
    )
    image_1920 = fields.Image(
        default=_default_image
    )
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(
        change_default=True
    )
    city = fields.Char()
    state_id = fields.Many2one(
        "res.country.state",
        string='State',
        ondelete='restrict',
        domain="[('country_id', '=?', country_id)]"
    )
    country_id = fields.Many2one(
        'res.country',
        string='Country',
        ondelete='restrict'
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
    gender = fields.Selection(
        [
            ('male', 'Male'),
            ('female', 'Female')
        ],
        'Gender',
        required=True,
        default='male'
    )
    nationality = fields.Many2one(
        'res.country',
        'Nationality'
    )
    emergency_contact = fields.Many2one(
        'res.partner',
        'Emergency Contact'
    )
    identification_id = fields.Char(
        'ID Number', size=64
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
    location_id = fields.Many2one(
        'sie.location',
        string='Reparto de procedencia'
    )
    title = fields.Many2one(
        'sie.person.title',
        string=u'Título',
        ondelete='restrict'
    )
    email = fields.Char()
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
    login = fields.Char(
        'Login',
        related='partner_id.user_id.login',
        readonly=1
    )
    last_login = fields.Datetime(
        'Latest Connection',
        readonly=1,
        related='partner_id.user_id.login_date'
    )
    emp_id = fields.Many2one(
        'hr.employee',
        'HR Employee'
    )
    active = fields.Boolean(default=True)
    category_id = fields.Many2one(
        'sie.faculty.category',
        u'Categoría',
        ondelete='restrict'
    )
    type = fields.Selection(
        [
            ('civil', 'Civil'),
            ('military', 'Military'),
        ],
        string='Tipo',
        default='civil',
        required=True
    )
    acronym = fields.Char(
        'Acronimo',
        size=10
    )
    academic_title_id = fields.Many2one(
        'sie.academic.title',
        string=u'Título Académico'
    )

    _sql_constraints = [
        (
            'email_unique',
            'UNIQUE(email)',
            u'Email debe ser único'
        ),
        (
            'identification_id',
            'UNIQUE(identification_id)',
            u'Identificación debe ser única'
        ),
        (
            'check_name',
            'CHECK(1=1)',
            'Contacto requiere un nombre'
        ),
    ]

    @api.depends('grade_id', 'specialty_id', 'academic_title_id', 'first_name', 'last_name', 'mother_name',
                 'middle_name')
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

    # @api.depends('birthday')
    # def _compute_age(self):
    #     if self.birthday:
    #         birthday = fields.Datetime.from_string(self.birthday)
    #         today = fields.Datetime.from_string(fields.Datetime.now())
    #         if today >= birthday:
    #             age = relativedelta(today, birthday)
    #             self.age = age.years

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

