# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CertificateWizar(models.TransientModel):
    _name = 'report.certificate.wizard'
    _description = 'Report certificate'

    course_id = fields.Many2one('sie.course', string='Course', required=True)

    @api.multi
    def print_report(self):
        url = '/web/aguena/report_certificate?' \
              '&course_id=%s' \
              % (self.course_id.id)
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }
