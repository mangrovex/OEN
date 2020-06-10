# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SubjectWizard(models.TransientModel):
    _name = 'report.subject.wizard'
    _description = 'Report Subject'

    course_id = fields.Many2one('sie.course', string='Course', required=True)

    @api.multi
    def print_report(self):
        data = {}
        data['course_id'] = self.course_id.id
        data['download_name'] = self.course_id.name + '.pdf'
        return self.env['report'].get_action(self, 'openedunav_report.report_subject_act', data=data)
