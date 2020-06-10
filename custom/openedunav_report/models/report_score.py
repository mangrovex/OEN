import time
from odoo import api, models


class ReportScore(models.AbstractModel):
    _name = 'report.openedunav_report.report_score_act'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        docs = self.env['sie.score'].browse(self.ids)
        promotion = docs.course_id.promotion_course.name
        course_name = docs.course_id.name.split('-')[0]
        report = report_obj._get_report_from_name('openedunav_report.report_score_act')
        docargs = {
            'doc_ids': self.ids,
            'doc_model': report.model,
            'docs': docs,
            'promotion': promotion,
            'course_name': course_name,
        }
        return report_obj.render('openedunav_report.report_score_act', docargs)
