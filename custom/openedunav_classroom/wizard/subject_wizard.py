# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SubjectWizard(models.TransientModel):
    _name = 'report.subject.wizard'
    _description = 'Report Subject'

    course_id = fields.Many2one('sie.course', string='Course', required=True)

    def print_report(self):
        for record in self:
            data = {'course_id': record.course_id.id, 'download_name': record.course_id.name + '.pdf'}
            return record.env['report'].get_action(record, 'openedunav_report.report_subject_act', data=data)
