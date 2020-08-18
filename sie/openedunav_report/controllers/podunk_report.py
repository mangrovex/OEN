#!/usr/bin/env python
#  -*- coding: UTF-8 -*-

from manexreport.project.report import Report
from manexreport.widget.table import Table
from manexreport.widget.heading import Heading
from manexreport.widget.heading_array import HeadingArray
from manexreport.widget.pagebreak import PageBreak
from manexreport.prefab import alignment
import manexreport.prefab.paper as paper_type


def get_heading(report, course_name, promotion_name, title_report, full_title=None, teacher_title=None,
                detail_title=None,
                deviation_title=None):
    report.author = ' '
    report.department = ' '
    report.add(Heading('ACADEMIA DE GUERRA NAVAL', 2, True, 20, alignment.CENTER, 8, False, False))
    report.add(Heading(title_report, 0, True, 20, alignment.LEFT, 8, False,
                       False))
    report.add(Heading('CURSO:  %s' % course_name, 1, True, 13, alignment.LEFT, 8, False, False))
    report.add(Heading(u'PROMOCIÓN:  %s' % promotion_name, 1, True, 13, alignment.LEFT, 8, False, False))
    if full_title:
        report.add(Heading(full_title, 2, False, 10, alignment.LEFT, 8, False, False))
    if deviation_title:
        line1_0 = '                                                                      '
        line1_1 = '                                                                      '
        line1_2 = '                                                                      '
        line1_3 = u'%s' % deviation_title
        report.add(HeadingArray([line1_0, line1_1, line1_2, line1_3], 2, False, 10, alignment.RIGHT, 8, False, False))
    if detail_title:
        report.add(Heading(detail_title, 2, False, 10, alignment.LEFT, 8, False, False))
    if teacher_title:
        report.add(Heading(teacher_title, 2, False, 10, alignment.LEFT, 8, False, False))


def get_heading_score_final(report, course_name, promotion_name, title_report, full_title, teacher_title=None,
                            deviation_title=None):
    report.author = ' '
    report.department = ' '
    report.add(Heading('ACADEMIA DE GUERRA NAVAL', 2, True, 20, alignment.CENTER, 8, False, False))
    report.add(Heading(title_report, 0, True, 20, alignment.LEFT, 8, False,
                       False))
    report.add(Heading('CURSO:  %s' % course_name, 1, True, 13, alignment.LEFT, 8, False, False))
    line1_0 = u'PROMOCIÓN : '
    line1_1 = u'%s  ' % promotion_name
    line1_2 = u'               %s ' % teacher_title
    line1_3 = '         '
    line1_4 = u'%s' % deviation_title

    report.add(HeadingArray([line1_0, line1_1, line1_2, line1_3, line1_3, line1_4], 1, False, 10, alignment.LEFT,
                            8, False, False))

    heading = Heading(' ', 3, False, 10, alignment.RIGHT, 8, False, False)
    report.add(heading)


def get_table(number, grade, fullname):
    table = Table()
    if number != None:
        col = table.add_column(number)
        col.width = 15
        col.row.style.horizontal_alignment = alignment.LEFT
    col = table.add_column(grade)
    col.width = 40
    col.row.style.horizontal_alignment = alignment.LEFT
    col = table.add_column(fullname)
    col.width = 200
    col.row.style.horizontal_alignment = alignment.LEFT
    return table


def populate_table(columns, scores_array, column_width, rows, column_start, column_end):
    if column_width == 90:
        table = get_table(None, scores_array[0][0], scores_array[0][1])
        column_range = column_end
        column_start = 2
    else:
        table = get_table(scores_array[0][0], scores_array[0][1], scores_array[0][2])
        column_range = 3 + column_end - column_start
    y_range = column_start - 1
    for j in range(column_start, column_end):
        col = table.add_column(scores_array[0][j])
        col.width = column_width
        col.row.style.horizontal_alignment = alignment.CENTER
    scores_array_2 = [[0 for m in range(column_range)] for n in range(rows - 1)]
    w = 0
    for x in range(len(scores_array)):
        if x != 0:
            z = 0
            for y in range(len(scores_array[x])):
                if (y < 3) or ((y > y_range) and (y < column_end)):
                    scores_array_2[w][z] = scores_array[x][y]
                    z += 1
            w += 1
    for row in scores_array_2:
        table.add_row(row)
    return table


def get_report(scores_array, column_width):
    rows = len(scores_array)
    columns = len(scores_array[0])
    table = table1 = table2 = table3 = table4 = tabla5 = Table()
    flag = 0
    if columns <= 17:
        flag = 1
        table = populate_table(columns, scores_array, column_width, rows, 3, columns)
    elif (columns > 17) and (columns <= 31):
        flag = 2
        table = populate_table(columns, scores_array, column_width, rows, 3, 17)
        table1 = populate_table(columns, scores_array, column_width, rows, 17, columns)
    elif columns > 31 and (columns <= 45):
        flag = 3
        table = populate_table(columns, scores_array, column_width, rows, 3, 17)
        table1 = populate_table(columns, scores_array, column_width, rows, 17, 31)
        table2 = populate_table(columns, scores_array, column_width, rows, 31, columns)
    elif columns > 45 and (columns <= 59):
        flag = 4
        table = populate_table(columns, scores_array, column_width, rows, 3, 17)
        table1 = populate_table(columns, scores_array, column_width, rows, 17, 31)
        table2 = populate_table(columns, scores_array, column_width, rows, 31, 45)
        table3 = populate_table(columns, scores_array, column_width, rows, 45, columns)
    elif columns > 59 and (columns <= 73):
        flag = 5
        table = populate_table(columns, scores_array, column_width, rows, 3, 17)
        table1 = populate_table(columns, scores_array, column_width, rows, 17, 31)
        table2 = populate_table(columns, scores_array, column_width, rows, 31, 45)
        table3 = populate_table(columns, scores_array, column_width, rows, 45, 59)
        table4 = populate_table(columns, scores_array, column_width, rows, 59, columns)
    elif columns > 73:
        flag = 6
        table = populate_table(columns, scores_array, column_width, rows, 3, 17)
        table1 = populate_table(columns, scores_array, column_width, rows, 17, 31)
        table2 = populate_table(columns, scores_array, column_width, rows, 31, 45)
        table3 = populate_table(columns, scores_array, column_width, rows, 45, 59)
        table4 = populate_table(columns, scores_array, column_width, rows, 59, 73)
        table5 = populate_table(columns, scores_array, column_width, rows, 59, columns)
    return flag, table, table1, table2, table3, table4, tabla5


def report_pdf(full_path, scores_array, course_name, promotion_name, title_report, full_title=None, teacher_title=None,
               detail_title=None, final=None, boss_name=None, boss_title=None, deviation_title=None):
    report = Report(full_path, paper_type.A4_LANDSCAPE, None, None, None, None, None, True, True)
    if final == True:

        get_heading_score_final(report, course_name, promotion_name, title_report, full_title, teacher_title,
                                deviation_title)
    else:
        get_heading(report, course_name, promotion_name, title_report, full_title, teacher_title, detail_title,
                    deviation_title)
    if scores_array:
        if final == True:
            column_with = 90
        else:
            column_with = 30
        flag, table, table1, table2, table3, table4, table5 = get_report(scores_array, column_with)
        if flag == 1:
            report.add(table)
        elif flag == 2:
            report.add(table)
            report.add(PageBreak())
            get_heading(report, course_name, promotion_name, title_report, full_title, teacher_title, detail_title)
            report.add(table1)
        elif flag == 3:
            report.add(table)
            report.add(PageBreak())
            get_heading(report, course_name, promotion_name, title_report, full_title, teacher_title, detail_title)
            report.add(table1)
            report.add(PageBreak())
            get_heading(report, course_name, promotion_name, title_report, full_title, teacher_title, detail_title)
            report.add(table2)
        elif flag == 4:
            report.add(table)
            report.add(PageBreak())
            get_heading(report, course_name, promotion_name, title_report, full_title, teacher_title, detail_title)
            report.add(table1)
            report.add(PageBreak())
            get_heading(report, course_name, promotion_name, title_report, full_title, teacher_title, detail_title)
            report.add(table2)
            report.add(PageBreak())
            get_heading(report, course_name, promotion_name, title_report, full_title, teacher_title, detail_title)
            report.add(table3)
        elif flag == 5:
            report.add(table)
            report.add(PageBreak())
            get_heading(report, course_name, promotion_name, title_report, full_title, teacher_title, detail_title)
            report.add(table1)
            report.add(PageBreak())
            get_heading(report, course_name, promotion_name, title_report, full_title, teacher_title, detail_title)
            report.add(table2)
            report.add(PageBreak())
            get_heading(report, course_name, promotion_name, title_report, full_title, teacher_title, detail_title)
            report.add(table3)
            report.add(PageBreak())
            get_heading(report, course_name, promotion_name, title_report, full_title, teacher_title, detail_title)
            report.add(table4)
        elif flag == 6:
            report.add(table)
            report.add(PageBreak())
            get_heading(report, course_name, promotion_name, title_report, full_title, teacher_title, detail_title)
            report.add(table1)
            report.add(PageBreak())
            get_heading(report, course_name, promotion_name, title_report, full_title, teacher_title, detail_title)
            report.add(table2)
            report.add(PageBreak())
            get_heading(report, course_name, promotion_name, title_report, full_title, teacher_title, detail_title)
            report.add(table3)
            report.add(PageBreak())
            get_heading(report, course_name, promotion_name, title_report, full_title, teacher_title, detail_title)
            report.add(table4)
            report.add(PageBreak())
            get_heading(report, course_name, promotion_name, title_report, full_title, teacher_title, detail_title)
            report.add(table5)
    if final == True:
        table_signature = Table()
        col = table_signature.add_column('col1')
        col.row.style.horizontal_alignment = alignment.CENTER
        table_signature.add_row(['  ', ])
        table_signature.add_row(['  ', ])
        table_signature.add_row(['  ', ])
        table_signature.add_row(['  ', ])
        # table_signature.add_row(['  ', ])
        table_signature.add_row(['______________________________________________________', ])
        table_signature.add_row([u'%s' % boss_name, ])
        table_signature.add_row([u'%s' % boss_title, ])
        table_signature.add_row([u'EL JEFE DEL DEPARTAMENTO DE ESTADÍSTICA Y EVALUACIÓN', ])
        table_signature.auto_grow(report.canvas, report.page_width)
        table_signature.set_drew_header(True)
        table_signature.set_flag(False)
        report.add(table_signature)
    report.create()
