# -*- coding: utf-8 -*-

from odoo import fields, models


class ResStateCity(models.Model):
    _name = 'res.state.city'
    _description = "City models"

    state_id = fields.Many2one('res.country.state', 'State', required=True)
    name = fields.Char('Name', size=64, required=True)
    code = fields.Char('Code', size=4, required=True)

