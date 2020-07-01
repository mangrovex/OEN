# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

from manexreport.project.report import Report
from manexreport.widget.table import Table
from manexreport.widget.heading import Heading
from manexreport.widget.heading_array import HeadingArray
from manexreport.widget.pagebreak import PageBreak
from manexreport.prefab import alignment
import manexreport.prefab.paper as paper_type

# from openedunav.openedunav_school.controllers.util import format_sie


def get_heading(report, course_name, promotion_name, year, student_name, student_nuc, t_hours, credit, start_date,
                end_date, index):
    report.author = ' '
    report.department = ' '
    report.add(Heading('ARMADA DEL ECUADOR', 1, False, 7, alignment.CENTER, 8, False, False))
    report.add(Heading('ACADEMIA DE GUERRA NAVAL', 2, False, 7, alignment.CENTER, 8, False, False))
    report.add(Heading('Guayaquil', 5, False, 7, alignment.CENTER, 8, False, False))
    report.add(Heading('CERTIFICADO DE ESTUDIOS', 3, True, 14, alignment.CENTER, 8, False, False))
    line1_0 = 'CURSO : '
    line1_1 = u'%s' % course_name
    line1_2 = u'          PROMOCIÓN : '
    line1_3 = u'%s  ' % promotion_name
    line1_4 = u'          AÑO : '
    line1_5 = u'%s' % year
    report.add(HeadingArray([line1_0, line1_1.ljust(83 - len(line1_1)), line1_2, line1_3, line1_4, line1_5], 1, False,
                            10, alignment.CENTER, 8, False, False))
    line2_0 = 'OFICIAL ALUMNO : '
    line2_1 = u'%s                             ' % student_name
    report.add(HeadingArray([line2_0, line2_1], 1, False, 10, alignment.CENTER, 8, False, False))
    line3_0 = u'No. CÉDULA : '
    line3_1 = u'%s               ' % student_nuc
    line3_2 = u'       TOTAL HORAS : '
    line3_3 = u'%s      ' % t_hours
    line3_4 = u'        CRÉDITOS : '
    line3_5 = u'%s' % credit
    report.add(HeadingArray([line3_0, line3_1, line3_2, line3_3, line3_4, line3_5], 1, False, 10, alignment.CENTER,
                            8, False, False))
    line4_0 = 'FECHA DE INICIO : '
    line4_1 = u'%s               ' % start_date
    line4_2 = u'FECHA DE FINALIZACIÓN : '
    line4_3 = u'%s' % end_date
    report.add(HeadingArray([line4_0, line4_1, line4_2, line4_3], 1, False, 10, alignment.CENTER, 8, False, False))
    report.add(Heading('  ', 3, False, 7, alignment.CENTER, 8, False, False))


def get_table(subject, average, coefficient, score_final):
    table = Table()
    col = table.add_column(subject)
    col.width = 300
    col.row.style.horizontal_alignment = alignment.LEFT
    col = table.add_column(average)
    col.width = 50
    col.row.style.horizontal_alignment = alignment.CENTER
    col = table.add_column(coefficient)
    col.width = 50
    col.row.style.horizontal_alignment = alignment.CENTER
    col = table.add_column(score_final)
    col.width = 50
    col.row.style.horizontal_alignment = alignment.CENTER
    return table


def get_report(scores_array):
    table = get_table(u'MATERIAS', u'PROMEDIO', u'COEFICIENTE', u'NOTA FINAL')
    for row in scores_array:
        table.add_row(row)
    return table


def report_pdf(full_path, scores_array, course_name, promotion_name, year, student_name, student_nuc, student_id,
               subjects, t_hours, credit, start_date, end_date, logo_path, date_now, boss_name, boss_title,
               director_name, director_title, score_array_summary, score_array_summary_final, array_seminaries,
               child_course, child_achievement, flag_new_table):
    report = Report(full_path, paper_type.A4_PORTRAIT, None, 40, 30, 40, 20, False, False, True, logo_path,
                    40, 40, 50)
    page_width = report.page_width - report.left_margin - report.right_margin

    if student_name:
        longitude = len(student_name)
        for index in range(longitude):
            get_heading(report, course_name, promotion_name, year, student_name[index], student_nuc[index],
                        t_hours, credit, start_date, end_date, index + 1)
            num_students = len(score_array_summary) - 1
            if flag_new_table:
                score_array, seniority = get_certificate_scores_array_new_table(student_id[index], scores_array,
                                                                                subjects,
                                                                                score_array_summary,
                                                                                score_array_summary_final,
                                                                                child_course, child_achievement)
            else:
                score_array, seniority = get_certificate_scores_array(student_id[index], scores_array, subjects,
                                                                      score_array_summary, score_array_summary_final,
                                                                      child_course, child_achievement)
            if score_array:
                table = get_report(score_array)
                try:
                    table.auto_grow(report.canvas, page_width)
                except:
                    pass
                list_columns = [subjects + 1, subjects + 2, subjects + 3, subjects + 4, subjects + 5, subjects + 6,
                                subjects + 7]
                table.set_flag(True, list_columns)
                report.add(table)

            table_seniority = Table()
            col = table_seniority.add_column('col1')
            col.row.style.horizontal_alignment = alignment.LEFT
            col = table_seniority.add_column('col2')
            col.width = 50
            col.row.style.horizontal_alignment = alignment.RIGHT
            table_seniority.add_row([' ', ' ', ])
            if seniority != '--':
                table_seniority.add_row(
                    ['ANTIGUEDAD', '%s de %s           ' % (seniority, num_students), ])
            table_seniority.add_row([' ', ' '])
            if array_seminaries:
                table_seniority.add_row(['SEMINARIOS:', ' '])
                for row in array_seminaries:
                    table_seniority.add_row([row, ''])
            table_seniority.add_row([' ', ' '])
            table_seniority.add_row([' ', 'Guayaquil, %s' % date_now, ])
            table_seniority.auto_grow(report.canvas, page_width)
            table_seniority.set_drew_header(True)
            table_seniority.set_flag(False, [1])

            report.add(table_seniority)

            report.add(Heading('', 1, False, 8, alignment.CENTER, 18, False, False))

            table_signature = Table()
            col = table_signature.add_column('col1')
            col.row.style.horizontal_alignment = alignment.CENTER
            col = table_signature.add_column('col2')
            col.row.style.horizontal_alignment = alignment.CENTER
            if table.get_row_count() <= 35:
                table_signature.add_row(['  ', '  ', ])
                table_signature.add_row(['  ', '  ', ])
                table_signature.add_row(['  ', '  ', ])
                table_signature.add_row(['  ', '  ', ])
                table_signature.add_row(['  ', '  ', ])
                table_signature.add_row(['  ', '  ', ])
            table_signature.add_row(['EL JEFE DEL DEPARTAMENTO DE', 'EL DIRECTOR DE LA ACADEMIA', ])
            table_signature.add_row([u'ESTADÍSTICA Y EVALUACIÓN', 'DE GUERRA NAVAL', ])
            table_signature.add_row(['  ', '  ', ])
            table_signature.add_row(['  ', '  ', ])
            table_signature.add_row(['  ', '  ', ])
            table_signature.add_row(['____________________________', '____________________________', ])
            table_signature.add_row([u'%s' % boss_name, u'%s' % director_name, ])
            table_signature.add_row([u'%s' % boss_title, u'%s' % director_title, ])
            table_signature.auto_grow(report.canvas, page_width)
            table_signature.set_drew_header(True)
            table_signature.set_flag(False)
            report.add(table_signature)

            if index != longitude - 1:
                report.add(PageBreak())
    report.create()


def get_certificate_scores_array(student_id, scores_array_child, subjects, score_array_summary,
                                 score_array_summary_final, child_course=None, child_achievement=None):
    num_subjects = subjects
    num_columns = 4
    num_records = num_subjects + 3 + len(child_achievement) + len(child_course)

    scores_array = [[0 for j in range(num_columns)] for i in range(num_records)]
    flag = False
    if scores_array_child:
        data = scores_array_child
        try:
            longitude = len(data[0])
        except:
            longitude = 0
        if longitude > 0:
            position_x = -1
            for x in range(len(scores_array_child)):
                if x != 0:
                    if data[x][0] == '%s' % student_id:
                        position_x += 1
                        scores_array[position_x][0] = data[x][1]
                        scores_array[position_x][1] = data[x][2]
                        scores_array[position_x][2] = data[x][3]
                        scores_array[position_x][3] = data[x][4]
            position_x += 1
            scores_array[position_x][0] = '  '
            scores_array[position_x][1] = '  '
            scores_array[position_x][2] = '  '
            scores_array[position_x][3] = '  '
            position_x += 1
            for y in range(len(child_achievement)):
                position_x += y
                for w in range(len(score_array_summary)):
                    if w != 0:
                        if score_array_summary[w][3] == '%s' % student_id:
                            index = 4 + 2 * y
                            achievement_1 = score_array_summary[w][index]
                            achievement_2 = score_array_summary[0][index + 1]
                            achievement_3 = score_array_summary[w][index + 1]
                            break
                scores_array[position_x][0] = child_achievement[y].param_name.name  # u'APROVECHAMIENTO'
                try:
                    if achievement_1 != '--':
                        value = float(achievement_1)
                    else:
                        value = 0.0
                    if value < 10:
                        achievement_1 = ' %s' % achievement_1.rjust(len(achievement_1) + 1, ' ')
                        if len(achievement_1) < 8:
                            if achievement_1 == '  --':
                                achievement_1 = achievement_1.ljust(len(achievement_1) + 1, '-')
                            else:
                                achievement_1 = achievement_1.ljust(len(achievement_1) + 1, '0')
                    else:
                        if len(achievement_1) < 7:
                            achievement_1 = achievement_1.ljust(len(achievement_1) + 1, '0')
                    scores_array[position_x][1] = achievement_1.replace('.', ',')
                except:
                    flag = True
                    pass
                try:
                    scores_array[position_x][2] = achievement_2.replace('*', '')
                except:
                    pass
                try:
                    if achievement_3 != '--':
                        value = float(achievement_3)
                    else:
                        value = 0.0
                    if value < 10:
                        achievement_3 = ' %s' % achievement_3.rjust(len(achievement_3) + 1, ' ')
                        if len(achievement_3) < 8:
                            if achievement_3 == '  --':
                                achievement_3 = achievement_3.ljust(len(achievement_3) + 1, '-')
                            else:
                                achievement_3 = achievement_3.ljust(len(achievement_3) + 1, '0')
                    else:
                        if len(achievement_3) < 7:
                            achievement_3 = achievement_3.ljust(len(achievement_3) + 1, '0')
                    scores_array[position_x][3] = achievement_3.replace('.', ',')
                except:
                    pass
            position_x += 1
            scores_array[position_x][0] = '  '
            scores_array[position_x][1] = '  '
            scores_array[position_x][2] = '  '
            scores_array[position_x][3] = '  '
            position_x += 1
            for y in range(len(child_course)):
                for w in range(len(score_array_summary_final)):
                    if w != 0:
                        if score_array_summary_final[w][3] == '%s' % student_id:
                            achievement_1 = score_array_summary_final[0][4 + y].split()
                            longitude = len(achievement_1)
                            coefficient = achievement_1[longitude - 1].replace(',', '.')
                            achievement_2 = score_array_summary_final[w][4 + y]
                            final = achievement_2.replace(',', '.')
                            value = float(final) / float(coefficient)
                            scores_array[position_x][0] = child_course[y].name  # u'APRENDIZAJE'
                            value_str = '%s' % format_sie(value, 4)
                            if value < 10:
                                value_str = ' %s' % value_str.rjust(len(value_str) + 1, ' ')
                                if len(value_str) < 8:
                                    value_str = value_str.ljust(len(value_str) + 1, '0')
                            else:
                                if len(value_str) < 7:
                                    value_str = value_str.ljust(len(value_str) + 1, '0')
                            scores_array[position_x][1] = value_str.replace('.', ',')
                            scores_array[position_x][2] = coefficient.replace('.', ',')
                            value_2 = float(achievement_2)
                            if value_2 < 10:
                                achievement_2 = ' %s' % achievement_2.rjust(len(achievement_2) + 1, ' ')
                                if len(achievement_2) < 8:
                                    achievement_2 = achievement_2.ljust(len(achievement_2) + 1, '0')
                            else:
                                if len(achievement_2) < 7:
                                    achievement_2 = achievement_2.ljust(len(achievement_2) + 1, '0')
                            scores_array[position_x][3] = achievement_2.replace('.', ',')
                            break
                position_x += 1

            for w in range(len(score_array_summary_final)):
                if w != 0:
                    if score_array_summary_final[w][3] == '%s' % student_id:
                        longitude = len(score_array_summary_final[0])
                        achievement_final = score_array_summary_final[w][longitude - 2]
                        achievement_seniority = score_array_summary_final[w][longitude - 1]
                        scores_array[position_x][0] = u'PROMEDIO FINAL'
                        scores_array[position_x][1] = '  '
                        scores_array[position_x][2] = '  '
                        scores_array[position_x][3] = achievement_final.replace('.', ',')
                        break
        else:
            scores_array = []
            achievement_seniority = '--'
    else:
        scores_array = []
        achievement_seniority = '--'
    try:
        achievement_seniority_result = '%s' % achievement_seniority
    except:
        achievement_seniority_result = '--'
        scores_array = []
        pass
    return scores_array, '%s' % achievement_seniority_result


def get_certificate_scores_array_new_table(student_id, scores_array_child, subjects, score_array_summary,
                                           score_array_summary_final, child_course=None, child_achievement=None):
    num_subjects = subjects
    num_columns = 4
    num_records = num_subjects + 3 + len(child_course)

    scores_array = [[0 for j in range(num_columns)] for i in range(num_records)]
    flag = False
    if scores_array_child:
        data = scores_array_child
        try:
            longitude = len(data[0])
        except:
            longitude = 0
        if longitude > 0:
            position_x = -1
            for x in range(len(scores_array_child)):
                if x != 0:
                    if data[x][0] == '%s' % student_id:
                        position_x += 1
                        scores_array[position_x][0] = data[x][1]
                        scores_array[position_x][1] = data[x][2]
                        scores_array[position_x][2] = data[x][3]
                        scores_array[position_x][3] = data[x][4]
            position_x += 1
            scores_array[position_x][0] = '  '
            scores_array[position_x][1] = '  '
            scores_array[position_x][2] = '  '
            scores_array[position_x][3] = '  '
            position_x += 1
            scores_array[position_x][0] = '  '
            scores_array[position_x][1] = '  '
            scores_array[position_x][2] = '  '
            scores_array[position_x][3] = '  '
            position_x += 1
            for y in range(len(child_course)):
                for w in range(len(score_array_summary_final)):
                    if w != 0:
                        if score_array_summary_final[w][3] == '%s' % student_id:
                            achievement_1 = score_array_summary_final[0][4 + y].split()
                            longitude = len(achievement_1)
                            coefficient = achievement_1[longitude - 1].replace(',', '.')
                            achievement_2 = score_array_summary_final[w][4 + y]
                            final = achievement_2.replace(',', '.')
                            value = float(final) / float(coefficient)
                            scores_array[position_x][0] = child_course[y].name  # u'APRENDIZAJE'
                            value_str = '%s' % format_sie(value, 4)
                            if value < 10:
                                value_str = ' %s' % value_str.rjust(len(value_str) + 1, ' ')
                                if len(value_str) < 8:
                                    value_str = value_str.ljust(len(value_str) + 1, '0')
                            else:
                                if len(value_str) < 7:
                                    value_str = value_str.ljust(len(value_str) + 1, '0')
                            scores_array[position_x][1] = value_str.replace('.', ',')
                            scores_array[position_x][2] = coefficient.replace('.', ',')
                            value_2 = float(achievement_2)
                            if value_2 < 10:
                                achievement_2 = ' %s' % achievement_2.rjust(len(achievement_2) + 1, ' ')
                                if len(achievement_2) < 8:
                                    achievement_2 = achievement_2.ljust(len(achievement_2) + 1, '0')
                            else:
                                if len(achievement_2) < 7:
                                    achievement_2 = achievement_2.ljust(len(achievement_2) + 1, '0')
                            scores_array[position_x][3] = achievement_2.replace('.', ',')
                            break
                position_x += 1

            for w in range(len(score_array_summary_final)):
                if w != 0:
                    if score_array_summary_final[w][3] == '%s' % student_id:
                        longitude = len(score_array_summary_final[0])
                        achievement_final = score_array_summary_final[w][longitude - 2]
                        achievement_seniority = score_array_summary_final[w][longitude - 1]
                        scores_array[position_x][0] = u'PROMEDIO FINAL'
                        scores_array[position_x][1] = '  '
                        scores_array[position_x][2] = '  '
                        scores_array[position_x][3] = achievement_final.replace('.', ',')
                        break
        else:
            scores_array = []
            achievement_seniority = '--'
    else:
        scores_array = []
        achievement_seniority = '--'
    try:
        achievement_seniority_result = '%s' % achievement_seniority
    except:
        achievement_seniority_result = '--'
        scores_array = []
        pass
    return scores_array, '%s' % achievement_seniority_result
