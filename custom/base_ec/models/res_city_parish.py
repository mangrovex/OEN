# -*- coding: utf-8 -*-
from odoo import models, fields


class ResCityParish(models.Model):
    _name = 'res.city.parish'
    _description = 'Parroquias'

    city_id = fields.Many2one('res.state.city', ondelete='restrict', string="Ciudad", )
    name = fields.Char(string="Parroquia", )
    code = fields.Char(string="Código", )
