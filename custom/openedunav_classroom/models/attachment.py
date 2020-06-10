from odoo import models, fields, api


class SieAttachment(models.Model):
    _name = 'sie.attachment'
    _description = 'Sie attachment'

    name = fields.Char('Name', required=True)
    file = fields.Binary('file', required=True)

    _order = 'name'

    _sql_constraints = [
        ('name_uk', 'unique(name)', 'File must be unique'),
    ]

    # @api.one
    # @api.depends('file')
    # def _compute_name(self):
    #     if file:
    #         self.name = str(self.file)
    #     else:
    #         self.name = "archivo.pfd"
