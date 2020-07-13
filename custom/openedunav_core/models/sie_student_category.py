# -*- coding: utf-8 -*-
# Copyright (C) 2009-TODAY Manexware S.A.

from odoo import fields, models


class StudentCategory(models.Model):

    _name = "sie.student.category"
    _description = "Student Category"

    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(string='Color Index')
    student_ids = fields.Many2many('sie.student', 'student_category_rel', 'category_id', 'emp_id', string='Students')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]
