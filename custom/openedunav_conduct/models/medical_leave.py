import time
import logging

from odoo import _, models, fields, api
from misc import CONTROL_STATE

_logger = logging.getLogger(__name__)


class SieMedicalLeave(models.Model):
    _name = 'sie.medical.leave'
    _description = 'Medical Leave'

    name = fields.Char(string='Name', compute='_compute_display_name', store=True)
    diagnosis = fields.Text(string='Diagnosis', size=96, required=True, readonly=True,
                            states={'draft': [('readonly', False)]})
    date = fields.Datetime(string='Date', required=True, readonly=True, states={'draft': [('readonly', False)]})
    course_id = fields.Many2one(comodel_name='sie.course', string='Course', ondelete='restrict', required=True,
                                readonly=True, domain="[('state', '=', 'running')]",
                                states={'draft': [('readonly', False)]})
    enrollment_id = fields.Many2one(comodel_name='sie.enrollment', string='Classroom', ondelete='restrict',
                                    domain="[('course_id', '=', course_id)]", required=True, readonly=True,
                                    states={'draft': [('readonly', False)]})
    student_id = fields.Many2one(comodel_name='sie.student', string="Student", required=True)
    hours = fields.Integer(string='Hours', required=True, readonly=True, states={'draft': [('readonly', False)]})
    time = fields.Char(compute='_compute_time', string='Time')
    can_attend = fields.Boolean(string='Can Attend Class?', readonly=True,
                                states={'draft': [('readonly', False)]})
    reason_ids = fields.Many2many(comodel_name='sie.exempt.kind', string='Reasons to Exempt',
                                  readonly=True, states={'draft': [('readonly', False)]})
    notes = fields.Text(string='Notes')
    state = fields.Selection(CONTROL_STATE, string='State')

    _order = 'date DESC'

    _defaults = {
        'date': lambda *args: time.strftime('%Y-%m-%d %H:%M:%S'),
        'state': lambda *args: 'draft',
        'hours': lambda *args: 1,
        'can_attend': lambda *args: True,
    }

    _sql_constraints = [
        ('hours_ck', 'check(hours > 0)', 'Hours must be greater than 0'),
    ]

    # @api.onchange('enrollment_id')
    # @api.one
    # @api.depends('enrollment_id.student_ids')
    # def _compute_student(self):
    #     if self.enrollment_id:
    #         query = """SELECT sie_student_id
    #         FROM sie_enrollment_sie_student_rel
    #         WHERE sie_enrollment_id = %s"""
    #         self._cr.execute(query, (self.enrollment_id.id,))
    #         ids = [row[0] for row in self._cr.fetchall()]
    #         _logger.warning(ids)
    #         students = self.env['sie.student'].search([('id', 'in', ids)])
    #         _logger.warning(students)
    #         # students = []
    #         # for student in data:
    #         #     _logger.warning(student.display_title_name)
    #         #     students.append(student)
    #         self.student_id = students
    #         # return students
    #
    # @api.multi
    # @api.depends('enrollment_id', 'student_id', 'name')
    # def _compute_display_name(self):
    #     if self.enrollment_id and self.student_id:
    #         create_date = time.strftime('%Y%m%d-%H%M%S')
    #         name = '%s - %s - %s' % (self.enrollment_id.name, self.student_id.identification_id, create_date)
    #         self.name = name

    @api.one
    @api.depends('hours')
    def _compute_time(self):
        if self.hours:
            time_str = ''
            if (self.hours % 24) == 0:
                days = self.hours / 24
                time_str = '%s %s' % (days, days == 1 and _('Day') or _('Days'))
            else:
                time_str = '%s %s' % (self.hours, self.hours == 1 and _('Hour') or _('Hours'))
            self.time = time_str

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
        return super(SieMedicalLeave, self).copy(default)

    @api.multi
    def unlink(self):
        for record in self:
            if record.state in ('settled'):
                raise Warning(_('You can not delete an medical leave which was settled'))
        return models.Model.unlink(self)
