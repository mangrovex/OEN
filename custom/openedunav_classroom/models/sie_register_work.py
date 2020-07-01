from odoo import models, fields, api


class SieDirectionWork(models.Model):
    _name = 'sie.register.work'
    _description = 'Register work'
    _rec_name = 'work_name'
    _order = 'name, course_id'

    name = fields.Char(
        string='Name',
        compute='_compute_fullname',
        store=True
    )
    work_name = fields.Char(
        string='Work Name',
        required=True
    )
    work_date = fields.Date(
        string='Work Date',
        required=True
    )
    course_id = fields.Many2one(
        'sie.course',
        string='Course',
        ondelete='restrict',
        required=True,
        domain=[('state', '!=', 'finalized')]
    )
    work_type = fields.Selection(
        string='Work Type',
        selection=
        [
            ('direction', 'Direction'),
            ('aprovechamiento', 'Aprovechamiento')
        ],
        required=True
    )
    faculty_ids = fields.Many2many(
        'sie.faculty',
        string='Faculties',
        required=True,
        ondelete='restrict'
    )

    _sql_constraints = [
        ('name_uk', 'unique(name, course_id)', 'Name must be unique per course'),
    ]

    @api.depends('course_id', 'work_name')
    def _compute_fullname(self):
        for record in self:
            if record.course_id:
                fullname = '%s %s' % (record.course_id.name, record.work_name)
                record.name = fullname
