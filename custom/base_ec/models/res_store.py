# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from odoo import models, fields, SUPERUSER_ID, api
from odoo.osv import osv


class ResStore(models.Model):
    _name = "res.store"
    _description = 'Agencias'
    _order = 'parent_id desc, name'

    name = fields.Char(
        'Name',
        required=True,
    )
    code = fields.Char('Código', required=True)
    parent_id = fields.Many2one(
        'res.store',
        'Parent Store',
    )
    child_ids = fields.One2many(
        'res.store',
        'parent_id',
        'Child Stores'
    )
    company_id = fields.Many2one(
        'res.company', 'Company',
        # required=True,
        help='If specified, this store will be only available on selected '
        'company',
    )
    user_ids = fields.Many2many(
        'res.users',
        'res_store_users_rel',
        'cid', 'user_id',
        'Users'
    )

    city = fields.Many2one('res.state.city', string=u'Ciudad')
    address = fields.Text(u'Dirección')
    phone_one = fields.Char(u'Teléfono 1')
    phone_two = fields.Char(u'Teléfono 2')
    email = fields.Char(u'Correo electrónico')

    _sql_constraints = [
        ('name_uniq', 'unique (name, company_id)',
            'The store name must be unique per company!'),
        ('code_company_uniq', 'unique (code,company_id)',
         'The code of the operating unit must '
         'be unique per company!'),
    ]


    _constraints = [
        (osv.osv._check_recursion,
         'Error! You can not create recursive stores.', ['parent_id'])
    ]

    # # Copy from res_company
    # def name_search(
    #         self, name='', args=None, operator='ilike',
    #         context=None, limit=100):
    #     context = dict(context or {})
    #     if context.pop('user_preference', None):
    #         # We browse as superuser. Otherwise, the user would be able to
    #         # select only the currently visible stores (according to rules,
    #         # which are probably to allow to see the child stores) even if
    #         # she belongs to some other stores.
    #         user = self.pool.get('res.users').browse(
    #             cr, SUPERUSER_ID, uid, context=context)
    #         store_ids = list(set(
    #             [user.store_id.id] + [cmp.id for cmp in user.store_ids]))
    #         uid = SUPERUSER_ID
    #         args = (args or []) + [('id', 'in', store_ids)]
    #     return super(res_store, self).name_search(name=name, args=args, operator=operator,
    #         context=context, limit=limit)

    @api.model
    @api.returns('self', lambda value: value.id)
    def _res_store_default_get(self):
        """ Returns the default operating unit.
        The 'object' and 'field' arguments are ignored but left here for
        backward compatibility and potential override.
        """
        return self.search([('code', '=', '001')],limit=1)

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        # Make a search with default criteria
        names1 = super(models.Model, self).name_search(
            name=name, args=args, operator=operator, limit=limit)
        # Make the other search
        names2 = []
        if name:
            domain = [('code', '=ilike', name + '%')]
            names2 = self.search(domain, limit=limit).name_get()
        # Merge both results
        return list(set(names1) | set(names2))[:limit]
