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
    _inherit = ['person.abstract.entity']
    _order = 'full_name'

    category_id = fields.Many2one(
        'sie.faculty.category',
        u'Categoría',
        ondelete='restrict'
    )

    def create_employee(self):
        for record in self:
            vals = {
                'name': record.name,
                'country_id': record.nationality.id,
                'gender': record.gender,
                'address_home_id': record.partner_id.id
            }
            emp_id = self.env['hr.employee'].create(vals)
            record.write({'emp_id': emp_id.id})
            record.partner_id.write({'partner_share': True, 'employee': True})

    @api.model
    def create(self, vals):
        self.env['ir.config_parameter'].sudo().set_param('sie_entity.global.variable', 'sie_faculty')
        return super(SieFaculty, self).create(vals)

    @api.onchange('ced_ruc')
    def _onchange_ced_ruc(self):
        for rec in self:
            if rec.ced_ruc:
                ced_ruc = rec.ced_ruc.replace('-', '')
                rec.ced_ruc = ced_ruc
                if not ci.is_valid(ced_ruc):
                    if rec.type_ced_ruc == 'cedula':
                        raise ValidationError('CI [%s] no es valido !' % ced_ruc)
                    elif rec.type_ced_ruc == 'ruc':
                        raise ValidationError('RUC [%s] no es valido !' % ced_ruc)
