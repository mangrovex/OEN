#!/usr/bin/env python
#  -*- coding: UTF-8 -*-

from odoo import http
from . import podunk_report as report
from . import util as util
from . import report_base
from . import report_integrator


class ScoreReport(report_base.ReportBase):
    def __init__(self, local_tz, local_dt, subject_id, course_id, student_id, order):
        report_base.ReportBase.__init__(self, local_tz, local_dt, subject_id, course_id, None, None, None, None,
                                            None,
                                            None,
                                            student_id, order)

    def get_summary_integrator(self, course):
        integrator_report_report = report_integrator.IntegratorReport(self.local_tz, self.local_dt, self.course_id,
                                                                      None, None, None, None, None, "nombre", None)

        if integrator_report_report:
            scores_array = integrator_report_report.get_summary_integrator_array_2column(course)
        else:
            scores_array = []
        return scores_array

    def get_summary_achievement_final(self, course, matrix_id):
        child = self.get_parameter_childs_by_course(matrix_id).sorted(key=lambda r: r.param_name.code)

        scores_array_child = [0 for u in range(len(child))]
        x = 0
        for y in range(len(child)):
            if course.new_table:
                if child[y].param_name.code == '001':
                    scores_array_child[x] = self.get_summary_scores_array_1column(course)
                    x += 1
                if child[y].param_name.code == '013':
                    scores_array_child[x] = report_integrator.IntegratorReport(self.local_tz, self.local_dt,
                                                                               self.course_id, self.parameter_id,
                                                                               self.war_games_report, self.war_games_id,
                                                                               self.judge_id, self.student_id,
                                                                               None, self.direction_work_id). \
                        get_summary_integrator_array_1column(course)
                    x += 1
            else:
                if child[y].param_name.code == '001':
                    scores_array_child[x] = self.get_summary_scores_array_1column(course)
                    x += 1
        scores_array_report = self.get_summary_scores_final(scores_array_child, child)
        return scores_array_report

    def get_detail_academic_achievement(self):
        course = http.request.env['sie.course'].search([('id', '=', int(self.course_id))])
        course_name = course.course_name.name
        course_hours = course.exec_hours
        matrix_id = str(course.matrix_id.id)
        promotion_name = '%s %s %s ' % (course.promotion_course.name, u'AÑO:', course.year)
        date_time = self.local_tz.normalize(self.local_dt).strftime("%d-%b-%Y_%H-%M-%S")
        subject_name, hours, running_hours, coefficient, teacher_name = self.get_subject_data(course, self.subject_id)
        coefficient_title = util.round_sie(coefficient, u'7')
        filename = '%s_%s_%s%s' % (self.get_initials_course(course_name), subject_name.replace(' ', '_'),
                                   date_time, '.pdf')
        full_path = self.directory + filename

        full_title = 'Materia: %s' % subject_name
        detail_title = 'Horas Programadas: %s   Horas Ejecutadas: %s   Coeficiente: %s   Horas del Curso: %s' % \
                       (hours, running_hours, coefficient_title, course_hours)
        title_report = 'Informe de Notas Detalladas de Materias'

        scores_array = self.get_detail_achievement(matrix_id, course, self.subject_id, float(coefficient_title))
        if scores_array:
            data = util.get_elements(scores_array)
            media = util.format_sie(util.round_sie(util.mean(data), self.get_sie_digits()), self.get_sie_digits())
            deviation = util.format_sie(util.round_sie(util.pstdev(data), self.get_sie_digits()),
                                        self.get_sie_digits())
        else:
            scores_array = []
            media = ''
            deviation = ''

        teacher_title = 'Profesor: %s                Promedio: %s     Desv.: %s' % (teacher_name,
                                                                                    media.replace('.', ','),
                                                                                    deviation.replace('.', ','))
        report.report_pdf(full_path, self.get_scores_array_without_id(scores_array, self.student_id), course_name,
                          promotion_name,
                          title_report, full_title, teacher_title,
                          detail_title)

        return filename, full_path

    def get_summary_academic_achievement(self):
        course = self.get_course(self.course_id)
        course_name = course.course_name.name
        promotion_name = '%s %s %s ' % (course.promotion_course.name, u'AÑO:', course.year)
        date_time = self.local_tz.normalize(self.local_dt).strftime("%d-%b-%Y_%H-%M-%S")
        filename = '%s_APRENDIZAJE_SUMARIZADAS_%s%s' % (self.get_initials_course(course_name), date_time, '.pdf')
        full_path = self.directory + filename

        title_report = 'Informe de Notas Sumarizadas de Aprendizaje'
        scores_array = self.get_summary_achievement(course)
        if scores_array:
            if self.order == "promedio":
                if course.new_table:
                    scores_array = sorted(scores_array, key=lambda nota: float(nota[4]) if nota[4] != "APREN" else 30,
                                          reverse=True)
                else:
                    scores_array = sorted(scores_array, key=lambda nota: float(nota[8]) if nota[8] != "APREN" else 30,
                                          reverse=True)
                scores_array = self.re_number(scores_array)
            data = util.get_elements(scores_array)
            media = util.mean(data)
            deviation = util.pstdev(data)
            if media != "---":
                media = util.format_sie(util.round_sie(media, self.get_sie_digits()), self.get_sie_digits())
            if deviation != "---":
                deviation = util.format_sie(util.round_sie(deviation, self.get_sie_digits()),
                                            self.get_sie_digits())
        else:
            scores_array = []
            media = ''
            deviation = ''
        deviation_title = 'Promedio: %s     Desv.: %s' % (media.replace('.', ','), deviation.replace('.', ','))
        report.report_pdf(full_path, self.get_scores_array_without_id(scores_array, self.student_id), course_name,
                          promotion_name,
                          title_report, None, None, None, False, None, None, deviation_title)

        return filename, full_path

    def get_summary_academic_final(self):
        course = self.get_course(self.course_id)
        course_state = course.state
        matrix_id = str(course.matrix_id.id)
        course_name = course.course_name.name
        promotion_name = '%s %s %s ' % (course.promotion_course.name, u'AÑO:', course.year)
        date_time = self.local_tz.normalize(self.local_dt).strftime("%d-%b-%Y_%H-%M-%S")
        filename = '%s_NOTAS_FINALES_%s%s' % (self.get_initials_course(course_name), date_time, '.pdf')
        full_path = self.directory + filename
        title_report = 'Informe de Notas Finales'
        scores_array = self.get_summary_achievement_final(course, matrix_id)
        if scores_array:
            scores_array = self.remove_foreign_print(scores_array, self.course_id)
            if self.order == "nombre":
                index = 2
                scores_array = sorted(scores_array, key=lambda nota: nota[index] if nota[index] != "Nombre"
                else 'A')
            data = util.get_elements(scores_array)
            media = util.format_sie(util.round_sie(util.mean(data), self.get_sie_digits()), self.get_sie_digits())
            deviation = util.format_sie(util.round_sie(util.pstdev(data), self.get_sie_digits()),
                                        self.get_sie_digits())
        else:
            scores_array = []
            media = ''
            deviation = ''
        deviation_title = 'Promedio: %s     Desv.: %s' % (media.replace('.', ','), deviation.replace('.', ','))
        teacher_title = 'Fecha Inicio: %s            Fecha Finalizacion: %s' % (course.start_date, course.end_date)
        boss_name = ' '
        boss_title = ' '
        directors = self.get_directors(self.course_id)
        if directors:
            boss_name = '%s %s %s' % (directors.statistician_id.name.title(),
                                      directors.statistician_id.last_name_1.upper(),
                                      directors.statistician_id.last_name_2.title())
            grade = directors.statistician_id.grade_id.name
            specialty = directors.statistician_id.specialty_id.acronym
            if grade and specialty:
                boss_title = '%s - %s' % (grade, specialty)
            else:
                boss_title = ' '
        report.report_pdf(full_path, self.get_scores_array_without_index(self.get_scores_array_without_id(
            scores_array, self.student_id), course_state, self.student_id), course_name, promotion_name, title_report,
                          None, teacher_title, None, True, boss_name, boss_title, deviation_title)

        return filename, full_path

    def get_summary_academic_final_guest(self):
        course = self.get_course(self.course_id)
        matrix_id = str(course.matrix_id.id)
        course_name = course.course_name.name
        promotion_name = '%s %s %s ' % (course.promotion_course.name, u'AÑO:', course.year)
        date_time = self.local_tz.normalize(self.local_dt).strftime("%d-%b-%Y_%H-%M-%S")
        filename = '%s_NOTAS_FINALES_%s%s' % (self.get_initials_course(course_name), date_time, '.pdf')
        full_path = self.directory + filename
        title_report = 'Informe de Notas Finales'
        scores_array = self.get_summary_achievement_final(course, matrix_id)
        if scores_array:
            scores_array = self.only_foreign_print(scores_array, self.course_id)
            if self.order == "promedio":
                scores_array = sorted(scores_array, key=lambda nota: float(nota[7]) if nota[7] != "Promedio Final"
                else 30, reverse=True)
            data = util.get_elements(scores_array)
            media = util.format_sie(util.round_sie(util.mean(data), self.get_sie_digits()), self.get_sie_digits())
            deviation = util.format_sie(util.round_sie(util.pstdev(data), self.get_sie_digits()),
                                        self.get_sie_digits())
        else:
            scores_array = []
            media = ''
            deviation = ''
        deviation_title = 'Promedio: %s     Desv.: %s' % (media.replace('.', ','), deviation.replace('.', ','))
        teacher_title = 'Fecha Inicio: %s            Fecha Finalizacion: %s' % (course.start_date, course.end_date)
        boss_name = ' '
        boss_title = ' '
        directors = self.get_directors(self.course_id)
        if directors:
            boss_name = '%s %s %s' % (directors.statistician_id.name.title(),
                                      directors.statistician_id.last_name_1.upper(),
                                      directors.statistician_id.last_name_2.title())
            boss_title = '%s - %s' % (directors.statistician_id.grade_id.name,
                                      directors.statistician_id.specialty_id.acronym)
        report.report_pdf(full_path, self.get_scores_array_without_index(self.get_scores_array_without_id(scores_array))
                          , course_name, promotion_name,
                          title_report, None, teacher_title, None, True, boss_name, boss_title, deviation_title)

        return filename, full_path
