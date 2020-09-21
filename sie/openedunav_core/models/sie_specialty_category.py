# -*- coding: utf-8 -*-

from odoo import _, models, fields, api
from odoo.osv import expression


class SieSpecialtyCategory(models.Model):
    _name = 'sie.specialty.category'
    _description = 'Sie Specialty Category'

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

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if operator == 'ilike' and not (name or '').strip():
            domain = []
        else:
            domain = ['|', ('name', operator, name), ('acronym', operator, name)]
        rec = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return models.lazy_name_get(self.browse(rec).with_user(name_get_uid))

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
            return super(SieSpecialtyCategory, record).copy(default)
