#!/usr/bin/env python
#  -*- coding: UTF-8 -*-

import datetime
from io import StringIO

import pytz
from PyPDF2 import PdfFileWriter, PdfFileReader

from addons.web.controllers.main import serialize_exception
from odoo import http
from odoo.http import request
from . import report_integrator
from . import report_score
from . import report_certificate


class SchoolReportController(http.Controller):
    def print_report(self, full_path, filename):
        file_content = ''
        tmp = StringIO()
        output = PdfFileWriter()
        inputFile = open(full_path, 'rb')
        pdf_temp = PdfFileReader(inputFile)
        if pdf_temp:
            for page in range(pdf_temp.getNumPages()):
                output.addPage(pdf_temp.getPage(page))
            output.write(tmp)
            tmp.seek(0)
            data = tmp.read()
            tmp.close()
            file_content = data
        return file_content


    @http.route('/web/aguena/report_integrator', type='http', auth="user")
    @serialize_exception
    def report_integrator(self, course_id=None, report_type=None, parameter_id=None, war_games_report=None,
                          war_games_id=None, judge_id=None, direction_work_id=None, student_id=None, ordenar=None,
                          **kw):
        local_tz = pytz.timezone('America/Guayaquil')
        utc_dt = datetime.datetime.utcnow()
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
        flag = 0
        filename = ''
        full_path = ''
        i_report = report_integrator.IntegratorReport(local_tz, local_dt, course_id, parameter_id, war_games_report,
                                                      war_games_id, judge_id, student_id, ordenar, direction_work_id)
        if report_type == 'D':
            flag = 1
            filename, full_path = i_report.get_detail_integrator()
        elif report_type == 'S':
            flag = 1
            filename, full_path = i_report.get_summary_integrator()

        if flag:
            file_content = self.print_report(full_path, filename)
            if not file_content:
                return request.not_found()
            else:
                if not filename:
                    filename = '%s.pdf' % 'report'
                return request.make_response(file_content, headers=[('Content-Disposition',
                                                                     'attachment; filename=%s' % filename),
                                                                    ('Content-Type', 'application/pdf')])

    @http.route('/web/aguena/report_score', type='http', auth="user")
    @serialize_exception
    def report_academic_achievement(self, course_id=None, report_type=None, subject_id=None, student_id=None,
                                    ordenar=None,
                                    **kw):
        local_tz = pytz.timezone('America/Guayaquil')
        utc_dt = datetime.datetime.utcnow()
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
        flag = 0
        filename = ''
        full_path = ''
        s_report = report_score.ScoreReport(local_tz, local_dt, subject_id, course_id, student_id, ordenar)
        if report_type == 'D':
            flag = 1
            filename, full_path = s_report.get_detail_academic_achievement()
        elif report_type == 'S':
            flag = 1
            filename, full_path = s_report.get_summary_academic_achievement()
        elif report_type == 'F':
            flag = 1
            filename, full_path = s_report.get_summary_academic_final()
        elif report_type == 'FG':
            flag = 1
            filename, full_path = s_report.get_summary_academic_final_guest()

        if flag:
            file_content = self.print_report(full_path, filename)
            if not file_content:
                return request.not_found()
            else:
                if not filename:
                    filename = '%s.pdf' % 'report'
                return request.make_response(file_content, headers=[('Content-Disposition',
                                                                     'attachment; filename=%s' % filename),
                                                                    ('Content-Type', 'application/pdf')])

    @http.route('/web/aguena/report_certificate', type='http', auth="user")
    @serialize_exception
    def report_certificate(self, course_id=None, **kw):
        local_tz = pytz.timezone('America/Guayaquil')
        utc_dt = datetime.datetime.utcnow()
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)

        cert_report = report_certificate.CertificateReport(local_tz, local_dt, course_id)
        flag = 1
        filename, full_path = cert_report.get_certificate_report()
        if flag:
            file_content = self.print_report(full_path, filename)
            if not file_content:
                return request.not_found()
            else:
                if not filename:
                    filename = '%s.pdf' % 'report'
                return request.make_response(file_content, headers=[('Content-Disposition',
                                                                     'attachment; filename=%s Export' % filename),
                                                                    ('Content-Type', 'application/pdf')])
