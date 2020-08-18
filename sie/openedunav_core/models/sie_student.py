# -*- coding: utf-8 -*-
# Copyright (C) 2009-TODAY Manexware S.A.

import logging

from dateutil.relativedelta import relativedelta

from odoo import _, models, fields, api

_logger = logging.getLogger(__name__)


class SieStudent(models.Model):
    _name = "sie.student"
    _description = "OpenEduNav Faculty"
    _inherit = ['person.abstract.entity']
    _order = 'full_name'

    guest = fields.Boolean(
        'Invitado'
    )
    category_ids = fields.Many2many(
        'sie.student.category', 
        'student_category_rel',
        'student_id', 
        'category_id', 
        groups="sie.group_sie_manager",
        string='Category Tags'
    )
    admission_date = fields.Date(
        string='F.de ingreso Armada'
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
    location_id = fields.Many2one(
        'sie.location',
        string='Origin'
    )

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

    @api.model
    def create(self, vals):
        self.env['ir.config_parameter'].sudo().set_param('sie_entity.global.variable', 'sie_student')
        return super(SieStudent, self).create(vals)

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
                    # 'is_student': True,
                    'tz': self._context.get('tz'),
                })
                record.user_id = user_id