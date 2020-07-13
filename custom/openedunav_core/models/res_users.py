# -*- coding: utf-8 -*-

import logging

from odoo import models, api

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _name = "res.users"
    _inherit = "res.users"

    def create_user(self, records, user_group=None):
        for rec in records:
            if not rec.user_id:
                user_vals = {
                    'name': rec.name,
                    'login': rec.email or (rec.name + rec.last_name),
                    'partner_id': rec.partner_id.id,
                    # 'dept_id': rec.main_department_id.id,
                    # 'department_ids': rec.allowed_department_ids.ids
                }
                user_id = self.create(user_vals)
                rec.user_id = user_id
                if user_group:
                    user_group.users = user_group.users + user_id

    # @api.onchange('first_name', 'middle_name', 'last_name', 'mother_name')
    # def _compute_name(self):
    #     for record in self:
    #         if record.first_name and record.last_name and record.mother_name:
    #             if record.middle_name:
    #                 display_name = '%s %s %s %s' % (record.last_name, record.mother_name,
    #                                                 record.first_name, record.middle_name)
    #             else:
    #                 display_name = '%s %s %s' % (record.last_name,
    #                                              record.mother_name, record.first_name)
    #             record.name = display_name.upper()
