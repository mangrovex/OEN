from odoo import models, fields


class SieFaultSuggestedSanction(models.Model):
    _name = 'sie.fault.suggested.sanction'
    _description = 'Suggested Sanctions'

    name = fields.Char(string='Suggested Sanction', required=True)
    classification_id = fields.Many2one(comodel_name='sie.fault.classification', string='Classification of Fault',
                                        ondelete='cascade')

    _sql_constraints = [
        ('name_uk', 'unique(name, classification_id)', 'Suggested sanction must be unique'),
    ]
