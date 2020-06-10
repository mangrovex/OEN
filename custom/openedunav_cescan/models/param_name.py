from odoo import _, models, fields


class SieParamName(models.Model):
    _name = 'sie.param.name'
    _description = 'Matrix Parameter Name'

    name = fields.Char(string='Name', required=True)
    short_name = fields.Char(String='Short Name')
    code = fields.Char(required=True)

    _sql_constraints = [
        ('name_level_uk', 'unique(name,short_name)', _('Parameter must be unique')),
        ('code_uk', 'unique(code)', _('Code must be unique')),
    ]
