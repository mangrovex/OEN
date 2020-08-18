from odoo import models, fields, api
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError
from misc import GENDER, MEASURE_UNIT, TIME_CONTROL, time_value_pattern, number_value_pattern

class SiePhysicalProofStudent(models.Model):
    _name = 'sie.physical.proof.student'
    _description = 'Student\'s Physical Proof Score'
    _rec_name = 'student_id'

    student_id = fields.Many2one(comodel_name='sie.student', string='Estudiantes', ondelete='restrict',
                                 required=True, store=True)
    # grade = fields.Char(string='Grade', store=True)
    # #gender = fields.Char(string='Gender', store=True)
    # gender = fields.Selection(GENDER, 'Gender')
    #table = fields.Integer(string='Table', store=True)
    # table = fields.Many2one(comodel_name='sie.physical.proof.table', string='Table', store=True)
    #run = fields.Char(string='run', required=True, compute='_check_run')
    #run = fields.Char(string='run', required=True)
    # abdominal = fields.Char(string='Score Abdominal', required=True)
    # push_ups = fields.Char(string='Score Push-Ups', required=True) #felexion de pecho
    # swimming = fields.Char(string='Swimming', required=True) #natacion
    # race = fields.Char(string='Score Race', required=True) #carrera
    # climb = fields.Char(string='Score Climb', required=True) #cabo
    # flotation = fields.Boolean(string='Score Flotation', required=True) # flotacion
    #score = fields.Float(string='Puntaje',compute='_compute_score', digits=dp.get_precision('Score'), store = True )#puntaje
    score = fields.Float('Nota', digits=dp.get_precision('Score'))
    full_name = fields.Char("Nombre", related='student_id.full_name', store=True)
    seq = fields.Integer('No.')
    # score = fields.Float(compute='_compute_score_total', string='Score',
    #                      digits=dp.get_precision('Score'), store=True)
    # time = fields.Many2one('sie.time.proof')
    physical_proof_id = fields.Many2one(comodel_name='sie.physical.proof', string='Pruebas fisicas ID',
                                        ondelete='cascade')
    physical_proof_student_table_id = fields.Many2one('sie.physical.proof.student.table',
                                                      # compute = '_compute_physical_proof_student_table_id',
                                                      ondelete='cascade',
                                                      # store = True,
                                                      string = 'Puntaje',
                                                      domain="[('physical_proof_student_id','=',id)]")
                                                      # inverse = '_inverse_physical_proof_student_table_id')
    # physical_proof_student_test_ids = fields.One2many('sie.physical.proof.student.test',
    #                                                   string='Pruebas',
    #                                                   inverse_name='physical_proof_student_id')

    _order = 'seq'

    @api.multi
    @api.depends('physical_proof_student_test_ids','physical_proof_student_test_ids.score')
    def _compute_score(self):
        for record in self:
            if record.physical_proof_student_test_ids:
                score = 0
                nota = 0.0
                for test in record.physical_proof_student_test_ids:
                    nota += float(test.score)
                    score=nota*20/700
                record.score = score

    # @api.onchange('run')
    # def _check_run(self):
    #     match = time_value_pattern.match(self.run)
    #     if not match:
    #         self.run = 'error!'
    # @api.multi
    # def _inverse_physical_proof_student_table_id(self):
    #     pass
    #
    # @api.multi
    # @api.depends('physical_proof_id')
    # def _compute_physical_proof_student_table_id(self):
    #     for record in self:
    #         if record.physical_proof_id:
    #             physical_proof_student_table = self.env['sie.physical.proof.student.table'].create({
    #                 'score': '0'
    #             })
    #             record.physical_proof_student_table_id = physical_proof_student_table.id

    @api.multi
    @api.onchange('abdominal')
    def _check_abdominal(self):
        for record in self:
            if record.abdominal:
                match = number_value_pattern.match(record.abdominal)
                if not match:
                    record.abdominal = 'error!'
    @api.multi
    @api.onchange('push_ups')
    def _check_push_ups(self):
        for record in self:
            if record.push_ups:
               match = number_value_pattern.match(self.push_ups)
            if not match:
                record.push_ups = 'error!'

    @api.multi
    @api.onchange('swimming')
    def _check_swimming(self):
        for record in self:
            if record.swimming:
               match = time_value_pattern.match(self.swimming)
            if not match:
               self.swimming = 'error!'

    @api.multi
    @api.onchange('race')
    def _check_race(self):
        for record in self:
            if record.race:
               match = time_value_pattern.match(self.race)
            if not match:
                self.race = 'error!'

    @api.multi
    @api.onchange('climb')
    def _check_climb(self):
        for record in self:
            if record.climb:
               match = time_value_pattern.match(self.climb)
            if not match:
              self.climb = 'error!'

    # @api.onchange('flotation')
    # def _check_flotation(self):
    #     if self.flotation:
    #        match = time_value_pattern.match(self.flotation)
    #        if not match:
    #          self.flotation = 'error!'

    # @api.multi
    # # @api.depends('run', 'abdominal', 'push_ups', 'swimming', 'race', 'climb', 'flotation')
    # @api.depends('abdominal', 'push_ups', 'swimming', 'race', 'climb', 'flotation')
    # def _compute_score_total(self):
    #     pass
    #     # for record in self:
    #     # # if self.run != 'error!' and self.abdominal != 'error!' and self.push_ups != 'error!' \
    #     # #         and self.swimming != 'error!' and self.race != 'error!' and self.climb != 'error!' \
    #     # #         and self.flotation != 'error!':
    #     #     if record.abdominal != 'error!' and record.push_ups != 'error!' \
    #     #             and record.swimming != 'error!' and record.race != 'error!' and record.climb != 'error!':
    #     #     #total = 0
    #     #     # if int(self.run) > -1:
    #     #     #     total_run = SiePhysicalProofStudent._compute_score(self, self.run)
    #     #     # else:
    #     #     #     total_run = 0
    #     #         if int(record.abdominal) > -1:
    #     #             total_abdominal = SiePhysicalProofStudent._compute_score(self, record.abdominal,"ab")
    #     #         else:
    #     #             total_abdominal = 0
    #     #         if int(record.push_ups) > -1:
    #     #             total_push_ups = SiePhysicalProofStudent._compute_score(self, record.push_ups,"pu")
    #     #         else:
    #     #             total_push_ups = 0
    #     #         minutes, seconds = record.swimming.split(",")
    #     #         if int(minutes) > -1 or int(seconds) > -1:
    #     #             total_swimming = SiePhysicalProofStudent._compute_score(self, record.swimming,"sw")
    #     #         else:
    #     #             total_swimming = 0
    #     #         minutes, seconds = record.race.split(",")
    #     #         if int(minutes) > -1 or int(seconds) > -1:
    #     #             total_race = SiePhysicalProofStudent._compute_score(self, record.race,"ra")
    #     #         else:
    #     #             total_race = 0
    #     #         minutes, seconds = record.climb.split(",")
    #     #         if int(minutes) > -1 or int(seconds) > -1:
    #     #             total_climb = SiePhysicalProofStudent._compute_score(self, record.climb,"cl")
    #     #         else:
    #     #             total_climb = 0
    #     #         # if int(self.flotation) > -1:
    #     #         #     total_flotation = SiePhysicalProofStudent._compute_score(self, self.flotation)
    #     #         # else:
    #     #         #     total_flotation = 0
    #     #
    #     #         if record.flotation:
    #     #             total_flotation = 100
    #     #         else:
    #     #             total_flotation = 0
    #     #     total = total_abdominal + total_push_ups + total_swimming + total_race + total_climb + total_flotation
    #     #     param_obj = self.env['sie.physical.proof.param']
    #     #     domain = [('table_id', '=', self.table.id)]
    #     #     domain += [('gender', '=', self.gender)]
    #     #     param_ids = param_obj.search(domain)
    #     #     score = 0
    #     #     total_ref = 0
    #     #     for rec in param_ids:
    #     #           # test_obj = self.env['sie.physical.proof.test']
    #     #           # domain = [('id', '=', rec.test_id)]
    #     #           # test_id = param_obj.search(domain)
    #     #           # total_ref = total_ref + test_id.score
    #     #           # score = 20 * total / total_ref
    #     #           score = total
    #     #     record.score = score

    # def _compute_score(self, in_value, code):
    #     value = in_value
    #     param_obj = self.env['sie.physical.proof.param']
    #     domain = [('table_id', '=', self.table.id)]
    #     domain += [('gender', '=', self.gender)]
    #     domain += [('test_id.code', '=', code)]
    #     param_ids = param_obj.search(domain)
    #     score = 0
    #     total = 0
    #     for rec in param_ids:
    #         total = 0
    #         test_id = rec.test_id
    #         if rec.measure == 'time':
    #             m, s = in_value.split(',')
    #             seconds = (int(m) * 60) + int(s)
    #             if rec.control == 'exceed':
    #                 # if exceed then 0
    #                 if seconds >= int(rec.value):
    #                     total = test_id.score
    #                 else:
    #                     # (rec.score_ref - (rec.int_value - seconds)) * rec.coefficient
    #                     total = 0
    #             elif rec.control == 'between':
    #                 if seconds <= int(rec.value):
    #                     total = test_id.score
    #                 elif seconds > int(rec.max_value):
    #                     total = 0
    #                 else:
    #                     total = test_id.score - ((seconds - int(rec.value)) / rec.coefficient)
    #             else:  # if not exceed then 0
    #                 if seconds <= int(rec.value):
    #                     total = test_id.score
    #                 else:
    #                     # (rec.score_ref - (seconds - rec.int_value)) * rec.coefficient
    #                     total = 0
    #         else:
    #             value = int(in_value)
    #             if value == 0:
    #                 total = 0
    #             if value >= int(rec.value):
    #                 total = test_id.score
    #             else:
    #                 coefficient = test_id.score / int(rec.value)
    #                 total = value * coefficient
    #     score = score + total
    #     return score

    @api.multi
    def unlink(self):
        for record in self:
            record.physical_proof_student_table_id.unlink()
        return super(SiePhysicalProofStudent, self).unlink()


class SiePhysicalProofStudentTest(models.Model):
    _name = 'sie.physical.proof.student.test'
    _description = 'Student\'s Physical Proof Student test'
    _rec_name = 'score'

    score = fields.Float(string='Puntaje', digits=(16,2), compute='_compute_score', store=True)
    cantidad = fields.Char('Cantidad', default='0')
    physical_proof_student_id = fields.Many2one('sie.phyical.proof.student')
    physical_proof_param_id = fields.Many2one('sie.physical.proof.param')

    @api.multi
    @api.depends("cantidad")
    def _compute_score(self):
        for record in self:
            if record.physical_proof_param_id.measure == 'time':
                if record.cantidad:
                    match = time_value_pattern.match(record.cantidad)
                    #if int(record.cantidad) >=int(record.hysical_proof_param_id.value):
                    #record.score = 100
                    #else:
                    #record.score = =SI((N7*60+O7)<=746,150,SI((N7*60+O7)>=746,150-(((N7*60+O7)-746)*150/505)))
                if not match:
                   raise ValidationError('Error ' + record.physical_proofpy_param_id.name)
                else:
                    minutes, seconds = record.physical_proof_param_id.value.split(',')
                    total_seconds_param = int(minutes) * 60 + int(seconds)
                    minutes, seconds = record.cantidad.split(',')
                    total_seconds = int(minutes) * 60 + int(seconds)
                    if total_seconds <= total_seconds_param:
                        #record.score=150
                        record.score = record.physical_proof_param_id.test_id.score
                    else:
                        record.score = record.physical_proof_param_id.test_id.score - ((total_seconds - total_seconds_param) * record.physical_proof_param_id.test_id.score / 505)
            else:
                if int(record.cantidad) >= int(record.physical_proof_param_id.value):
                    record.score = record.physical_proof_param_id.test_id.score
                else:
                    record.score = record.physical_proof_param_id.test_id.score-((int(record.physical_proof_param_id.value)-int(record.cantidad))*101/int(record.physical_proof_param_id.value))



