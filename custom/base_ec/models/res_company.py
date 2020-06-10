# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompany(models.Model):
    _name = "res.company"
    _inherit = "res.company"

    ruc_contador = fields.Char('Ruc del Contador', size=13)
    cedula_rl = fields.Char(u'Cédula Representante Legal', size=10)
    establishments = fields.Integer("Establecimientos")
    city_id = fields.Many2one('res.state.city', 'Ciudad',
                              domain="[('state_id','=',state_id)]")

    @api.onchange('city_id')
    def _onchange_city_id(self):
        for record in self:
            if record.city_id:
                record.city = self.city_id.name.capitalize()
            else:
                record.city = None

    def onchange_state(self, state_id):
        if state_id:
            return {'value': {'city_id': None, 'city': None}}
        return super(ResCompany, self).onchange_state(state_id)

    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.country_id:
            self.state_id = None
            self.city_id = None
            self.parish_id = None