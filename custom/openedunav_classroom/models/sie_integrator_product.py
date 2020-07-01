import time
import logging

from odoo import _, models, fields, api
from odoo.exceptions import ValidationError
from operator import attrgetter

_logger = logging.getLogger(__name__)


class SieIntegratorProduct(models.Model):
    _name = 'sie.integrator.product'
    _description = 'Integrator Product'
    _rec_name = 'parameter_id'
    _order = 'score_number'

    name = fields.Char(
        compute='_compute_name',
        store=True
    )
    notes = fields.Text(string='Notes')
    course_id = fields.Many2one(
        'sie.course',
        string='Course',
        ondelete='restrict',
        required=True,
        domain="[('state', '=', 'running')]" #        , ('statistician.user_id','=',uid)
    )
    parameter_id = fields.Many2one(
        'sie.matrix.parameter',
        string='Parameter',
        ondelete='restrict',
        domain="[('last_child', '=', True), ('parent_ref', 'like', '013'), "
               "('type', '=', False), ('course_ref', '=', matrix_id)]",
        required=True
    )
    student_ids = fields.One2many(
        'sie.integrator.product.student',
        inverse_name='score_id',
        string='Students', store=True
    )
    state = fields.Selection(
        [
            ('planned', _('PLenned')),
            ('running', _('Running')),
            ('finalized', _('Finalized')),
        ],
        string='State',
        default='draft'
    )
    parameter_id_name = fields.Char(
        compute='_compute_parameter_id_name'
    )
    matrix_id = fields.Many2one(
        "sie.matrix",
        compute='_compute_matrix',
        ondelete='restrict'
    )
    judge_id = fields.Many2one(
        "sie.faculty",
        string="Judge",
        ondelete='restrict'
    )
    score_number = fields.Selection(
        [
            ('1', 'Note 1'),
            ('2', 'Note 2'),
            ('3', 'Note 3'),
            ('4', 'Note 4'),
            ('5', 'Note 5'),
            ('6', 'Note 6'),
            ('7', 'Note 7'),
            ('8', 'Note 8'),
            ('9', 'Note 9'),
            ('10', 'Note 10'),
            ('11', 'Note 11'),
            ('12', 'Note 12'),
            ('13', 'Note 13'),
            ('14', 'Note 14'),
            ('15', 'Note 15'),
            ('16', 'Note 16'),
            ('17', 'Note 17'),
        ],
        string='Score',
        required=True
    )

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

    def publish(self):
        for record in self:
            record.state = 'published'

    def settle(self):
        for record in self:
            record.state = 'settled'

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

    @api.depends('parameter_id')
    def _compute_parameter_id_name(self):
        for record in self:
            if record.parameter_id:
                record.parameter_id_name = record.parameter_id.name
                if not '014' in record.parameter_id.parent_ref:
                    record.has_war_games = False
                else:
                    record.has_war_games = True

    @api.depends('course_id')
    def _compute_matrix(self):
        if self.course_id:
            self.matrix_id = self.course_id.matrix_id

    @api.depends('course_id', 'parameter_id', 'judge_id', 'score_number')
    def _compute_name(self):
        for record in self:
            name_concat = '{}},{},{},{}}'
            record.name = name_concat.format(record.course_id.id, record.parameter_id.id, record.judge_id.id,
                                             record.score_number)

    @api.constrains('score_number')
    def _check_score(self):
        for record in self:
            if record.score_number:
                if not record.score_number == "1":
                    data = record.env['sie.integrator.product'].search(
                        [('course_id', '=', record.course_id.id), ('parameter_id', '=', record.parameter_id.id),
                         ('judge_id', '=', record.judge_id.id), ('score_number', '=', int(record.score_number) - 1)])
                    if not data:
                        raise ValidationError("Falta nota " + str(int(record.score_number) - 1))
