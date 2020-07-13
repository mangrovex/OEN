from odoo import models, fields, api


class SieFaultSanction(models.Model):
    _name = 'sie.fault.sanction'
    _description = 'Sanction'

    name = fields.Char(string='Sanction', required=True)
    classification_id = fields.Many2one(comodel_name='sie.fault.classification', string='Classification of Fault',
                                        ondelete='restrict',
                                        required=True)
    demerits = fields.Integer(string='Demerits', required=True)

    _defaults = {
        'demerits': lambda *args: 0,
    }

    _sql_constraints = [
        ('name_uk', 'unique(name)', 'Sanction must be unique'),
        ('demerits_ck', 'check(demerits > 0)', 'Demerits must be greater than 0'),
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
        return super(SieFaultSanction, self).copy(default)
