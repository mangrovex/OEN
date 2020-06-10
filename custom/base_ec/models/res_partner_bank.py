# -*- encoding: utf-8 -*-

from odoo import models, fields, api


class ResPartnerBank(models.Model):
    _name = 'res.partner.bank'
    _inherit = 'res.partner.bank' 
    
    type_account = fields.Selection([
        ('savings','Ahorros'),
        ('current','Corriente'),
        ('virtual','Virtual'),
        ], string='Tipo de Cuenta Bancaria', 
        readonly=False, required=False, default='savings') 
    
    #Se reemplaza esta funcion porque cuando se crea la cuenta bancaria en la compania se crea una cuenta
    #Contable y un diario contable, no se debe permitir este comportamiento
    # @api.multi
    # def post_write(self):
    #     return True
    #
    def name_get(self):
        res = []
        for rec in self:
            name = rec.acc_number
            if rec.bank_id:
                name = '%s - %s' % (rec.bank_id.name, rec.acc_number)
            res.append((rec.id, name))
        return res
