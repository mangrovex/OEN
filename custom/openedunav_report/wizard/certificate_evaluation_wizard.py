# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CertificateEvaluationWizard(models.TransientModel):
    _name = 'report.certificate.evaluation.wizard'
    _description = 'Report certificate'

    course_id = fields.Many2one(
        'sie.course',
        string='Curso',
        required=True
    )
    faculty_id = fields.Many2one(
        'sie.faculty',
        string='Docente'
    )

    @api.onchange('course_id')
    def onchange_course_id(self):
        faculty_ids = []
        for subject_id in self.course_id.subject_ids:
            for content_id in subject_id.subject_content_ids:
                faculty_ids.append(content_id.faculty_id.id)
        return {
            'domain': {
                'faculty_id': [('id', 'in', faculty_ids)]
            }
        }

    def get_docs(self):
        context = {}
        docs =[]
        for subject_id in self.course_id.subject_ids:
            for content_id in subject_id.subject_content_ids:
                if content_id.faculty_id.id == self.faculty_id.id:
                    docs.append(content_id.id)
        context_str = '?context=' + str(context).replace("\'", "\"")
        docs_ids = [str(doc) for doc in docs]
        return ",".join(docs_ids), context_str

    def print_report(self):
        for record in self:
            doc_string, context_str = record.get_docs()
            return {
                "type": "ir.actions.act_url",
                "url": '/report/py3o/certificado_evaluacion_report/' + doc_string + context_str,
                "target": "new",
            }

