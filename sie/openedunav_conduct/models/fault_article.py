from odoo import models, fields, api


class SieFaultArticle(models.Model):
    _name = 'sie.fault.article'
    _description = 'Article'

    name = fields.Char(string='Article', required=True)
    kind_id = fields.Many2one(comodel_name='sie.fault.kind', string='Kind of Fault', ondelete='restrict', required=True)
    classification_id = fields.Many2one(comodel_name='sie.fault.classification', string='Classification of Fault',
                                        ondelete='restrict',
                                        required=True)
    literal_ids = fields.One2many(comodel_name='sie.fault.literal', inverse_name='article_id', string='Literals')

    _sql_constraints = [
        ('name_uk', 'unique(name)', 'Article must be unique'),
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
        return super(SieFaultArticle, self).copy(default)
