from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SiePhysicalProofTable(models.Model):
    _name = 'sie.physical.proof.table'
    _description = 'Table'

    name = fields.Integer('Table', required=True)
    from_included = fields.Integer('From', required=True, help='Included')
    to_not_included = fields.Integer('To', required=True, help='Not included')

    _order = 'name'

    _sql_constraints = [
        ('name_uk', 'unique(name)', 'Test must be unique'),
    ]

    @api.one
    @api.constrains('from_included')
    def _check_from_included(self):
        if self.from_included:
            if self.from_included <= 0:
                raise ValidationError('"From" must be greater than 0')

    @api.one
    @api.constrains('name')
    def _check_name(self):
        if self.name:
            if self.name <= 0:
                raise ValidationError('"Name" must be greater than 0')

    @api.one
    @api.constrains('to_not_included')
    def _check_to_not_included(self):
        if self.to_not_included and self.from_included:
            if self.to_not_included < self.from_included:
                raise ValidationError('"To" must be greater than "from"')

    @api.multi
    @api.constrains('score')
    def validate_score(self):
        for record in self:
            if record.score < 0.0 or record.score > 20:
                raise ValidationError(record.student_id.name + ' revisar Nota ' + str(record.score))