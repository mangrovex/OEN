# -*- coding: utf-8 -*
from odoo import _, models, fields, api


class SieCourseScore(models.Model):
    _name = 'sie.course.score'
    _description = 'Notas Curso'

    name = fields.Char(string='Nombre')