# -*- coding: utf-8 -*
import time
import logging
import icu

from operator import attrgetter
from odoo import _, models, fields, api
from .misc import CONTROL_STATE, SCORE_NUMBER

_logger = logging.getLogger(__name__)

class SiePhysicalProof(models.Model):
    _name = 'sie.physical.proof'
    _description = 'Physical Proof'

    name = fields.Char(string='Nombre', compute='_compute_display_name', store=True)
    date = fields.Date(string='Fecha', required=True)
    notes = fields.Text(string='Notas')
    course_id = fields.Many2one(comodel_name='sie.course', string='Curso', domain="[('state', '=', 'running')]",
                                ondelete='restrict', required=True)
    # enrollment_id = fields.Many2one(comodel_name='sie.enrollment', string='Division', ondelete='restrict',
    #                                 domain="[('course_id', '=', course_id)]")
    student_ids = fields.One2many(comodel_name='sie.physical.proof.student', inverse_name='physical_proof_id',
                                string='Estudiantes')
    #score = fields.Float(string='Puntaje', digits=(16, 2))
    score_number = fields.Selection(SCORE_NUMBER, string='No. Noa')
    state = fields.Selection(CONTROL_STATE, 'State',default='draft')
    is_readonly = fields.Boolean(string='Is readonly?')


    @api.multi
    @api.depends('course_id', 'date')
    def _compute_display_name(self):
        for record in self:
            if record.course_id and record.date:
                create_date = time.strftime('%Y%m%d%H%M%S')
                name = '%s | %s ' % (record.course_id.name, create_date)
                record.name = name

    @api.onchange('course_id')
    def onchange_course_id(self):
        students = []
        enrollment = self.env['sie.enrollment'].search([('course_id', '=', self.course_id.id)])
        student_ids = enrollment.student_ids
        seq = 0
        for student in student_ids:
            if not student.inactive:
                data = {
                    'name': student.ced_ruc,
                    'student_id': student.id,
                    'seq': seq
                }
                students.append(data)
        self.student_ids = students

    # @api.onchange('enrollment_id')
    # def _onchange_enrollment_id(self):
    #     students = []
    #     for student in self.enrollment_id.student_ids:
    #         table_obj = self.env['sie.physical.proof.table']
    #         domain = [('from_included', '<=', student.age)]
    #         domain += [('to_not_included', '>', student.age)]
    #         record = table_obj.search(domain)
    #         data = {
    #             #'name': student.identification_id,
    #             'student_id': student.id,
    #             # 'gender': student.gender,
    #             'table': record.id,
    #             #'run': '-1',
    #             'abdominal': '-1',
    #             'push_ups': '-1',
    #             'swimming': '-1',
    #             'race': '-1',
    #             'climb': '-1',
    #             'flotation': '-1',
    #         }
    #         students.append(data)
    #     self.student_ids = students

    #     def _compute_score(self):
    #     cr.execute("""WITH x (proof_id, score, score_ref) AS (
    #
    # 		SELECT proof_id, sum(score), sum(score_ref)
    # 		FROM sie_physical_proof_score
    # 		WHERE proof_id IN %s
    # 		GROUP BY proof_id
    # 	) SELECT proof_id, 20 * score / score_ref FROM X""", (tuple(ids), ))
    # res = dict(cr.fetchall())
    # for id in ids:
    # obj = self.browse(cr, uid, id)
    # _logger.info(res.get(id, 0))
    #    res[id] = res.get(id, 0)
    # return res

    def publish(self):
        self.write({'state': 'published'})
        return True

    def settle(self):
        self.write({'state': 'settled'})
        return True

    @api.multi
    def load_tables(self):
        for record in self:
            if record.course_id:
                for student in record.student_ids:
                     physical_proof_table = self.env['sie.physical.proof.table'].search([('from_included','<=',student.student_id.age),
                                                                                        ('to_not_included','>=',student.student_id.age)],limit=1)


                     #physical_proof_params = self.env['sie.physical.proof.param'].search([('table_id','=',physical_proof_table.id),
                                                                                       # ('gender','=',student.student_id.gender)])
                     # data_params = []
                     # for param in physical_proof_params:
                     #    data_params.append([0,0,{
                     #        'physical_proof_param_id': param.id,
                     #
                     # student.physical_proof_student_test_ids = data_params

    # @api.model
    # def create(self, values):
    #     e_obj = self.env['sie.enrollment'].browse(values.get('enrollment_id'))
    #     values['course_id'] = e_obj.course_id.id
    #     return super(SiePhysicalProof, self).create(values)

    def copy(self, default=None):
        default = dict(default or {})
        default['state'] = 'draft'
        return super(SiePhysicalProof, self).copy(default)

    # def write(self, values):
    #     record = self[0]
    #     e_obj = record.enrollment_id
    #     if e_obj.course_id:
    #         values['course_id'] = e_obj.course_id.id
    #     return super(SiePhysicalProof, self).write(values)

    @api.multi
    def unlink(self):
        unlink_ids = []
        for record in self:
            if record.state in ('settled'):
                raise models.Model.except_osv(_('Invalid Action!'), _('You can not delete an record which was settled'))
            if record.student_ids:
                for student in record.student_ids:
                    student.physical_proof_student_table_id.unlink()
        return super(SiePhysicalProof, self).unlink()

    @api.multi
    def sort_by_name(self):
        for record in self:
             collator = icu.Collator.createInstance(icu.Locale('es'))
             # student_ids = sorted(record.student_ids,key=attrgetter('last_name','mother_name','first_name','middle_name'),cmp=collator.compare)
             student_ids = sorted(record.student_ids,key=attrgetter('full_name'),cmp=collator.compare)
             seq = 0
             for student in student_ids:
                 seq += 1
                 student.write({'seq':seq})

    @api.multi
    def sort_by_score(self):
        for record in self:
            student_ids = record.student_ids.sorted(
                key=attrgetter('score'), reverse=True)
            seq = 0
            for student in student_ids:
                seq += 1
                student.write({'seq': seq})
