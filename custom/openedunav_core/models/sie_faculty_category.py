# -*- coding: utf-8 -*-
# Copyright (C) 2009-TODAY Manexware S.A.

from odoo import fields, models


class FacultyCategory(models.Model):

    _name = "sie.faculty.category"
    _description = "Faculty Category"

    name = fields.Char(string="Category Name", required=True)
    code = fields.Integer(string='Code')
    # faculty_ids = fields.Many2many(
    #     'sie.faculty',
    #     'faculty_category_rel',
    #     'category_id',
    #     'emp_id',
    #     string='Faculties'
    # )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Category name already exists !"),
    ]
