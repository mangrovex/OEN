import time
import logging

from odoo import _, models, fields, api
from odoo.exceptions import ValidationError
from .misc import CONTROL_STATE, SCORE_NUMBER
from operator import attrgetter

_logger = logging.getLogger(__name__)


class SieIntegratorProduct(models.Model):
    _name = 'sie.integrator.product'
    _description = 'Integrator Product'
    _rec_name = 'parameter_id'

    name = fields.Char(compute='_compute_name', store=True)
    notes = fields.Text(string='Notes')
    course_id = fields.Many2one('sie.course', string='Course', ondelete='restrict', required=True,
                                domain="[('state', '=', 'running')]")
                                # domain="[('state', '=', 'running'),"
                                #        "('statistician.user_id','=',uid)]")
    parameter_id = fields.Many2one('sie.matrix.parameter', string='Parameter', ondelete='restrict',
                                   domain="[('last_child', '=', True),"
                                          "('parent_ref', 'like', '013'),"
                                          "('type', '=', False),"
                                          "('course_ref', '=', matrix_id)]",
                                   required=True)
    student_ids = fields.One2many('sie.integrator.product.student', inverse_name='score_id',
                                  string='Students', store=True)
    state = fields.Selection(CONTROL_STATE, string='State', default='draft')
    parameter_id_name = fields.Char(compute='_compute_parameter_id_name')
    matrix_id = fields.Many2one("sie.matrix", compute='_compute_matrix', ondelete='restrict')
    judge_id = fields.Many2one("sie.faculty", string="Judge", ondelete='restrict')
    score_number = fields.Selection(SCORE_NUMBER, string='Score', required=True)

    _order = 'score_number'

    _sql_constraints = [
        ('name_uk', 'unique(name)', 'Record must be unique'),
    ]

    @api.onchange('parameter_id')
    def onchange_parameter_id(self):
        if self.parameter_id.parent_ref:
            if not '014' in self.parameter_id.parent_ref:
                students = []
                enrollment = self.env['sie.enrollment'].search([('name', '=', self.course_id.name)])
                student_ids = enrollment.student_ids.sorted(key=attrgetter('last_name_1', 'last_name_2'))
                for student in student_ids:
                    if not student.inactive:
                        data = {
                            'name': student.identification_id,
                            'student_id': student.id,
                        }
                        students.append(data)
                self.student_ids = students
            else:
                self.student_ids = ''

    @api.one
    def publish(self):
        self.state = 'published'

    @api.one
    def settle(self):
        self.state = 'settled'

    @api.multi
    def unlink(self):
        unlink_ids = []
        for record in self:
            if record.state in 'settled':
                raise models.Model.except_osv(_('Invalid Action!'), _('You can not delete an record which was settled'))
            else:
                unlink_ids.append(record.id)
            if record.score_number:
                if not record.score_number == "1":
                    data = self.env['sie.integrator.product'].search(
                        [('course_id', '=', record.course_id.id), ('parameter_id', '=', record.parameter_id.id),
                         ('judge_id', '=', record.judge_id.id), ('score_number', '=', int(record.score_number) + 1)])
                    if data:
                        raise ValidationError("Debes borrar primero la nota " + str(int(record.score_number) + 1))
        return super(SieIntegratorProduct, self).unlink()

    @api.multi
    @api.depends('parameter_id')
    def _compute_parameter_id_name(self):
        if self.parameter_id:
            self.parameter_id_name = self.parameter_id.name
            if not '014' in self.parameter_id.parent_ref:
                self.has_war_games = False
            else:
                self.has_war_games = True

    @api.depends('course_id')
    def _compute_matrix(self):
        if self.course_id:
            self.matrix_id = self.course_id.matrix_id

    @api.one
    @api.depends('course_id', 'parameter_id', 'judge_id', 'score_number')
    def _compute_name(self):
        name = '%s,%s,%s,%s,%s,%s' % (self.course_id.id, self.parameter_id.id,
                                      self.judge_id.id, self.score_number)
        self.name = name

    @api.one
    @api.constrains('score_number')
    def _check_score(self):
        if self.score_number:
            if not self.score_number == "1":
                data = self.env['sie.integrator.product'].search(
                    [('course_id', '=', self.course_id.id), ('parameter_id', '=', self.parameter_id.id),
                    ('judge_id', '=', self.judge_id.id), ('score_number', '=', int(self.score_number) - 1)])
                if not data:
                    raise ValidationError("Falta nota " + str(int(self.score_number) - 1))
