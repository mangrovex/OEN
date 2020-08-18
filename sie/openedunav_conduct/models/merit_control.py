import time
import logging

from odoo import _, models, fields, api
from odoo.exceptions import ValidationError
from misc import CONTROL_STATE

_logger = logging.getLogger(__name__)


class SieMeritControl(models.Model):
    _name = 'sie.merit.control'
    _description = 'Control of Merits'

    name = fields.Text(string='name', required=True, compute='_compute_display_name',
                       readonly=True, states={'draft': [('readonly', False)]})
    date = fields.Date(string='Date', required=True, readonly=True, states={'draft': [('readonly', False)]})
    course_id = fields.Many2one(comodel_name='sie.course', string='Course', domain="[('state', '=', 'running')]",
                                ondelete='restrict', required=True)
    enrollment_id = fields.Many2one(comodel_name='sie.enrollment', string='Classroom', ondelete='restrict',
                                    domain="[('course_id.state', '!=', 'finalized')]", required=True, readonly=True,
                                    states={'draft': [('readonly', False)]})
    student_id = fields.Many2one(comodel_name='sie.student', string="Student", selection='_get_students', required=True)
    merit_id = fields.Many2one(comodel_name='sie.merit', string='Merit', ondelete='restrict', required=True,
                               readonly=True,
                               states={'draft': [('readonly', False)]})
    kind_id = fields.Many2one(comodel_name='sie.medal.kind', string='Kind of Medal',
                              domain="[('id','=',merit_id.kind_id)]")
    merits = fields.Integer(string='Merits', required=True, readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection(CONTROL_STATE, string='State')
    notes = fields.Text(string='Notes', store=True)
    _order = 'date DESC'

    _defaults = {
        'date': lambda *args: time.strftime('%Y-%m-%d'),
        'merits': lambda *args: 0,
        'state': lambda *args: 'draft',
    }

    @api.multi
    @api.depends('course_id', 'date', 'name', 'enrollment_id')
    def _compute_display_name(self):
        if self.course_id and self.enrollment_id:
            create_date = time.strftime('%Y%m%d-%H%M%S')
            name = '%s - MERITO - %s - %s' % (self.enrollment_id.name,
                                              self.parameter_id.name, create_date)
            self.name = name

    @api.one
    @api.constrains('merits')
    def _check_merits(self):
        if self.merits:
            flag = (self.merits >= self.merit_id.min_merits)
            flag &= (self.merits <= self.merit_id.max_merits)
            if not flag:
                raise ValidationError('Merits should be between min and max')

    @api.onchange('merit_id')
    def onchange_merit(self):
        if self.merit_id:
            self.merits = self.merit_id.min_merits

    def publish(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'published'}, context=context)
        return True

    def settle(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'settled'}, context=context)
        return True

    def action_cancel(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'draft'}, context=context)
        return True

    @api.one
    def copy(self, default=None):
        default = dict(default or {})
        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)
        default['name'] = new_name
        default['state'] = 'draft'
        return super(SieMeritControl, self).copy(default)

    @api.multi
    def unlink(self):
        for record in self:
            if record.state in ('settled'):
                raise Warning(_('You can not delete an merit which was settled'))
        return models.Model.unlink(self)
