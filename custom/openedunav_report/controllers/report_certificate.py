#!/usr/bin/env python
#  -*- coding: UTF-8 -*-

from odoo import http
from . import podunk_certificate as certificate
from . import util as util
from . import report_base
from . import report_integrator
from . import report_score


class CertificateReport(report_base.ReportBase):
    def __init__(self, local_tz, local_dt, course_id):
        report_base.ReportBase.__init__(self, local_tz, local_dt, None, course_id, None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            None)

    def get_certificate_report(self):
        logo_path = self.directory + 'aguena.png'
        course = self.get_course(self.course_id)
        course_name = course.course_name.name
        promotion_name = course.promotion_course.name
        year = course.year
        date_time = self.local_tz.normalize(self.local_dt).strftime("%d-%b-%Y_%H-%M-%S")
        date_now = '%s %s' % (self.get_month_spanish_fullname(self.local_tz.normalize(self.local_dt).strftime("%m")),
                              self.local_tz.normalize(self.local_dt).strftime("%d de %Y"))
        filename = '%s_CERTIFICADO_%s%s' % (self.get_initials_course(course_name), date_time, '.pdf')
        full_path = self.directory + filename
        course = self.get_course(self.course_id)
        t_hours = '%s' % course.exec_hours
        credit = '%s' % course.total_credits

        boss_name = ' '
        boss_title = ' '
        director_name = ' '
        director_title = ' '
        directors = self.get_directors(self.course_id)
        if directors:
            boss_name = '%s %s %s' % (directors.statistician_id.name.title(),
                                      directors.statistician_id.last_name_1.upper(),
                                      directors.statistician_id.last_name_2.title())
            boss_title = '%s - %s' % (directors.statistician_id.grade_id.name,
                                      directors.statistician_id.specialty_id.acronym)
            director_name = '%s %s %s' % (directors.director_id.name.title(),
                                          directors.director_id.last_name_1.upper(),
                                          directors.director_id.last_name_2.title())
            director_title = '%s - %s' % (
            directors.director_id.grade_id.name, directors.director_id.specialty_id.acronym)

        seminaries = self.get_seminaries(self.course_id)
        x = 0
        array_seminaries = [0 for u in range(len(seminaries))]
        for seminary in seminaries:
            seminary_detail = u'     %s - %s horas' % (seminary.seminary_name, seminary.duration)
            array_seminaries[x] = seminary_detail
            x += 1

        enrollment = self.get_enrollment(self.course_id)
        # num_students = len(enrollment.student_ids)
        student_id = []
        student_name = []
        student_nuc = []

        s_report = report_score.ScoreReport(self.local_tz, self.local_dt, "", course.id, None, None)

        score_array_subjects, subjects = s_report.get_summary_scores_array_subject(course)
        matrix_id = str(course.matrix_id.id)
        child_course = self.get_parameter_childs_by_course(matrix_id).sorted(key=lambda r: r.param_name.code)

        score_array_summary_final = s_report.get_summary_achievement_final(course, matrix_id)

        for data in score_array_summary_final:
            for student in enrollment.student_ids:
                if str(student.id) == data[3]:
                    student_name.append(student.display_title_name)
                    student_nuc.append(student.identification_id)
                    student_id.append(student.id)

        score_array_summary = s_report.get_summary_achievement(course)

        foreign_students = len(self.get_enrollment(self.course_id).student_ids.filtered("guest"))
        if course.new_table:
            certificate.report_pdf(full_path, score_array_subjects, course_name, promotion_name,
                                   year, student_name, student_nuc, student_id, subjects,
                                   t_hours, credit, course.start_date, course.end_date, logo_path, date_now, boss_name,
                                   boss_title, director_name, director_title,
                                   score_array_summary,
                                   score_array_summary_final,
                                   array_seminaries, child_course,
                                   None, True)
        else:
            child_achievement = self.get_parameter_by_code("001", matrix_id).child_ids.sorted(
                key=lambda r: r.param_name.code)

            p_report = report_productivity.ProductivityReport(self.local_tz,
                                                              self.local_dt, course.id,
                                                              '',
                                                              '', None, None)
            a_report = report_professional_attitude.AttitudeReport(self.local_tz, self.local_dt, '',
                                                                   course.id, '', '', None, None)
            # score_array_summary_productivity = p_report.get_summary_productivity_array(course)
            # score_array_summary_attitude = a_report.get_summary_professional_attitudes_array(course)
            certificate.report_pdf(full_path, score_array_subjects, course_name, promotion_name,
                                   year, student_name, student_nuc, student_id, subjects,
                                   t_hours, credit, course.start_date, course.end_date, logo_path, date_now, boss_name,
                                   boss_title, director_name, director_title,
                                   score_array_summary,
                                   score_array_summary_final, array_seminaries, child_course,
                                   child_achievement, False)
        return filename, full_path
