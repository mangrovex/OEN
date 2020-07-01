# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WizardSieStudent(models.TransientModel):
    _name = 'wizard.sie.student'
    _description = "Create User for selected Student(s)"

    def _get_students(self):
        if self.env.context and self.env.context.get('active_ids'):
            return self.env.context.get('active_ids')
        return []

    student_ids = fields.Many2many(
        'sie.student',
        default=_get_students,
        string='Students'
    )

    def create_student_user(self):
        user_group = self.env.ref('openedunav_core.group_faculty')
        active_ids = self.env.context.get('active_ids', []) or []
        records = self.env['sie.student'].browse(active_ids)
        self.env['res.users'].create_user(records, user_group)
