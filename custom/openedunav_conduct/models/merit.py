import logging

from odoo import models, fields
from misc import KIND_OF_MERIT

_logger = logging.getLogger(__name__)


class SieMerit(models.Model):
    _name = 'sie.merit'
    _description = 'Merits'

    name = fields.Char(string='Merit', size=96, required=True)
    kind_of_merit = fields.Selection(KIND_OF_MERIT, 'Kind of Merit', required=True)
    kind_id = fields.Many2one(comodel_name='sie.medal.kind', string='Kind of Medal', ondelete='restrict')
    min_merits = fields.Integer(string='Minimum Merits')
    max_merits = fields.Integer(string='Merits Maximum')

    _defaults = {
        'kind_of_merit': lambda *args: 'medal',
        'min_merits': lambda *args: 0,
        'max_merits': lambda *args: 0,
    }

    _sql_constraints = [
        ('merit_uk', 'unique(name, kind_of_merit, kind_id)', 'Merit must be unique'),
        ('min_merits_ck', 'check(min_merits >= 0)', 'Merits minimum must be greater or equal to 0'),
        ('max_merits_ck', 'check(max_merits >= min_merits)',
         'Merits maximum must be greater than or equal to minimum merit'),
    ]
