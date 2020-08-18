# -*- coding: utf-8 -*-
from stdnum.ec import ruc, ci

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
from odoo.tools import config


def check_ced_ruc(ced):
    if ci.is_valid(ced):
        return True
    else:
        return False


def check_ruc_s_pri(ruc):
    try:
        # soporte para nacionalizados(codigo 30 y 50)
        if int(ruc[0] + ruc[1]) < 25 or int(ruc[0] + ruc[1]) in (30, 50):
            test1 = True
        else:
            test1 = False
        if int(ruc[2]) == 9:
            test2 = True
        else:
            test2 = False
        val0 = int(ruc[0]) * 4
        val1 = int(ruc[1]) * 3
        val2 = int(ruc[2]) * 2
        val3 = int(ruc[3]) * 7
        val4 = int(ruc[4]) * 6
        val5 = int(ruc[5]) * 5
        val6 = int(ruc[6]) * 4
        val7 = int(ruc[7]) * 3
        val8 = int(ruc[8]) * 2
        tot = val0 + val1 + val2 + val3 + val4 + val5 + val6 + val7 + val8
        divisor = int(tot / 11.0)
        veri = int(11 - (tot - (11 * divisor)))
        if veri == 11: veri = 0
        if veri == 0:
            if (int(ruc[9])) == 0:
                test3 = True
            else:
                test3 = False
        else:
            if (int(ruc[9])) == (veri):
                test3 = True
            else:
                test3 = False
        # la ultima parte debe ser el codigo del establecimiento, entre 001, 00N
        # pero x ahora solo validar que sea 001
        if ruc[10:] in ('001',):
            test4 = True
        else:
            test4 = False
        if test1 and test2 and test3 and test4:
            return True
        else:
            return False
    except:
        return False


def check_ruc_s_pub(ruc):
    try:
        # soporte para nacionalizados(codigo 30 y 50)
        if int(ruc[0] + ruc[1]) < 25 or int(ruc[0] + ruc[1]) in (30, 50):
            test1 = True
        else:
            test1 = False
        if int(ruc[2]) == 6:
            test2 = True
        else:
            test2 = False
        val0 = int(ruc[0]) * 3
        val1 = int(ruc[1]) * 2
        val2 = int(ruc[2]) * 7
        val3 = int(ruc[3]) * 6
        val4 = int(ruc[4]) * 5
        val5 = int(ruc[5]) * 4
        val6 = int(ruc[6]) * 3
        val7 = int(ruc[7]) * 2
        tot = val0 + val1 + val2 + val3 + val4 + val5 + val6 + val7
        divisor = int(tot / 11.0)
        veri = int(11 - (tot - (11 * divisor)))
        if veri == 11: veri = 0
        if veri == 0:
            if (int(ruc[8])) == 0:
                test3 = True
            else:
                test3 = False
        else:
            if (int(ruc[8])) == (veri):
                test3 = True
            else:
                test3 = False
        # la ultima parte debe ser el codigo del establecimiento, entre 001, 00N
        # pero x ahora solo validar que sea 001
        if ruc[10:] in ('001',):
            test4 = True
        else:
            test4 = False
        if test1 and test2 and test3 and test4:
            return True
        else:
            # FIXME: por alguna razon existio un caso de un ruc que el sistema del sri tiene asignado a una persona
            #  natural y tiene la forma de institucion publica
            if test4:
                return check_ced_ruc(ruc[:10])
            return False
    except:
        return False


def check_ruc_p_nat(ruc):
    try:
        # soporte para nacionalizados(codigo 30 y 50)
        if int(ruc[0] + ruc[1]) < 25 or int(ruc[0] + ruc[1]) in (30, 50):
            test1 = True
        else:
            test1 = False
        if int(ruc[2]) < 6:
            test2 = True
        else:
            test2 = False
        valores = [int(ruc[x]) * (2 - x % 2) for x in range(9)]
        suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
        dsup = 10
        if suma > 10:
            dsup = (int(str(suma)[0]) + 1) * 10
        veri = dsup - suma
        if veri == 10:
            veri = 0
        if int(ruc[9]) == veri:
            test3 = True
        else:
            test3 = False
        # la ultima parte debe ser el codigo del establecimiento, entre 001, 00N
        # pero x ahora solo validar que sea 001
        if ruc[10:] in ('001',):
            test4 = True
        else:
            test4 = False
        if test1 and test2 and test3 and test4:
            return True
        else:
            if test4:
                return check_ced_ruc(ruc[:10])
            return False
    except:
        return False


def check_id_cons_final(ced):
    b = True
    try:
        for n in ced:
            if int(n) != 9:
                b = False
        return b
    except:
        return False


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):  # noqa
        args = args or []
        if name:
            ids = self.search([('vat', operator, name)] + args, limit=limit)  # noqa
            if not ids:
                ids = self.search([('name', operator, name)] + args, limit=limit)  # noqa
        else:
            ids = self.search(args, limit=limit)
        return ids.name_get()

    company_type = fields.Selection(default="person")
    type_ced_ruc = fields.Selection(
        [
            ('cedula', 'CEDULA'),
            ('ruc', 'RUC'),
            ('pasaporte', 'PASAPORTE'),
            ('placa', u'PLACA o RAMV/CPN'),
            ('final', 'CONSUMIDOR FINAL')
        ],
        'Type ID',
        track_visibility='onchange'
    )
    type_person = fields.Selection(
        [
            ('6', 'Persona Natural'),
            ('9', 'Persona Juridica')
        ],
        string='Person Type',
        required=True,
        default='6'
    )
    ced_ruc = fields.Char(
        'NUC/RUC',
        help=u'Identificación o Registro Unico de Contribuyentes',
        store=True,
        track_visibility='onchange'
    )
    vat = fields.Char(
        compute='_compute_vat',
        store=True
    )
    tz = fields.Selection(default="America/Guayaquil")
    city_id = fields.Many2one(
        'res.state.city',
        'City Id.',
        ondelete='restrict',
        domain="[('state_id','=',state_id)]"
    )
    parish_id = fields.Many2one(
        'res.city.parish',
        ondelete='restrict',
        string="Parish",
        domain="[('city_id', '=', city_id)]"
    )

    _sql_constraints = [
        ('partner_unique',
         'unique(country_id,ced_ruc,type_ced_ruc)',
         u'La indeficación debe ser única.'),
        ('partner_unique_id',
         'unique(ced_ruc,type_ced_ruc)',
         u'La indeficación debe ser única.'),
    ]

    @api.constrains("vat")
    def _check_vat_unique(self):
        for record in self:
            if record.parent_id or not record.vat:
                continue
            test_condition = config["test_enable"] and not self.env.context.get(
                "test_vat"
            )
            if test_condition:
                continue
            if record.same_vat_partner_id:
                raise ValidationError(
                    _("The VAT %s already exists in another partner.") % record.vat
                )

    @api.depends('ced_ruc', 'country_id')
    def _compute_vat(self):
        for record in self:
            if not record.ced_ruc:
                record.vat = None
            else:
                if not record.country_id:
                    record.vat = "EC" + record.ced_ruc
                else:
                    record.vat = record.country_id.code + record.ced_ruc

    @api.onchange('vat')
    def _onchange_vat(self):
        for record in self:
            if record.vat:
                record.vat = record.vat.upper()

    @api.onchange('type_ced_ruc')
    def _onchange_type_ced_ruc(self):
        for record in self:
            if not record.type_ced_ruc:
                record.vat = None

    @api.onchange('ced_ruc')
    def _onchange_ced_ruc(self):
        for record in self:
            if record.ced_ruc:
                if record.country_id:
                    record.vat = record.country_id.code + record.ced_ruc
                else:
                    record.vat = "EC" + record.ced_ruc
            else:
                record.vat = None

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
        return super(ResPartner, self).onchange_state(state_id)

    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.country_id:
            self.state_id = None
            self.city_id = None
            self.parish_id = None

    @api.constrains('type_ced_ruc', 'type_person', 'ced_ruc')
    def check_ced_ruc(self):
        for record in self:
            if record.type_ced_ruc:
                if record.ced_ruc:
                    if not ci.is_valid(record.ced_ruc):
                        if record.type_ced_ruc == 'cedula':
                            raise ValidationError('CI [%s] no es valido !' % record.ced_ruc)
                        elif record.type_ced_ruc == 'ruc':
                            raise ValidationError('RUC [%s] no es valido !' % record.ced_ruc)

    def create_user(self):
        self.env['res.users'].create_user(self)

    @api.model
    def _validate_ref(self, ref):
        type_ref = ""
        if self.env.context.get('skip_ruc_validation') or not ref:
            return type_ref
        try:
            if not self.env.context.get('foreign', False):
                # validar que sea solo numeros
                try:
                    int(ref)
                except ValueError:
                    raise Warning(_(u'La CEDULA/RUC %s solo debe tener números, por favor verifique') % (ref))
                if len(ref) == 13:
                    dato = ref
                    if int(dato[2]) == 9:
                        # verify if partner is a private company
                        if check_ruc_s_pri(ref):
                            type_ref = 'ruc'
                        elif check_id_cons_final(ref):
                            type_ref = 'consumidor'
                        else:
                            raise Warning(_(u'La CEDULA/RUC %s no es correcta, por favor verifique') % (ref))
                    elif int(dato[2]) == 6:
                        # verify if partner is a statal company
                        if check_ruc_s_pub(ref):
                            type_ref = 'ruc'
                        else:
                            raise Warning(_(u'La CEDULA/RUC %s es incorrecto, por favor verifique') % (ref))
                    elif int(dato[2]) < 6:
                        # verify if partner is a natural person
                        if check_ruc_p_nat(ref):
                            type_ref = 'ruc'
                        else:
                            raise Warning(_(u'La CEDULA/RUC %s es incorrecto, por favor verifique') % (ref))
                    else:
                        raise Warning(_(u'La CEDULA/RUC %s es incorrecto, por favor verifique') % (ref))
                elif len(ref) == 10:
                    # verify the dni or Cedula of partner
                    if check_ced_ruc(ref):
                        type_ref = 'cedula'
                    else:
                        raise Warning(_(u'La CEDULA/RUC %s es incorrecto, por favor verifique') % (ref))
                else:
                    raise Warning(_(u'La CEDULA/RUC %s es incorrecto, por favor verifique') % (ref))
            else:
                type_ref = 'passport'
        except:
            raise Warning(_(u'La CEDULA/RUC %s es incorrecto, por favor verifique') % (ref))
        return type_ref
