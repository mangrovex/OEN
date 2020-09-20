# -*- coding: utf-8 -*-
from odoo import models, fields, api
from operator import attrgetter
import logging
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ScoreContentReportWizard(models.TransientModel):
    _name = 'score.content.report.wizard'
    _description = 'Score Content'

    course_id = fields.Many2one(
        'sie.course',
        string='Course',
        domain="[('state', '=', 'running')]",
        ondelete='restrict',
        required=True
    )
    # , ('module_ids.faculty_id.user_id', '=', uid)
    module_id = fields.Many2one(
        'sie.module',
        string='Módulo',
        ondelete='restrict',
        domain="[('course_ids', '=' , course_id), ('state', '=' , 'r')]",
        required=False
    )
    knowledge_id = fields.Many2one(
        'sie.knowledge',
        string=u'Àrea de conocimiento',
        ondelete='restrict',
        domain="[('module_id', '=',module_id) ]",
        required=True
    )
    content_id = fields.Many2one(
        'sie.content',
        string=u'Contenido imprescindible',
        ondelete='restrict',
        domain="[('knowledge_id', '=',knowledge_id) ]",
        required=True
    )
    report_date = fields.Date(string="Start Date", required=True, default=fields.Date.today)

    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'course_id': self.course_id.id,
                'module_id': self.module_id.id,
                'knowledge_id': self.knowledge_id.id,
                'content_id': self.content_id.id,
                'report_date': self.report_date,
            },
        }

        return self.env.ref('openedunav_report.score_content_report').report_action(self, data=data)


class ReportScoreContent(models.AbstractModel):
    _name = 'report.openedunav_report.score_content_report_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        course_id = data['form']['course_id']
        module_id = data['form']['module_id']
        knowledge_id = data['form']['knowledge_id']
        content_id = data['form']['content_id']
        report_date = data['form']['report_date']

        docs = []
        students = []
        score_content = self.env['sie.score.content'].search(
            [('course_id', '=', course_id), ('module_id', '=', module_id),
             ('knowledge_id', '=', knowledge_id),
             ('content_id', '=', content_id)])
        for student_line in score_content.score_content_student_line:
            score = (student_line.score_1 + student_line.score_2) / 2
            students.append({
                'ruc': student_line.student_id.ced_ruc,
                'grade': student_line.student_id.grade_id.name,
                'score_1': student_line.score_1,
                'score_2': student_line.score_2,
                'score': score,
                'full_name': student_line.full_name,
                'seq': student_line.seq,
                'note': "  ",
            })

        docs.append({
            'course_name': score_content.course_id.name,
            'division': score_content.course_id.enrollment,
            'module_name': score_content.module_id.name,
            'knowledge_name': score_content.knowledge_id.name,
            'content_name': score_content.content_name,
            'teacher': score_content.teacher_id.full_name,
            'number_module': score_content.module_id.number_module,
            'report_date': report_date,

        })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'students': students,
            'docs': docs,
        }
