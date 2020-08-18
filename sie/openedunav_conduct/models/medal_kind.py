from odoo import _, models, fields


class SieMedalKind(models.Model):
    _name = 'sie.medal.kind'
    _description = 'Kind of Medal'

    name = fields.Char(string='Name', size=96, required=True)

    _order = 'name'

    _sql_constraints = [
        ('name_uk', 'unique(name)', 'Kind of medal must be unique'),
    ]

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default = default.copy()
        current = self.browse(cr, uid, id, context=context)
        default.update({'name': current.name + _(' (Copy)')})
        return super(SieMedalKind, self).copy(cr, uid, id, default, context=context)
