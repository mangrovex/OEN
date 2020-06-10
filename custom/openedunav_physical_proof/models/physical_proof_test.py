from odoo import _, models, fields
import odoo.addons.decimal_precision as dp


class SiePhysicalProofTest(models.Model):
    _name = 'sie.physical.proof.test'
    _description = 'Test'

    name = fields.Char('Test', size=96, required=True)
    code = fields.Char()
    score = fields.Float('Score', required=True, digits=dp.get_precision('Score'), default=100)

    _sql_constraints = [
        ('name_uk', 'unique(name)', 'Test must be unique'),
        ('code_uk', 'unique(code)', 'code must be unique'),
        ('score_ck', 'check (score > 0)', 'Score must be greater than 0'),
    ]

    def copy(self, default=None):
        default = dict(default or {})
        default.update({'name': self.name + _(' (Copy)')})
        return super(SiePhysicalProofTest, self).copy(default)
