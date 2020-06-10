from odoo import models, fields, api


class SieFaultLiteral(models.Model):
    _name = 'sie.fault.literal'
    _description = 'Literal'

    literal = fields.Char(string='Literal', size=4)
    name = fields.Text(string='Description', required=True)
    article_id = fields.Many2one(comodel_name='sie.fault.article', string='Article', ondelete='cascade', required=True)
    display_name = fields.Char(string='Name', compute='_compute_display_name')

    _order = 'article_id, literal'

    _sql_constraints = [
        ('literal_uk', 'unique(literal, article_id)', 'Literal must be unique'),
    ]

    @api.one
    @api.depends('name', 'literal')
    def _compute_display_name(self):
        names = [self.literal]
        self.display_name = ''.join(filter(None, names))

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=25):
        args = args or []
        if name:
            if len(name) == 1:
                args += [('literal', '=', name)]
            else:
                args += ['|', ('literal', operator, name), ('name', operator, name)]
        recs = self.search(args, limit=limit)
        return recs.name_get()
