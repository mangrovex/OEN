from odoo import models, fields, api


class SieFaultKind(models.Model):
    _name = 'sie.fault.kind'
    _description = 'Kind of Fault'

    name = fields.Char(string='Kind of Fault', required=True)

    _order = 'name'

    _sql_constraints = [
        ('name_uk', 'unique(name)', 'Kind of fault must be unique'),
    ]

    @api.one
    def copy(self, default=None):
        default = dict(default or {})
        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)
        default['name'] = new_name
        return super(SieFaultKind, self).copy(default)
