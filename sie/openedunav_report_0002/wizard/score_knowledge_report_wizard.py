# -*- coding: utf-8 -*-
from odoo import models, fields, api
from operator import attrgetter
import logging
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ScoreKnowledgeReportWizard(models.TransientModel):
    _name = 'score.knowledge.report.wizard'
    _description = 'Score Knowledge'

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

    report_date = fields.Date(string="Start Date", required=True, default=fields.Date.today)

    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'course_id': self.course_id.id,
                'module_id': self.module_id.id,
                'knowledge_id': self.knowledge_id.id,
                'report_date': self.report_date,
            },
        }

        return self.env.ref('openedunav_report.score_knowledge_report').report_action(self, data=data)


class ReportScoreKnowledge(models.AbstractModel):
    _name = 'report.openedunav_report.score_knowledge_report_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        course_id = data['form']['course_id']
        module_id = data['form']['module_id']
        knowledge_id = data['form']['knowledge_id']
        report_date = data['form']['report_date']

        docs = []
        students = []
        contents = []
        module = self.env['sie.module'].search(
            [('id', '=', module_id)])
        course = self.env['sie.course'].search(
            [('id', '=', course_id)])
        knowledge = self.env['sie.knowledge'].search(
            [('module_id', '=', module_id),
             ('id', '=', knowledge_id)])

        for content_id in knowledge.content_ids:
            score_content = self.env['sie.score.content'].search(
                [('course_id', '=', course_id), ('module_id', '=', module_id),
                 ('knowledge_id', '=', knowledge_id),
                 ('content_id', '=', content_id.id),('state', '=', 'published')])
            for student_line in score_content.score_content_student_line:
                score_line = (student_line.score_1 + student_line.score_2) / 2
                contents.append({
                    'ruc': student_line.student_id.ced_ruc,
                    'score': score_line,
                    'content_name': score_content.content_name,
                })
        enrollment = self.env['sie.enrollment'].search([('course_id', '=', course_id)])
        student_ids = enrollment.student_ids.sorted(key=attrgetter('last_name', 'mother_name'))
        seq = 0
        for student in student_ids:
            seq += 1
            scores_ruc = []
            for content in contents:
                if content['ruc'] == student.ced_ruc:
                    scores_ruc.append({
                        'score': content['score'],
                        'content_name': content['content_name'],
                    })
            score = 0.0
            for score_ruc in scores_ruc:
                score += score_ruc['score']
            students.append({
                'ruc': student.ced_ruc,
                'grade': student.grade_id.name,
                'scores': scores_ruc,
                'score': score/2,
                'full_name': student.full_name,
                'seq': seq,
                'note': "  ",
            })

        docs.append({
            'course_name': course.name,
            'division': course.enrollment,
            'module_name': module.name,
            'knowledge_name': knowledge.name,
            'teacher': course.assigned_officer_id.full_name,
            'number_module': module.number_module,
            'report_date': report_date,

        })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'students': students,
            'docs': docs,
        }
