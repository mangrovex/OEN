from odoo import models, fields


class SieExemptKind(models.Model):
    _name = 'sie.exempt.kind'
    _description = 'Kind of Exempt'

    name = fields.Char('Kind of Exempt', size=96, required=True)

    _order = 'name'

    _sql_constraints = [
        ('name_uk', 'unique(name)', 'Kind of exempt must be unique'),
    ]
