from odoo import _, models, fields


class SieCourseName(models.Model):
    _name = 'sie.course.name'
    _description = 'Course Name'

    name = fields.Char(string='Name', required=True)

    _sql_constraints = [
        ('name_level_uk', 'unique(name)', _('Name must be unique per level')),
    ]
