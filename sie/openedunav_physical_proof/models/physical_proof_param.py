import logging

from odoo import _, models, fields, api
from odoo.exceptions import ValidationError
import odoo.addons.decimal_precision as dp
from misc import GENDER, MEASURE_UNIT, TIME_CONTROL, time_value_pattern, number_value_pattern

_logger = logging.getLogger(__name__)

GENDER_EC = {
    'male':'hombres',
    'female':'mujeres'
}


class SiePhysicalProofParam(models.Model):
    _name = 'sie.physical.proof.param'
    _description = 'Parameter'

    name = fields.Char(string='Name', compute='_compute_display_name', store = True)
    test_id = fields.Many2one('sie.physical.proof.test', 'Test', ondelete='restrict', required=True)
    table_id = fields.Many2one('sie.physical.proof.table', 'Table', ondelete='restrict', required=True)
    gender = fields.Selection(GENDER, 'Gender', required=True ,default = 'male')
    measure = fields.Selection(MEASURE_UNIT, 'Unit of Measure', required=True , default = 'time')
    control = fields.Selection(TIME_CONTROL, 'Type of Control', default = 'between')
    value = fields.Char('Value', size=8, required=True)
    int_value = fields.Integer(compute='_get_int_value', string='Value', store=True, multi='compute')
    max_value = fields.Char('Maximum Value', size=8)
    int_max_value = fields.Integer(compute='_get_int_value', string='Value', store=True, multi='compute')
    coefficient = fields.Float('Coefficient', digits=dp.get_precision('Coefficient'), default = 0)


    _sql_constraints = [
        ('param_uk', 'unique(test_id, table_id, gender)', 'Parameter must be unique'),
        ('coefficient_ck', 'check(coefficient >= 0)', 'Coefficient must be greater than or equal to 0'),
    ]

    @api.multi
    @api.depends('test_id', 'table_id','gender')
    def _compute_display_name(self):
        for record in self:
            if record.test_id and record.table_id and record.gender:
                name =  _('Tabla') +" "+ str(record.table_id.name) +" "+ GENDER_EC[record.gender] +" "+ record.test_id.name
                record.name = name

    @api.one
    @api.depends('measure', 'value')
    def _get_int_value(self):
        if self.int_value:
            if self.measure == 'time':
                m, s = self.value.split(',')
                seconds = (int(m) * 60) + int(s)
                self.int_value = seconds
                if self.max_value:
                    m, s = self.max_value.split(',')
                    seconds = (int(m) * 60) + int(s)
                    self.int_max_value = seconds
            else:
                value = int(self.value)
                self.int_value = value

    @api.one
    @api.constrains('value', 'measure')
    def _check_value(self):
        if self.value:
            match = False
            if self.measure == 'time':
                match = time_value_pattern.match(self.value)
            else:
                match = number_value_pattern.match(self.value)
            if not match:
                raise ValidationError('Valor con error')

