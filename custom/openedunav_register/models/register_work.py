from odoo import models, fields, api


class SieDirectionWork(models.Model):
    _name = 'sie.register.work'
    _description = 'Register work'
    _rec_name = 'work_name'

    name = fields.Char(string='Name', compute='_compute_fullname', store=True)
    work_name = fields.Char(string='Work Name', required=True)
    work_date = fields.Date(string='Work Date', required=True)
    course_id = fields.Many2one('sie.course', string='Course', ondelete='restrict',
                                required=True, domain=[('state', '!=', 'finalized')])
    work_type = fields.Selection(string='Work Type', selection=[('direction', 'Direction'),
                                                                ('aprovechamiento', 'Aprovechamiento')], required=True)
    faculty_ids = fields.Many2many('sie.faculty', string='Faculties', required=True, ondelete='restrict')

    _order = 'name, course_id'

    _sql_constraints = [
        ('name_uk', 'unique(name, course_id)', 'Name must be unique per course'),
    ]

    @api.one
    @api.depends('course_id', 'work_name')
    def _compute_fullname(self):
        if self.course_id:
            fullname = '%s %s' % (self.course_id.name, self.work_name)
            self.name = fullname
