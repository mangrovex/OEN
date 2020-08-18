# -*- coding: utf-8 -*-

from odoo import _, models, fields


class SieSpecialty(models.Model):
    _name = 'sie.specialty'
    _description = 'SieSpecialty'

    acronym = fields.Char(
        _('Acronimo'),
        size=10,
        required=True,
        search='_search_acronym'
    )
    name = fields.Char(
        _('Nombre'),
        size=96,
        required=True,
        search='_search_name'
    )

    _sql_constraints = [
        ('acronym_uk', 'unique(acronym)', u'Acronimo debe ser único'),
        ('name_uk', 'unique(name)', u'Nombre debe ser único'),
    ]

    def _search_name(self, operator, value):
        if operator == 'like':
            operator = 'ilike'
        if self.name:
            return [('name', operator, value)]

    def _search_acronym(self, operator, value):
        if operator == 'like':
            operator = 'ilike'
        if self.acronym:
            if len(self.acronym) == 4:
                return [('acronym', operator, value)]

    def copy(self, default=None):
        for record in self:
            default = dict(default or {})
            copied_count = record.search_count(
                [('name', '=like', u"Copy of {}%".format(record.name))])
            if not copied_count:
                new_name = u"Copy of {}".format(record.name)
                new_acronym = u"Copy of {}".format(record.acronym)
            else:
                new_name = u"Copy of {} ({})".format(record.name, copied_count)
                new_acronym = u"Copy of {} ({})".format(record.acronym, copied_count)
            default['name'] = new_name
            default['acronym'] = new_acronym
            return super(SieSpecialty, record).copy(default)
