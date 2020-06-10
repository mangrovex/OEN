from odoo import models, fields, api


class SieFaultClassification(models.Model):
    _name = 'sie.fault.classification'
    _description = 'Classification of Fault'

    name = fields.Char(string='Classification of Fault', required=True)
    description = fields.Text(string='Description')
    suggested_ids = fields.One2many(comodel_name='sie.fault.suggested.sanction', inverse_name='classification_id',
                                    string='Suggested Sanctions')

    _order = 'name'

    _sql_constraints = [
        ('name_uk', 'unique(name)', 'Classification of fault must be unique'),
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
        default['suggested_ids'] = []
        return super(SieFaultClassification, self).copy(default)
