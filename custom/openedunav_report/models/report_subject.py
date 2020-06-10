import time
from odoo import api, models


class ReportScore(models.AbstractModel):
    _name = 'report.openedunav_report.report_subject_act'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        course_id = self.env['sie.course'].browse(data['course_id'])
        course_name = course_id.name.split('-')[0]
        promotion = course_id.name.split('-')[1]
        year = course_id.year
        docs = self.env['sie.subject'].search([('course_id', '=', course_id.id)])
        ciencia_militar = docs.filtered(
            lambda r: r.shaft_id.id == self.env.ref('openedunav_core.sie_training_shaft_01').id)
        cultura_militar = docs.filtered(
            lambda r: r.shaft_id.id == self.env.ref('openedunav_core.sie_training_shaft_02').id)
        cultura_humanistica = docs.filtered(
            lambda r: r.shaft_id.id == self.env.ref('openedunav_core.sie_training_shaft_03').id)
        ciencia_tecnologia = docs.filtered(
            lambda r: r.shaft_id.id == self.env.ref('openedunav_core.sie_training_shaft_04').id)

        report = report_obj._get_report_from_name('openedunav_report.report_subject_act')
        docargs = {
            'doc_ids': self.ids,
            'doc_model': report.model,
            'docs': docs,
            'course_name': course_name,
            'promotion': promotion,
            'course': course_id,
            'year': year,
            'ciencia_militar': ciencia_militar,
            'cultura_militar': cultura_militar,
            'cultura_humanistica': cultura_humanistica,
            'ciencia_tecnologia': ciencia_tecnologia,
        }
        return report_obj.render('openedunav_report.report_subject_act', docargs)
