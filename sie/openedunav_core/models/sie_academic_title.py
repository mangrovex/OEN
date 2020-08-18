# -*- coding: utf-8 -*-


from odoo import models, fields


class SieAcademicTitle(models.Model):
    _name = 'sie.academic.title'
    _description = 'Academic Title'

    name = fields.Char(
        'Nombre',
        size=96,
        required=True
    )
    abbreviation = fields.Char(
        'Abreviatura'
    )

    _sql_constraints = [
        ('name_unique', 'unique (name)', u'Nombre debe ser único')
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
            return super(SieAcademicTitle, record).copy(default)
