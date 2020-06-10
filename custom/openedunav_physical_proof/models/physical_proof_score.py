from odoo import models, fields, api
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError
from misc import MEASURE_UNIT, TIME_CONTROL, time_value_pattern, number_value_pattern


class SiePhysicalProofScore(models.Model):
    _name = 'sie.physical.proof.score'
    _description = 'Score'
    _rec_name = 'param_id'

    param_id = fields.Many2one('sie.physical.proof.param', 'Parameter', ondelete='restrict', required=True)
    score_ref = fields.Float('Score', required=True, digits=dp.get_precision('Score'))
    control = fields.Selection(TIME_CONTROL, 'Type of Control', required=True)
    int_value = fields.Integer('Value', required=True)
    int_max_value = fields.Integer('Value', required=True)
    coefficient = fields.Float('Coefficient', digits=dp.get_precision('Coefficient'))
    measure = fields.Selection(MEASURE_UNIT, 'Unit of Measure', required=True)
    value = fields.Char('Value', size=8, required=True)
    score = fields.Float(compute='_compute_score', string='Score', digits=dp.get_precision('Total'),
                         store=True, default=0.0)
    proof_id = fields.Many2one('sie.physical.proof', 'Parent', ondelete='cascade', required=True)

    _sql_constraints = [
        ('score_uk', 'unique(param_id, proof_id)', 'Parameter must be unique'),
    ]

    def _compute_score(self):
        res = {}
        for rec in self:
            total = False
            if rec.measure == 'time':
                m, s = rec.value.split(',')
                seconds = (int(m) * 60) + int(s)
                if rec.control == 'exceed':
                    # if exceed then 0
                    if seconds >= rec.int_value:
                        total = rec.score_ref
                    else:
                        # (rec.score_ref - (rec.int_value - seconds)) * rec.coefficient
                        total = 0
                elif rec.control == 'between':
                    if seconds <= rec.int_value:
                        total = rec.score_ref
                    elif seconds > (rec.int_max_value):
                        total = 0
                    else:
                        total = rec.score_ref - ((seconds - rec.int_value) / rec.coefficient)
                else:  # if not exceed then 0
                    if seconds <= rec.int_value:
                        total = rec.score_ref
                    else:
                        # (rec.score_ref - (seconds - rec.int_value)) * rec.coefficient
                        total = 0
            else:
                value = int(rec.value)
                if value == 0:
                    total = 0
                if value >= rec.int_value:
                    total = rec.score_ref
                else:
                    coefficient = rec.score_ref / rec.int_value
                    total = value * coefficient
            res[rec.id] = total
        return res

    @api.constrains(value)
    def _check_value(self):
        match = False
        if self.measure == 'time':
            match = time_value_pattern.match(self.value)
        else:
            match = number_value_pattern.match(self.value)
        if not match:
            raise ValidationError('Value is not valid')
