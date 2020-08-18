from odoo import models, fields, api


class SieTimekeeping(models.Model):
    _name = 'sie.timekeeping'
    _description = 'Timekeeping'

    name = fields.Char(
        string='Name',
        compute='_compute_name',
        store=True
    )
    course_id = fields.Many2one(
        'sie.course',
        string='Course',
        required=True,
        ondelete='restrict'
    )
    module_id = fields.Many2one(
        'sie.module',
        string='module',
        required=True,
        domain="[('course_id', '=', course_id),('state', '=', 'r')]",
        ondelete='restrict'
    )
    faculty = fields.Char(
        compute='_compute_faculty',
        store=True
    )
    date = fields.Datetime(
        'Date',
        required=True
    )
    number_of_hours = fields.Integer(
        'Number of Hours',
        required=True
    )
    knowledge_id = fields.Many2one(
        'sie.knowledge',
        string='Learning knowledges',
        required=True,
        domain="[('module_ref','=',module_id),('last_child', '=', True)]",
        ondelete='restrict'
    )

    @api.depends('course_id', 'module_id', 'knowledge_id')
    def _compute_name(self):
        for record in self:
            if record.course_id and record.module_id and record.knowledge_id:
                record.name = '%s %s %s' % (record.course_id.name, record.module_id.name, record.knowledge_id.name)

    @api.depends('module_id')
    def _compute_faculty(self):
        for record in self:
            if record.module_id:
                record.faculty = record.module_id.faculty_id.name

    @api.model
    def create(self, vals):
        module_id = self.env['sie.module'].search([('id', '=', vals['module_id'])])
        hours = module_id.running_hours + vals['number_of_hours']
        module_id.sudo().write({'running_hours': hours})
        return super(SieTimekeeping, self).create(vals)

    def write(self, vals):
        for record in self:
            # timekeeping = self.env['sie.timekeeping'].search([('module_id', '=', vals['module_id'])])
            # hours_before = sum(record.number_of_hours for record in timekeeping)
            if 'number_of_hours' in vals:
                module_id = record.env['sie.module'].search([('id', '=', record.module_id.id)])
                hours = module_id.running_hours + vals['number_of_hours'] - record.number_of_hours
                module_id.sudo().write({'running_hours': hours})
            return super(SieTimekeeping, record).write(vals)

    def unlink(self):
        for obj in self:
            module_id = self.env['sie.module'].search([('id', '=', obj.module_id.id)])
            hours = module_id.running_hours - obj.number_of_hours
            module_id.sudo().write({'running_hours': hours})
        return super(SieTimekeeping, self).unlink()
