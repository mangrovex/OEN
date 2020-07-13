import time
import logging

from odoo import _, models, fields, api
from misc import CONTROL_STATE

_logger = logging.getLogger(__name__)


class SieSanctionControl(models.Model):
    _name = 'sie.sanction.control'
    _description = 'Control of Sanctions'

    name = fields.Char(string='Name', compute='_compute_display_name')
    date = fields.Date(string='Date', required=True, readonly=False, states={'settled': [('readonly', True)]})
    course_id = fields.Many2one(comodel_name='sie.course', string='Course', ondelete='restrict',
                                domain="[('state', '!=', 'finalized')]", required=True, readonly=False,
                                states={'settled': [('readonly', True)]})
    enrollment_id = fields.Many2one(comodel_name='sie.enrollment', string='Division', ondelete='restrict',
                                    domain="[('course_id', '=', course_id)]", required=True, readonly=False,
                                    states={'settled': [('readonly', True)]})
    student_id = fields.Many2one(comodel_name='sie.student', string='Student', ondelete='restrict',
                                 required=True, readonly=False, selection='_get_students',
                                 states={'settled': [('readonly', True)]})
    article_id = fields.Many2one(comodel_name='sie.fault.article', string='Article', ondelete='restrict',
                                 required=True, readonly=False,
                                 states={'settled': [('readonly', True)]})
    classification_id = fields.Many2one('sie.fault.classification', related='article_id.classification_id',
                                        string='Classification of Fault', store=True)
    literal_id = fields.Many2one('sie.fault.literal', 'Literal', ondelete='restrict',
                                 domain="[('article_id', '=', article_id)]", required=True, readonly=False,
                                 states={'settled': [('readonly', True)]})
    acts = fields.Text('Acts')
    punisher_id = fields.Many2one(comodel_name='sie.faculty', string='Punisher', ondelete='restrict', required=True,
                                  readonly=False, domain="[('type', '=', 'military')]",
                                  states={'settled': [('readonly', True)]}, store=True)
    sanction_id = fields.Many2one(comodel_name='sie.fault.sanction', string='Sanction', ondelete='restrict',
                                  domain="[('classification_id', '=', classification_id)]", required=True,
                                  readonly=False, states={'settled': [('readonly', True)]})
    demerits = fields.Integer('sie.fault.sanction', related='sanction_id.demerits', String='Demerit', store=True)
    state = fields.Selection(CONTROL_STATE, 'State')
    number = fields.Char('No Memo', size=96)
    officer_id = fields.Many2one('sie.faculty', 'Officer', ondelete='set null')

    _order = 'date DESC'

    _defaults = {
        'date': lambda *args: time.strftime('%Y-%m-%d'),
        'state': lambda *args: 'draft',
    }

    @api.multi
    @api.depends('enrollment_id', 'student_id')
    def _compute_display_name(self):
        if self.enrollment_id and self.student_id:
            create_date = time.strftime('%Y%m%d%H%M%S')
            name = '%s - %s - %s' % (self.enrollment_id.name, self.student_id.identification_id, create_date)
            self.name = name

    @api.multi
    @api.depends('enrollment_id')
    def _get_students(self):
        if self.enrollment_id:
            students = []
            for student in self.enrollment_id.student_ids:
                students.append(student)
            self.student_id = students

    def publish(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'published'}, context=context)
        return True

    def settle(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'settled'}, context=context)
        return True

    def action_cancel(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'draft'}, context=context)
        return True

    @api.multi
    def print_report(self):
        return self.env['report'].get_action(self, 'OpenEduFrog.sanction_control_report')

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
        return super(SieSanctionControl, self).copy(default)

    @api.multi
    def unlink(self):
        for record in self:
            if record.state in ('settled'):
                raise Warning(_('You can not delete an sanction which was settled'))
        return models.Model.unlink(self)
