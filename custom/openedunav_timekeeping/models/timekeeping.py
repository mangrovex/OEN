from odoo import models, fields, api


class SieTimekeeping(models.Model):
    _name = 'sie.timekeeping'
    _description = 'Timekeeping'

    name = fields.Char(string='Name', compute='_compute_name', store=True)
    course_id = fields.Many2one('sie.course', string='Course', required=True, ondelete='restrict')
    subject_id = fields.Many2one('sie.subject', string='Subject', required=True,
                                 domain="[('course_id', '=', course_id),('state', '=', 'r')]", ondelete='restrict')
    faculty = fields.Char(compute='_compute_faculty', store=True)
    date = fields.Datetime('Date', required=True)
    number_of_hours = fields.Integer('Number of Hours', required=True)
    unit_id = fields.Many2one('sie.subject.unit', string='Learning Units', required=True,
                              domain="[('subject_ref','=',subject_id),('last_child', '=', True)]", ondelete='restrict')

    @api.one
    @api.depends('course_id', 'subject_id', 'unit_id')
    def _compute_name(self):
        if self.course_id and self.subject_id and self.unit_id:
            self.name = '%s %s %s' % (self.course_id.name, self.subject_id.name, self.unit_id.name)

    @api.one
    @api.depends('subject_id')
    def _compute_faculty(self):
        if self.subject_id:
            self.faculty = self.subject_id.faculty_id.name

    @api.model
    def create(self, vals):
        subject_id = self.env['sie.subject'].search([('id', '=', vals['subject_id'])])
        hours = subject_id.running_hours + vals['number_of_hours']
        subject_id.sudo().write({'running_hours': hours})

        return super(SieTimekeeping, self).create(vals)

    @api.multi
    def write(self, vals):
        # timekeeping = self.env['sie.timekeeping'].search([('subject_id', '=', vals['subject_id'])])
        # hours_before = sum(record.number_of_hours for record in timekeeping)
        if 'number_of_hours' in vals:
            subject_id = self.env['sie.subject'].search([('id', '=', self.subject_id.id)])
            hours = subject_id.running_hours + vals['number_of_hours'] - self.number_of_hours
            subject_id.sudo().write({'running_hours': hours})

        return super(SieTimekeeping, self).write(vals)

    @api.multi
    def unlink(self):
        for obj in self:
            subject_id = self.env['sie.subject'].search([('id', '=', obj.subject_id.id)])
            hours = subject_id.running_hours - obj.number_of_hours
            subject_id.sudo().write({'running_hours': hours})

        return super(SieTimekeeping, self).unlink()
