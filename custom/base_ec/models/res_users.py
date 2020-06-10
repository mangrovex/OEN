# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class Users(models.Model):
    _name = 'res.users'
    _inherit = 'res.users'

    signature_image = fields.Binary(string='Firma digital')
    store_id = fields.Many2one(
        'res.store',
        'Tienda',
        context={'user_preference': True},
        help='The store this user is currently working for.'
    )
    store_ids = fields.Many2many(
        'res.store',
        'res_store_users_rel',
        'user_id', 'cid',
        'Stores'
    )

    def create_user(self, records, user_group=None):
        for rec in records:
            # if not rec.user_id:
            user_vals = {
                'name': rec.name,
                'login': rec.email or (rec.name),
                'partner_id': rec.id,

            }
            user_id = self.create(user_vals)
            if user_group:
                user_group.users = user_group.users + user_id

    @api.constrains('groups_id')
    def _check_tech_user(self):

        if self.has_group('base.group_erp_manager') and \
                not self.env['ir.config_parameter'].sudo().get_param('create_tech_user',"False").lower() == "true":
            raise UserError("No puedes asignar permisos de Administracion->Permisos de acceso")
            print("tiene el permiso")
        return True