#!/usr/bin/env python
#  -*- coding: UTF-8 -*-
from manexreport.project import report

from odoo import http

import decimal
from . import util as util
from . import report_base


class IntegratorReport(report_base.ReportBase):
    def __init__(self, local_tz, local_dt, course_id, parameter_id, war_games_report, war_games_id, judge_id,
                 student_id, order, direction_work_id):
        report_base.ReportBase.__init__(self, local_tz, local_dt, None, course_id, parameter_id, None,
                                            direction_work_id,
                                            judge_id, student_id, order)

    def get_detail_integrator(self):
        full_path = self.directory + 'producto_integrador_detallado.pdf'
        course = http.request.env['sie.course'].search([('id', '=', int(self.course_id))])
        course_name = course.course_name.name
        matrix_id = str(course.matrix_id.id)
        promotion_name = '%s %s %s ' % (course.promotion_course.name, u'AÑO:', course.year)
        filename = ''
        date_time = self.local_tz.normalize(self.local_dt).strftime("%d-%b-%Y_%H-%M-%S")
        parameter = self.get_parameter_by_id(self.parameter_id)
        param_name = parameter.param_name
        param_name_code = param_name.code

        if self.student_id:
            student = self.get_student(self.student_id)
        else:
            student = None

        if param_name_code == '023':
            filename = '%s_CONF_%s%s' % (self.get_initials_course(course_name), date_time, '.pdf')
            full_path = self.directory + filename
            scores_array = self.get_detail_con_tdi(self.parameter_id, matrix_id, 'TII')
            full_title = 'T.I.I. CONFERENCIA'
            title_report = 'Informe de Notas Detalladas de Conferencias'
            if student:
                if not student.inactive:
                    report.report_pdf(full_path, self.get_scores_array_without_id(scores_array, self.student_id),
                                      course_name, promotion_name, title_report, full_title)
            else:
                report.report_pdf(full_path, self.get_scores_array_without_id(scores_array, None), course_name,
                                  promotion_name, title_report, full_title)
        elif param_name_code == '024':
            work_name, scores_array = self.get_detail_tdd(self.direction_work_id, self.parameter_id, matrix_id)
            filename = '%s_TDD_%s_%s%s' % (self.get_initials_course(course_name), date_time,
                                           work_name.replace(' ', '_'), '.pdf')
            full_path = self.directory + filename
            full_title = 'Trabajo: %s' % work_name
            title_report = 'Informe de Notas Detalladas de Trabajos de Dirección'
            if student:
                if not student.inactive:
                    report.report_pdf(full_path, self.get_scores_array_without_id(scores_array, self.student_id),
                                      course_name, promotion_name, title_report, full_title)
            else:
                report.report_pdf(full_path, self.get_scores_array_without_id(scores_array, None), course_name,
                                  promotion_name, title_report, full_title)
        else:
            filename = '%s_PI_%s_%s%s' % (self.get_initials_course(course_name), param_name.name, date_time, '.pdf')
            full_path = self.directory + filename
            scores_array = self.get_detail_thesis(parameter.id, matrix_id, self.course_id, param_name.short_name)
            full_title = ''
            title_report = 'Informe de Notas Detalladas de Tesis, Ensayos o Monografías'
            report.report_pdf(full_path, self.get_scores_array_without_id(scores_array, self.student_id), course_name,
                              promotion_name,
                              title_report, full_title)
        return filename, full_path

    def get_summary_integrator(self):
        date_time = self.local_tz.normalize(self.local_dt).strftime("%d-%b-%Y_%H-%M-%S")

        course = self.get_course(self.course_id)
        course_name = course.course_name.name
        filename = '%s_producto_integrador_sumarizadas_%s%s' % (self.get_initials_course(course_name), date_time,
                                                                '.pdf')
        full_path = self.directory + filename
        promotion_name = '%s %s %s ' % (course.promotion_course.name, u'AÑO:', course.year)
        scores_array = self.get_summary_integrator_array(course)
        if scores_array:
            if self.order == "promedio":
                if course.new_table:
                    index = len(scores_array[0]) - 2
                    scores_array = sorted(scores_array,
                                          key=lambda nota: float(nota[index]) if nota[index] != "P.I." else 30,
                                          reverse=True)
                else:
                    index = len(scores_array[0]) - 2
                    scores_array = sorted(scores_array,
                                          key=lambda nota: float(nota[index]) if nota[index] != "P.I." else 30,
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
            media = ''
            deviation = ''

        title_report = 'Informe de Notas Sumarizadas de Producto Integrador'
        deviation_title = 'Promedio: %s     Desv.: %s' % (media.replace('.', ','), deviation.replace('.', ','))
        report.report_pdf(full_path, self.get_scores_array_without_id(scores_array, self.student_id), course_name,
                          promotion_name,
                          title_report, None, None, None, None, None, None, deviation_title)
        return filename, full_path

    def get_summary_integrator_array(self, course):
        matrix_id = course.matrix_id.id
        parameter = self.get_parameter_by_param_name('013', matrix_id)
        coefficient_pro = parameter.coefficient

        scores_array_users = []
        columns = 4
        columns_thesis = columns_games = columns_mono = columns_essay = columns_group_essay = columns_productivity = 0
        flag_thesis = flag_mono = flag_essay  = False
        flag_thesis_exists = flag_mono_exists = flag_essay_exists = False
        flag_average = True

        # calculo de notas por cada parametro
        # TESIS
        parameter_thesis = self.get_parameter_by_param_name('021', matrix_id, '013')
        if parameter_thesis.id == False:
            scores_array_thesis = []
        else:
            scores_array_thesis = self.get_detail_thesis(parameter_thesis.id, matrix_id, self.course_id,
                                                         parameter_thesis.param_name.short_name)
            flag_thesis_exists = True
            columns_thesis += 2
        if scores_array_thesis:
            flag_thesis = True
            num_students = len(scores_array_thesis)
            columns_pro = 2
            scores_array_users = [[0 for j in range(4)] for i in range(num_students)]
            scores_array_thesis_prom = [[0 for j in range(columns_pro)] for i in range(num_students)]
            w = 0
            for x in range(num_students):
                z = zz = 0
                longitude = len(scores_array_thesis[x])
                for y in range(longitude):
                    if y < 4:
                        scores_array_users[w][zz] = scores_array_thesis[x][y]
                        zz += 1
                    elif y == longitude - 2:
                        scores_array_thesis_prom[w][z] = scores_array_thesis[x][y]
                        z += 1
                    elif y == longitude - 1:
                        scores_array_thesis_prom[w][z] = scores_array_thesis[x][y]
                        z += 1
                w += 1
        # 'MONOGRAFIA'
        parameter_mono = self.get_parameter_by_param_name('031', matrix_id, '013')
        if parameter_mono.id == False:
            scores_array_mono = []
        else:
            scores_array_mono = self.get_detail_thesis(parameter_mono.id, matrix_id, self.course_id,
                                                       parameter_mono.param_name.short_name)
            flag_mono_exists = True
            columns_mono += 2
        if scores_array_mono:
            flag_mono = True
            num_students = len(scores_array_mono)
            columns_pro = 2
            scores_array_users = [[0 for j in range(4)] for i in range(num_students)]
            scores_array_mono_prom = [[0 for j in range(columns_pro)] for i in range(num_students)]
            w = 0
            for x in range(num_students):
                z = zz = 0
                longitude = len(scores_array_mono[x])
                for y in range(longitude):
                    if y < 4:
                        scores_array_users[w][zz] = scores_array_mono[x][y]
                        zz += 1
                    elif y == longitude - 2:
                        scores_array_mono_prom[w][z] = scores_array_mono[x][y]
                        z += 1
                    elif y == longitude - 1:
                        scores_array_mono_prom[w][z] = scores_array_mono[x][y]
                        z += 1
                w += 1

        course = self.get_course(self.course_id)
        flag_con = 'E'
        flag_dir = 'E'
        flag_inv = 'E'
        columns_con = 0
        columns_dir = 0
        columns_inv = 0
        if course.new_table:
            # Conference
            parameter_group_con = self.get_parameter_by_param_name('023', matrix_id, '013')
            flag_con, columns_con, scores_array_con_prom, scores_array_users_con = self.get_detail_conference_summary(
                matrix_id)

            # Work Direction
            parameter_group_dir = self.get_parameter_by_param_name('024', matrix_id, '013')
            flag_dir, columns_dir, scores_array_dir_prom, scores_array_users_dir = self.get_detail_tdd_summary(
                matrix_id)

            # Search
            parameter_group_inv = self.get_parameter_by_param_name('032', matrix_id, '013')
            flag_inv, columns_inv, scores_array_inv_prom, scores_array_users_inv = self.get_detail_tdi_summary(
                matrix_id)

        # crear arreglo de notas
        if course.new_table:
            columns += columns_games + columns_thesis + columns_mono + columns_essay + columns_group_essay + \
                       columns_con + columns_dir + columns_inv
        else:
            columns += columns_games + columns_thesis + columns_mono + columns_essay + columns_group_essay + \
                       columns_productivity

        if columns > 4:
            columns += 2

            num_students = len(scores_array_users)
            scores_array = [[0 for j in range(columns)] for i in range(num_students)]
            w = 0
            for x in range(num_students):
                z = 0
                for y in range(4):
                    scores_array[w][z] = scores_array_users[x][y]
                    z += 1
                w += 1

            position_array = 4
            if flag_thesis:
                w = 0
                longitude = 0
                for x in range(num_students):
                    z = position_array
                    longitude = len(scores_array_thesis_prom[x])
                    for y in range(longitude):
                        scores_array[w][z] = scores_array_thesis_prom[x][y]
                        z += 1
                    w += 1
                position_array += longitude
            elif flag_thesis_exists:
                flag_average = False
                w = 0
                longitude = 0
                for x in range(num_students):
                    z = position_array
                    longitude = 2
                    for y in range(longitude):
                        if w == 0:
                            if y == 0:
                                scores_array[w][z] = parameter_thesis.param_name.short_name
                            else:
                                scores_array[w][z] = "*%s" % parameter_thesis.coefficient
                        else:
                            scores_array[w][z] = "--"
                        z += 1
                    w += 1
                position_array += longitude

            if flag_mono:
                w = 0
                longitude = 0
                for x in range(num_students):
                    z = position_array
                    longitude = len(scores_array_mono_prom[x])
                    for y in range(longitude):
                        scores_array[w][z] = scores_array_mono_prom[x][y]
                        z += 1
                    w += 1
                position_array += longitude
            elif flag_mono_exists:
                flag_average = False
                w = 0
                longitude = 0
                for x in range(num_students):
                    z = position_array
                    longitude = 2
                    for y in range(longitude):
                        if w == 0:
                            if y == 0:
                                scores_array[w][z] = parameter_mono.param_name.short_name
                            else:
                                scores_array[w][z] = "*%s" % parameter_mono.coefficient
                        else:
                            scores_array[w][z] = "--"
                        z += 1
                    w += 1
                position_array += longitude

            if flag_con == 'OK':
                w = 0
                longitude = 0
                for x in range(num_students):
                    z = position_array
                    longitude = len(scores_array_con_prom[x])
                    for y in range(longitude):
                        scores_array[w][z] = scores_array_con_prom[x][y]
                        z += 1
                    w += 1
                position_array += longitude
            elif columns_con > 0:
                flag_average = False
                w = 0
                longitude = 0
                for x in range(num_students):
                    z = position_array
                    longitude = 2
                    for y in range(longitude):
                        if w == 0:
                            if y == 0:
                                scores_array[w][z] = parameter_group_con.param_name.short_name
                            else:
                                scores_array[w][1] = "*%s" % parameter_group_con.coefficient
                        else:
                            scores_array[w][z] = "--"
                        z += 1
                    w += 1
                position_array += longitude

            if flag_dir == 'OK':
                w = 0
                longitude = 0
                for x in range(num_students):
                    z = position_array
                    longitude = len(scores_array_dir_prom[x])
                    for y in range(longitude):
                        scores_array[w][z] = scores_array_dir_prom[x][y]
                        z += 1
                    w += 1
                position_array += longitude
            elif columns_dir > 0:
                flag_average = False
                w = 0
                longitude = 0
                for x in range(num_students):
                    z = position_array
                    longitude = 2
                    for y in range(longitude):
                        if w == 0:
                            if y == 0:
                                scores_array[w][z] = parameter_group_dir.param_name.short_name
                            else:
                                scores_array[w][1] = "*%s" % parameter_group_dir.coefficient
                        else:
                            scores_array[w][z] = "--"
                        z += 1
                    w += 1
                position_array += longitude

            if flag_inv == 'OK':
                w = 0
                longitude = 0
                for x in range(num_students):
                    z = position_array
                    longitude = len(scores_array_inv_prom[x])
                    for y in range(longitude):
                        scores_array[w][z] = scores_array_inv_prom[x][y]
                        z += 1
                    w += 1
                position_array += longitude
            elif columns_inv > 0:
                flag_average = False
                w = 0
                longitude = 0
                for x in range(num_students):
                    z = position_array
                    longitude = 2
                    for y in range(longitude):
                        if w == 0:
                            if y == 0:
                                scores_array[w][z] = parameter_group_inv.param_name.short_name
                            else:
                                scores_array[w][1] = "*%s" % parameter_group_inv.coefficient
                        else:
                            scores_array[w][z] = "--"
                        z += 1
                    w += 1
                position_array += longitude

            # promedio
            w = 0
            for x in range(num_students):
                if w == 0:
                    scores_array[w][columns - 2] = parameter.param_name.short_name
                    coefficient_pro_text = '*%s' % coefficient_pro
                    scores_array[w][columns - 1] = coefficient_pro_text.replace('.', ',')
                else:
                    if columns == 8:
                        if scores_array[w][columns - 3] == '--':
                            value = 0
                        else:
                            value = scores_array[w][columns - 3]
                        prom = util.round_sie(decimal.Decimal(value), self.get_sie_digits())
                        prom_coefficient = util.round_sie(decimal.Decimal(prom) * decimal.Decimal(coefficient_pro),
                                                          self.get_sie_digits())
                        scores_array[w][columns - 2] = util.format_sie(prom, self.get_sie_digits())
                        scores_array[w][columns - 1] = util.format_sie(prom_coefficient, self.get_sie_digits())
                    if columns == 10:
                        if scores_array[w][columns - 3] == '--':
                            value_3 = 0
                            value_3_alt = 0
                        else:
                            value_3 = scores_array[w][columns - 3]
                            value_3_alt = scores_array[w][columns - 4]
                        if scores_array[w][columns - 5] == '--':
                            value_5 = 0
                            value_5_alt = 0
                        else:
                            value_5 = scores_array[w][columns - 5]
                            value_5_alt = scores_array[w][columns - 6]
                        if value_3 == 0 or value_5 == 0:
                            prom = util.round_sie(decimal.Decimal(value_3_alt) +
                                                  decimal.Decimal(value_5_alt), self.get_sie_digits())
                            prom_coefficient = util.round_sie(decimal.Decimal(prom) * decimal.Decimal(coefficient_pro),
                                                              self.get_sie_digits())
                        else:
                            prom = util.round_sie(decimal.Decimal(value_3) +
                                                  decimal.Decimal(value_5), self.get_sie_digits())
                            prom_coefficient = util.round_sie(decimal.Decimal(prom) * decimal.Decimal(coefficient_pro),
                                                              self.get_sie_digits())
                        scores_array[w][columns - 2] = util.format_sie(prom, self.get_sie_digits())
                        scores_array[w][columns - 1] = util.format_sie(prom_coefficient, self.get_sie_digits())
                    if columns == 12:
                        if scores_array[w][columns - 3] == '--':
                            value_3 = 0
                            value_3_alt = 0
                        else:
                            value_3 = scores_array[w][columns - 3]
                            value_3_alt = scores_array[w][columns - 4]
                        if scores_array[w][columns - 5] == '--':
                            value_5 = 0
                            value_5_alt = 0
                        else:
                            value_5 = scores_array[w][columns - 5]
                            value_5_alt = scores_array[w][columns - 6]
                        if scores_array[w][columns - 7] == '--':
                            value_7 = 0
                            value_7_alt = 0
                        else:
                            value_7 = scores_array[w][columns - 7]
                            value_7_alt = scores_array[w][columns - 8]
                        if value_3 == 0 or value_5 == 0 or value_7 == 0:
                            prom = util.round_sie(decimal.Decimal(value_3_alt) +
                                                  decimal.Decimal(value_5_alt) +
                                                  decimal.Decimal(value_7_alt), self.get_sie_digits())
                            prom_coefficient = util.round_sie(decimal.Decimal(prom) * decimal.Decimal(coefficient_pro),
                                                              self.get_sie_digits())
                        else:
                            prom = util.round_sie(decimal.Decimal(value_3) + decimal.Decimal(value_5) +
                                                  decimal.Decimal(value_7), self.get_sie_digits())
                            prom_coefficient = util.round_sie(decimal.Decimal(prom) * decimal.Decimal(coefficient_pro),
                                                              self.get_sie_digits())
                        scores_array[w][columns - 2] = util.format_sie(prom, self.get_sie_digits())
                        scores_array[w][columns - 1] = util.format_sie(prom_coefficient, self.get_sie_digits())
                    if columns == 14:
                        if scores_array[w][columns - 3] == '--':
                            value_3 = 0
                            value_3_alt = 0
                        else:
                            value_3 = scores_array[w][columns - 3]
                            value_3_alt = scores_array[w][columns - 4]
                        if scores_array[w][columns - 5] == '--':
                            value_5 = 0
                            value_5_alt = 0
                        else:
                            value_5 = scores_array[w][columns - 5]
                            value_5_alt = scores_array[w][columns - 6]
                        if scores_array[w][columns - 7] == '--':
                            value_7 = 0
                            value_7_alt = 0
                        else:
                            value_7 = scores_array[w][columns - 7]
                            value_7_alt = scores_array[w][columns - 8]
                        if scores_array[w][columns - 9] == '--':
                            value_9 = 0
                            value_9_alt = 0
                        else:
                            value_9 = scores_array[w][columns - 9]
                            value_9_alt = scores_array[w][columns - 10]
                        if value_3 == 0 or value_5 == 0 or value_7 == 0 or value_9 == 0:
                            prom = util.round_sie(decimal.Decimal(value_3_alt) +
                                                  decimal.Decimal(value_5_alt) +
                                                  decimal.Decimal(value_7_alt) +
                                                  decimal.Decimal(value_9_alt)
                                                  , self.get_sie_digits())
                            prom_coefficient = util.round_sie(decimal.Decimal(prom) * decimal.Decimal(coefficient_pro),
                                                              self.get_sie_digits())
                        else:
                            prom = util.round_sie(decimal.Decimal(value_3) + decimal.Decimal(value_5) +
                                                  decimal.Decimal(value_7) + decimal.Decimal(value_9),
                                                  self.get_sie_digits())
                            prom_coefficient = util.round_sie(decimal.Decimal(prom) * decimal.Decimal(coefficient_pro),
                                                              self.get_sie_digits())
                        scores_array[w][columns - 2] = util.format_sie(prom, self.get_sie_digits())
                        scores_array[w][columns - 1] = util.format_sie(prom_coefficient, self.get_sie_digits())
                    if columns == 16:
                        if scores_array[w][columns - 3] == '--':
                            value_3 = 0
                            value_3_alt = 0
                        else:
                            value_3 = scores_array[w][columns - 3]
                            value_3_alt = scores_array[w][columns - 4]
                        if scores_array[w][columns - 5] == '--':
                            value_5 = 0
                            value_5_alt = 0
                        else:
                            value_5 = scores_array[w][columns - 5]
                            value_5_alt = scores_array[w][columns - 6]
                        if scores_array[w][columns - 7] == '--':
                            value_7 = 0
                            value_7_alt = 0
                        else:
                            value_7 = scores_array[w][columns - 7]
                            value_7_alt = scores_array[w][columns - 8]
                        if scores_array[w][columns - 9] == '--':
                            value_9 = 0
                            value_9_alt = 0
                        else:
                            value_9 = scores_array[w][columns - 9]
                            value_9_alt = scores_array[w][columns - 10]
                        if scores_array[w][columns - 11] == '--':
                            value_11 = 0
                            value_11_alt = 0
                        else:
                            value_11 = scores_array[w][columns - 11]
                            value_11_alt = scores_array[w][columns - 12]
                        if value_3 == 0 or value_5 == 0 or value_7 == 0 or value_9 == 0 or value_11 == 0:
                            prom = util.round_sie(decimal.Decimal(value_3_alt) +
                                                  decimal.Decimal(value_5_alt) +
                                                  decimal.Decimal(value_7_alt) +
                                                  decimal.Decimal(value_9_alt) +
                                                  decimal.Decimal(value_11_alt)
                                                  , self.get_sie_digits())
                            prom_coefficient = util.round_sie(decimal.Decimal(prom) * decimal.Decimal(coefficient_pro),
                                                              self.get_sie_digits())
                        else:
                            prom = util.round_sie(decimal.Decimal(value_3) + decimal.Decimal(value_5) +
                                                  decimal.Decimal(value_7) + decimal.Decimal(value_9) +
                                                  decimal.Decimal(value_11),
                                                  self.get_sie_digits())
                            prom_coefficient = util.round_sie(decimal.Decimal(prom) * decimal.Decimal(coefficient_pro),
                                                              self.get_sie_digits())
                        scores_array[w][columns - 2] = util.format_sie(prom, self.get_sie_digits())
                        scores_array[w][columns - 1] = util.format_sie(prom_coefficient, self.get_sie_digits())
                w += 1

        else:
            scores_array = []

        return scores_array
