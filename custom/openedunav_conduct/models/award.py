from odoo import models, fields, api


class SieAward(models.Model):
    _name = 'sie.award'
    _description = 'Award'

    name = fields.Char(('Name'), size=96, required=True)
    given = fields.Char(('Given'), size=96, required=True)

    _sql_constraints = [
        ('name_uk', 'unique(name)', 'Name must be unique')
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
        return super(SieAward, self).copy(default)
