from odoo import models, fields, api


class ResCountry(models.Model):
    _name = "res.country"
    _inherit = "res.country"

    code_ec = fields.Char('Cod. EC', size=3)
