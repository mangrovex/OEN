# -*- coding: utf-8 -*-

from odoo import _, models, fields, api


class SieGrade(models.Model):
    _name = 'sie.grade'
    _description = 'Grade'

    acronym = fields.Char(
        string='Acronimo',
        size=10,
        required=True,
        search='_search_acronym')
    name = fields.Char(
        string='Nombre',
        size=96,
        required=True,
        search='_search_name'
    )
    is_official = fields.Boolean(
        string='Es oficial?',
        help='Indica si el marino es oficial',
        default=False
    )
    order_ = fields.Integer(
        string=_('Order'),
        default=0
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

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {})
        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
            new_acronym = u"Copy of {}".format(self.acronym)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)
            new_acronym = u"Copy of {} ({})".format(self.acronym, copied_count)
        default['name'] = new_name
        default['acronym'] = new_acronym
        return super(SieGrade, self).copy(default)

    @api.depends('display_name')
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, '%s' % record.acronym))
        return result
