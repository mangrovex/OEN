# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    name = fields.Char(store=True)
    foreign = fields.Boolean(
        u'Foreign?',
        readonly=False
    )
    type = fields.Selection(
        selection_add=
        [
            ('sie.student', 'Student'),
            ('sie.faculty', 'Faculty'),
         ],
        string='Type',
    )
    is_parent = fields.Boolean("Is a Parent")
    is_faculty = fields.Boolean("Is a Faculty")
    is_student = fields.Boolean("Is a Student")
    alias = fields.Char(
        string='Alias',
        help='Common name that the Party is referred',
    )
    faculty_ids = fields.One2many(
        string='Related Faculties',
        comodel_name='sie.faculty',
        compute='_compute_faculty_ids_and_count',
    )
    count_faculties = fields.Integer(
        compute='_compute_faculty_ids_and_count',
    )
    student_ids = fields.One2many(
        string='Related Students',
        comodel_name='sie.student',
        compute='_compute_student_ids_and_count',
    )
    count_students = fields.Integer(
        compute='_compute_student_ids_and_count',
    )
    emergency_contact = fields.Many2one(
        'res.partner',
        'Emergency Contact'
    )
    emergency_phone = fields.Char(
        "Emergency Phone",
        groups="openedunav_core.group_user",
        tracking=True
    )

    _sql_constraints = [
        (
            'email_unique',
            'UNIQUE(email)',
            u'Email debe ser único'
        ),
        (
            'identification_unique',
            'UNIQUE(ced_ruc)',
            u'Identificación debe ser única'
        ),
        (
            'check_name',
            'CHECK(name IS NOT NULL)',
            'Contacto requiere un nombre'
        ),
    ]

    def _get_faculty_entity(self):
        for record in self:
            if record.type and record.type[:7] == 'faculty':
                return record.env[record.type].search([
                    ('partner_id', '=', record.id),
                ])

    def _get_student_entity(self):
        for record in self:
            if record.type and record.type[:6] == 'student':
                return record.env[record.type].search([
                    ('partner_id', '=', record.id),
                ])

    def _compute_faculty_ids_and_count(self):
        for record in self:
            faculties = self.env['sie.faculty'].search([
                ('partner_id', 'child_of', record.id),
            ])
            record.count_faculties = len(faculties)
            record.faculty_ids = [(6, 0, faculties.ids)]

    def _compute_student_ids_and_count(self):
        for record in self:
            students = self.env['sie.student'].search([
                ('partner_id', 'child_of', record.id),
            ])
            record.count_faculties = len(students)
            record.faculty_ids = [(6, 0, students.ids)]

    @api.model
    def create(self, vals):
        """ It overrides create to bind appropriate sie entity. """
        if self.env['ir.config_parameter'].sudo().get_param('sie_entity.global.variable') == 'sie_faculty':
            vals['type'] = 'sie.faculty'
            vals['is_parent'] = False
            vals['is_faculty'] = True
            vals['is_student'] = False
        if self.env['ir.config_parameter'].sudo().get_param('sie_entity.global.variable') == 'sie_student':
            vals['type'] = 'sie.student'
            vals['is_parent'] = False
            vals['is_faculty'] = False
            vals['is_student'] = True
        return super(ResPartner, self).create(vals)
