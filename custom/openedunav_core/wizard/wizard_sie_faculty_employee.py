# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WizardSieFacultyEmployee(models.TransientModel):
    _name = 'wizard.sie.faculty.employee'
    _description = "Create Employee and User of Faculty"

    user_boolean = fields.Boolean(
        "Want to create user too ?",
        default=True
    )

    def create_employee(self):
        for record in self:
            active_id = self.env.context.get('active_ids', []) or []
            faculty = self.env['sie.faculty'].browse(active_id)
            faculty.create_employee()
            if record.user_boolean and not faculty.user_id:
                user_group = self.env.ref('openedunav_core.group_faculty')
                self.env['res.users'].create_user(faculty, user_group)
