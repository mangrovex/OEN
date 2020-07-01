from odoo import models, fields


class SieConcept(models.Model):
    _name = 'sie.concept'
    _description = 'Concept of Faculty Appreciation'
    _order = 'name'

    name = fields.Char(
        'Concept',
        size=96,
        required=True
    )
    description = fields.Text(
        'Description',
        required=True
    )

    _sql_constraints = [
        ('name_uk', 'unique(name)', 'Concept must be unique'),
    ]

    def copy(self, default=None):
        for record in self:
            default = dict(default or {})
            copied_count = record.search_count(
                [('name', '=like', u"Copy of {}%".format(record.name))])
            if not copied_count:
                new_name = u"Copy of {}".format(record.name)
            else:
                new_name = u"Copy of {} ({})".format(record.name, copied_count)
            default['name'] = new_name
            return super(SieConcept, record).copy(default)
