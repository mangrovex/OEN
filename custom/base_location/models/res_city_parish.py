# -*- coding: utf-8 -*-
from odoo import models, fields


class ResCityParish(models.Model):
    _name = 'res.city.parish'
    _description = 'Parroquias'

    city_id = fields.Many2one('res.state.city', ondelete='restrict', string="City Id.", )
    name = fields.Char(string="Parish", )
    code = fields.Char(string="Code", )
