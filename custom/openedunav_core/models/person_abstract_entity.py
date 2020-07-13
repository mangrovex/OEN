# -*- coding: utf-8 -*-
from stdnum.ec import ci, ruc

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class PersonAbstractEntity(models.AbstractModel):
    _name = 'person.abstract.entity'
    _description = 'Person Abstract Entity'
    _inherits = {'res.partner': 'partner_id'}
    _inherit = ['mail.thread']

    # Redefine ``active`` so that it is managed independently from partner.
    active = fields.Boolean(
        default=True,
    )
    partner_id = fields.Many2one(
        string='Related Partner',
        comodel_name='res.partner',
        required=True,
        ondelete='cascade',
        index=True,
    )
    type = fields.Selection(
        related='partner_id.type',
        default=lambda s: s._name,
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
    nationality = fields.Many2one(
        'res.country',
        'Nationality'
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
    type_personal = fields.Selection(
        [
            ('civil', 'Civil'),
            ('military', 'Military'),
        ],
        string='Personal Type',
        default='civil',
        required=True
    )
    academic_title_ids = fields.Many2many(
        'sie.academic.title',
        string='Academic Titles'
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
    acronym = fields.Char(
        'Acronimo',
        size=10
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
    religion = fields.Many2one(
        'sie.religion',
        'Religion',
        ondelete='restrict'
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
    serial_navy = fields.Char(
        string="Serial Naval"
    )
    ssnid = fields.Char(
        'SSN No',
        help='Social Security Number',
        tracking=True
    )
    sinid = fields.Char(
        'SIN No',
        help='Social Insurance Number',
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
    user_id = fields.Many2one(
        'res.users',
        'User',
        ondelete="cascade",
        help='The internal user in charge of this contact.'
    )

    # _sql_constraints = [
    #     (
    #         'unique_serial_navy',
    #         'UNIQUE(serial_navy)',
    #         'Serial Navy must be unique per student!'
    #     )
    # ]

    def toggle_active(self):
        """ It toggles patient and partner activation. """
        for record in self:
            super(PersonAbstractEntity, self).toggle_active()
            if record.active:
                record.partner_id.active = True
            else:
                entities = record.env[record._name].search([
                    ('partner_id', 'child_of', record.partner_id.id),
                    ('active', '=', True),
                ])
                if not entities:
                    record.partner_id.active = False

    def toggle(self, attr):
        if getattr(self, attr) is True:
            self.write({attr: False})
        elif getattr(self, attr) is False:
            self.write({attr: True})

    @api.depends('grade_id', 'specialty_id', 'academic_title_ids', 'first_name', 'last_name', 'mother_name',
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
        self.name = self._compute_full_name()

    @api.onchange('grade_id', 'specialty_id', 'academic_title_ids')
    def _onchange_name_prefix(self):
        self.name = self._compute_name()

    def create_student_user(self):
        user_group = self.env.ref("base.group_portal") or False
        users_res = self.env['res.users']
        for record in self:
            if not record.user_id:
                user_id = users_res.create({
                    'name': record.name,
                    'partner_id': record.partner_id.id,
                    'login': record.email,
                    'groups_id': user_group,
                    'is_student': True,
                    'tz': self._context.get('tz'),
                })
                record.user_id = user_id

    @api.constrains('ced_ruc', 'type_ced_ruc', 'type_person')
    def check_ced_ruc(self):
        for record in self:
            if record.type_ced_ruc:
                if record.type_ced_ruc == 'cedula' and not ci.is_valid(record.ced_ruc):
                    raise ValidationError('CI [%s] no es valido !' % record.ced_ruc)
                elif record.type_ced_ruc == 'ruc' and not ruc.is_valid(record.ced_ruc):
                    raise ValidationError('RUC [%s] no es valido !' % record.ced_ruc)