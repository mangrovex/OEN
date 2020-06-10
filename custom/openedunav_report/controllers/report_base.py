#!/usr/bin/env python
#  -*- coding: UTF-8 -*-

import decimal
from operator import attrgetter

from odoo import http
from . import util as util


class ReportBase:
    'Common base class for all reports'
    scoreArray = []

    def __init__(self, local_tz, local_dt, subject_id=None, course_id=None, parameter_id=None,
                 evaluator_id=None,
                 direction_work_id=None,
                 war_games_report=None,
                 war_games_id=None,
                 judge_id=None,
                 student_id=None,
                 order=None):
        self.directory = self.get_directory()
        self.local_tz = local_tz
        self.local_dt = local_dt
        self.subject_id = subject_id
        self.course_id = course_id
        self.parameter_id = parameter_id
        self.evaluator_id = evaluator_id
        self.direction_work_id = direction_work_id
        self.war_games_report = war_games_report
        self.war_games_id = war_games_id
        self.judge_id = judge_id
        self.student_id = student_id
        self.order = order

    def get_directory(self):
        config_parameter = http.request.env['ir.config_parameter']
        parameter = config_parameter.search([('key', '=', 'sie_report_path')])
        if parameter:
            value = parameter.value
        else:
            value = '/opt/odoo/reports/'
        return value

    def get_directors(self, course_id):
        sie_course = http.request.env['sie.register.directors']
        director = sie_course.search([('course_id', '=', int(course_id))])
        return director

    def get_student(self, student_id):
        sie_course = http.request.env['sie.student']
        course = sie_course.search([('id', '=', int(student_id))])
        return course

    def get_enrollment(self, course_id):
        sie_enrollment = http.request.env['sie.enrollment']
        enrollment = sie_enrollment.search([('course_id', '=', int(course_id))])
        return enrollment

    def get_course(self, course_id):
        sie_course = http.request.env['sie.course']
        course = sie_course.search([('id', '=', int(course_id))])
        return course

    def get_param_name_by_code(self, parameter_code):
        sie_param_name = http.request.env['sie.param.name']
        parameter = sie_param_name.search([('code', '=', parameter_code)])
        return parameter

    def get_parameter_by_code(self, parameter_code, course_ref):
        sie_param_name = http.request.env['sie.param.name']
        param_name = sie_param_name.search([('code', '=', parameter_code)])
        matrix_parameter = http.request.env['sie.matrix.parameter']
        parameter = matrix_parameter.search([('param_name', '=', param_name.id), ('course_ref', '=', course_ref)])
        return parameter

    def get_parameter_by_id(self, parameter_id):
        matrix_parameter = http.request.env['sie.matrix.parameter']
        parameter = matrix_parameter.search([('id', '=', int(parameter_id))])
        return parameter

    def get_parameter_by_param_name(self, param_name_code, matrix_id, parent_ref_code=None):
        param_name = self.get_param_name_by_code(param_name_code)
        matrix_parameter = http.request.env['sie.matrix.parameter']
        if parent_ref_code:
            parameter = matrix_parameter.search([('course_ref', '=', matrix_id), ('param_name', '=', param_name.id),
                                                 ('parent_ref', 'like', parent_ref_code)])
        else:
            parameter = matrix_parameter.search([('course_ref', '=', matrix_id), ('param_name', '=', param_name.id)])
        return parameter

    def get_parameter_childs(self, parameter_id, matrix_id):
        parameter = self.get_parameter_by_id(parameter_id)
        matrix_parameter = http.request.env['sie.matrix.parameter']
        child_ids = matrix_parameter.search([('parent_ref', 'like', parameter.param_name.code),
                                             ('last_child', '=', True),
                                             ('course_ref', '=', matrix_id)])
        return child_ids

    def get_parameter_childs_by_course(self, matrix_id):
        matrix = http.request.env['sie.matrix']
        matrix_result = matrix.search([('id', '=', matrix_id)])
        return matrix_result.parameter_ids

    def get_students_course(self, course):
        students = http.request.env['sie.enrollment'] \
            .search([('course_id', '=', course.id)])
        students_actives = students.student_ids.filtered(lambda r: r.inactive == False)
        num_students = len(students_actives) + 1
        scores_array_users = [[0 for j in range(4)] for i in range(num_students)]
        for x in range(num_students):
            if x == 0:
                scores_array_users[x][0] = 'No.'
                scores_array_users[x][1] = 'Cargo'
                scores_array_users[x][2] = 'Nombres'
                scores_array_users[x][3] = 'ID'
            else:
                scores_array_users[x][0] = x
                scores_array_users[x][1] = students_actives[x - 1].grade_id.display_name
                scores_array_users[x][2] = students_actives[x - 1].full_name
                scores_array_users[x][3] = '%s' % students_actives[x - 1].id
        return scores_array_users

    def get_students_course_id(self, course_id):
        students = http.request.env['sie.enrollment'] \
            .search([('course_id', '=', course_id)])
        students_actives = students.student_ids.filtered(lambda r: r.inactive == False)
        num_students = len(students_actives) + 1
        scores_array_users = [[0 for j in range(4)] for i in range(num_students)]
        for x in range(num_students):
            if x == 0:
                scores_array_users[x][0] = 'No.'
                scores_array_users[x][1] = 'Cargo'
                scores_array_users[x][2] = 'Nombres'
                scores_array_users[x][3] = 'ID'
            else:
                scores_array_users[x][0] = x
                scores_array_users[x][1] = students_actives[x - 1].grade_id.display_name
                scores_array_users[x][2] = students_actives[x - 1].full_name
                scores_array_users[x][3] = '%s' % students_actives[x - 1].id
        return scores_array_users

    ######## Scores ########

    def get_subject_ids(self, course_id):
        subject_parameter = http.request.env['sie.subject']
        subject_ids = subject_parameter.search([('course_id', '=', int(course_id)), ('state', '!=', 'p'),
                                                ('plus_exec_hours', '=', True)])

        return subject_ids

    def get_subject_data(self, course, subject_id):
        subject_parameter = http.request.env['sie.subject']
        subject = subject_parameter.search([('id', '=', subject_id)])

        return subject.name, subject.hours, subject.running_hours, subject.coefficient, \
               subject.faculty_id.display_title_name

    def get_achievement_scores(self, parameter_id, course_id, subject_id):
        score_sie = http.request.env['sie.score']
        data = score_sie.search([('course_id', '=', int(course_id)), ('parameter_id', '=', parameter_id),
                                 ('subject_id', '=', int(subject_id)),
                                 ('state', '=', 'approved')])
        return data

    def get_achievement_scores_examen(self, quiz, score_number, course_id, subject_id):
        score_sie = http.request.env['sie.score']
        data = score_sie.search([('course_id', '=', int(course_id)), ('score_number', '=', score_number),
                                 ('subject_id', '=', int(subject_id)), ('quiz', '=', quiz),
                                 ('state', '=', 'approved')])
        return data

    def get_parameter_score_number(self, quiz, course_id, subject_id):
        score_sie = http.request.env['sie.score']
        data = score_sie.search([('course_id', '=', int(course_id)),
                                 ('subject_id', '=', int(subject_id)),
                                 ('quiz', '=', quiz),
                                 ('state', '=', 'approved')])
        return data

    def get_prom_score(self, num_child, scores_array_child, coefficient, title):
        num_columns = 6
        num_students = 0
        num_score = 0
        if num_child > 0:  # MVEGA
            for s in range(num_child):
                try:
                    num_students = len(scores_array_child[s])
                    if num_students > 0:
                        break
                except:
                    num_students = 0

            scores_array = [[0 for j in range(num_columns)] for i in range(num_students)]
            scores_array_prom = [[0 for j in range(2)] for i in range(num_students)]

            flag_user = False
            for w in range(num_child):
                data = scores_array_child[w]
                num_students = len(data)
                try:
                    longitude = len(data[0])
                except:
                    longitude = 0
                if not flag_user:
                    if longitude > 0:
                        num_score += 1
                        for x in range(num_students):
                            for y in range(4):
                                scores_array[x][y] = data[x][y]
                            if x == 0:
                                scores_array_prom[x][0] = title
                                coefficient_text = "*%s" % coefficient
                                scores_array_prom[x][1] = coefficient_text.replace('.', ',')
                            else:
                                value_2 = data[x][longitude - 2]
                                value_1 = data[x][longitude - 1]
                                if value_2 == '--':
                                    scores_array_prom[x][0] = value_2
                                else:
                                    scores_array_prom[x][0] = decimal.Decimal(value_2)
                                if value_1 == '--':
                                    scores_array_prom[x][1] = value_1
                                else:
                                    scores_array_prom[x][1] = decimal.Decimal(value_1)
                        flag_user = True
                else:
                    if longitude > 0:
                        num_score += 1
                        for x in range(num_students):
                            if x != 0:
                                value_2 = data[x][longitude - 2]
                                value_1 = data[x][longitude - 1]
                                if value_2 != '--':
                                    if (scores_array_prom[x][0] == '--'):
                                        scores_array_prom[x][0] = decimal.Decimal(value_2)
                                    else:
                                        scores_array_prom[x][0] += decimal.Decimal(value_2)
                                if value_1 != '--':
                                    if (scores_array_prom[x][1] == '--'):
                                        scores_array_prom[x][1] = decimal.Decimal(value_1)
                                    else:
                                        scores_array_prom[x][1] += decimal.Decimal(value_1)
            for x in range(num_students):
                if x == 0:
                    scores_array[x][num_columns - 2] = scores_array_prom[x][0]
                    scores_array[x][num_columns - 1] = scores_array_prom[x][1]
                else:
                    if scores_array_prom[x][0] == '--':
                        scores_array[x][num_columns - 2] = '--'
                        scores_array[x][num_columns - 1] = '--'
                    else:
                        prom = util.round_sie(scores_array_prom[x][1], self.get_sie_digits())
                        score_coefficient_tmp = prom * coefficient
                        score_coefficient = util.round_sie(float(score_coefficient_tmp),
                                                           self.get_sie_digits())
                        scores_array[x][num_columns - 2] = util.format_sie(prom, self.get_sie_digits())
                        scores_array[x][num_columns - 1] = util.format_sie(score_coefficient, self.get_sie_digits())
        else:
            scores_array = []
        return scores_array

    def get_detail_achievement(self, matrix_id, course_id, subject_id, coefficient):
        if course_id.new_table:
            parent_code = '001'
            parameter_parent = self.get_parameter_by_code('001', course_id.id)
        else:
            parent_code = '002'
            parameter_parent = self.get_parameter_by_param_name('002', matrix_id, '001')

        flag_pu = 0
        flag_apo = 0
        flag_vf = 0
        flag_pu_exam = 0

        parameter_pu = self.get_parameter_by_param_name('004', matrix_id, parent_code)
        parameter_pu_child_ids = self.get_parameter_childs(parameter_pu.id, matrix_id)
        coefficient_pu = parameter_pu.coefficient
        num_child_pu = 0
        scores_array_child_pu = [0 for u in range(len(parameter_pu_child_ids))]
        x = 0
        for parameter in parameter_pu_child_ids:
            data = self.get_achievement_scores(parameter.id, course_id, subject_id)
            if data:
                flag_pu = 1
                num_child_pu += 1
                title = parameter.param_name.short_name
                scores_array_child_pu[x] = self.get_scores_array_not_score_number(data, parameter.coefficient, True,
                                                                                  'sie.score.student', title)
            x += 1

        parameter_score_number = self.get_parameter_score_number('is_quiz_p', course_id, subject_id)
        num_child_pu_exam = 0
        scores_array_child_pu_exam = [0 for u in range(len(parameter_score_number))]
        x = 0
        for parameter in parameter_score_number:
            data = self.get_achievement_scores_examen('is_quiz_p', parameter.score_number, course_id, subject_id)
            if data:
                flag_pu_exam = 1
                num_child_pu_exam += 1
                title = 'EXAM'
                scores_array_child_pu_exam[x] = self.get_scores_array_by_score_number(data, 1, True,
                                                                                      'sie.score.student', 'EXAMENPU',
                                                                                      title)
            x += 1

        parameter_vf = self.get_parameter_by_param_name('009', matrix_id, parent_code)
        parameter_vf_child_ids = self.get_parameter_childs(parameter_vf.id, matrix_id)
        coefficient_vf = parameter_vf.coefficient
        num_child_vf = 0
        scores_array_child_vf = [0 for u in range(len(parameter_vf_child_ids))]
        x = 0
        for parameter in parameter_vf_child_ids:
            data = self.get_achievement_scores(parameter.id, course_id, subject_id)
            if data:
                flag_vf = 1
                num_child_vf += 1
                title = parameter.param_name.short_name
                scores_array_child_vf[x] = self.get_scores_array_not_score_number(data, parameter.coefficient, True,
                                                                                  'sie.score.student', title)
            x += 1

        if flag_vf == 0:
            parameter_score_number_vf = self.get_parameter_score_number('is_quiz_v', course_id, subject_id)
            num_child_vf = 0
            scores_array_child_vf = [0 for u in range(len(parameter_score_number_vf))]
            x = 0
            for parameter in parameter_score_number_vf:
                data = self.get_achievement_scores_examen('is_quiz_v', parameter.score_number, course_id, subject_id)
                if data:
                    flag_vf = 2
                    num_child_vf += 1
                    title = 'EXAM'
                    scores_array_child_vf[x] = self.get_scores_array_by_score_number(data, 1, True, 'sie.score.student',
                                                                                     'EXAMENVF', title)
                x += 1

        scores_array_child_apo = [0 for u in range(1)]
        parameter_apo = self.get_parameter_by_param_name('003', matrix_id, parent_code)
        if flag_pu == 0 and flag_pu_exam == 0:
            coefficient_apo = parameter_apo.coefficient + parameter_pu.coefficient
        else:
            coefficient_apo = parameter_apo.coefficient
        data = self.get_achievement_scores(parameter_apo.id, course_id, subject_id)
        if data:
            flag_apo = 1
            scores_array_child_apo = self.get_scores_array_not_score_number(data, coefficient_apo, True,
                                                                            'sie.score.student',
                                                                            parameter_apo.param_name.short_name)

        flag = flag_apo + flag_pu + flag_vf + flag_pu_exam
        if flag > 0:
            scores_array = [0 for u in range(flag)]
            scores_array_pu = [0 for u in range(1)]
            scores_array_pu_exam = [0 for u in range(1)]

            z = 0
            if flag_apo == 1:
                scores_array[z] = self.get_detail_one(1, scores_array_child_apo, coefficient_apo,
                                                      parameter_apo.param_name.short_name)
                z += 1
            flag_score_pu = 0
            if flag_pu == 1:
                scores_array_pu = self.get_detail(num_child_pu, scores_array_child_pu, coefficient_pu,
                                                  parameter_pu.param_name.short_name)
                flag_score_pu += 1
            if flag_pu_exam == 1:
                scores_array_pu_exam = self.get_detail_examen(num_child_pu_exam, scores_array_child_pu_exam, 1, 'EXPU')
                flag_score_pu += 2

            if flag_score_pu == 1:
                scores_array[z] = self.get_detail_pu(scores_array_pu, [], coefficient_pu)
                z += 1
            elif flag_score_pu == 2:
                scores_array[z] = self.get_detail_pu([], scores_array_pu_exam, coefficient_pu)
                z += 1
            elif flag_score_pu == 3:
                scores_array[z] = self.get_detail_pu(scores_array_pu, scores_array_pu_exam, coefficient_pu)
                z += 1

            if flag_vf == 1:
                scores_array[z] = self.get_detail(num_child_vf, scores_array_child_vf, coefficient_vf,
                                                  parameter_vf.param_name.short_name)
                z += 1
            elif flag_vf == 2:
                scores_array[z] = self.get_detail_examen_vf(num_child_vf, scores_array_child_vf, coefficient_vf, 'EXVF')
                z += 1

            score_array_report = self.get_detail_final(z, scores_array, coefficient,
                                                       parameter_parent.param_name.short_name)
        else:
            score_array_report = []

        return score_array_report

    def get_summary_achievement(self, course):
        matrix_id = course.matrix_id.id
        parameter_apre = self.get_parameter_by_param_name('001', matrix_id)
        coefficient_apre = parameter_apre.coefficient
        scores_array_report = []
        if course.new_table:
            scores_array_child_0 = self.get_summary_scores_array(course)
            if scores_array_child_0:
                scores_array_report = scores_array_child_0
        else:
            scores_array_child_0 = self.get_summary_scores_array(course)
            scores_array_child_1 = self.get_summary_integrator(course)
            x = 0;
            if scores_array_child_0:
                x += 1
            if scores_array_child_1:
                x += 1;
            scores_array_child = [0 for u in range(2)]
            if x == 1:
                parameter = self.get_parameter_by_param_name('013', course.matrix_id.id)
                coefficient_pro = parameter.coefficient
                param_name = parameter.param_name.short_name
                num_columns = len(scores_array_child_0[0])
                num_students = len(scores_array_child_0)
                scores_array_child_1 = [[0 for j in range(num_columns)] for i in range(num_students)]
                for x in range(num_students):
                    for y in range(num_columns):
                        if x == 0:
                            if y > 3:
                                scores_array_child_1[x][4] = param_name
                                scores_array_child_1[x][5] = ('*%s' % coefficient_pro).replace('.', ',')
                            else:
                                scores_array_child_1[x][y] = scores_array_child_0[x][y]
                        else:
                            if y > 3:
                                scores_array_child_1[x][y] = '--'
                            else:
                                scores_array_child_1[x][y] = scores_array_child_0[x][y]
                scores_array_child[0] = scores_array_child_0
                scores_array_child[1] = scores_array_child_1
            if x == 2:
                scores_array_child[0] = scores_array_child_0
                scores_array_child[1] = scores_array_child_1

            if scores_array_child[0]:
                scores_array_report = self.get_summary_scores(scores_array_child, coefficient_apre,
                                                              parameter_apre.param_name.short_name)
        return scores_array_report

    def get_summary_scores_array(self, course):
        subjects = self.get_subject_ids(course.id)
        matrix_id = course.matrix_id.id
        scores_array_report = []
        if course.new_table:
            parameter_apro = self.get_parameter_by_param_name('001', matrix_id)
            coefficient_apro = parameter_apro.coefficient
        else:
            parameter_apro = self.get_parameter_by_param_name('002', matrix_id)
            coefficient_apro = parameter_apro.coefficient
        longitude = len(subjects)
        if subjects:
            scores_array = [0 for u in range(longitude)]
            num_child = 0
            for subject in subjects:
                coefficient = util.round_sie(subject.coefficient, u'7')
                scores_array[num_child] = self.get_detail_achievement(matrix_id, course, subject.id,
                                                                      coefficient)
                num_child += 1
            scores_array_report = self.get_prom_score(num_child, scores_array, coefficient_apro,
                                                      parameter_apro.param_name.short_name)
        return scores_array_report

    def get_summary_scores_array_2column(self, course):
        data = self.get_summary_achievement(course)
        scores_array = self.get_summary_array_2column(data)
        return scores_array

    def get_summary_scores_array_1column(self, course):
        data = self.get_summary_achievement(course)
        if data:
            scores_array = self.get_summary_array_1column(data)
        else:
            scores_array = []
        return scores_array

    def get_summary_scores_array_subject(self, course):
        subjects = self.get_subject_ids(course.id)
        matrix_id = course.matrix_id.id
        scores_array_report = []

        longitude = len(subjects)
        if subjects:
            scores_array = [0 for u in range(longitude)]
            num_child = 0
            for subject in subjects:
                coefficient = util.format_sie(subject.coefficient, self.get_sie_digits_certificate())
                scores_array[num_child] = self.get_detail_achievement(matrix_id, course, subject.id,
                                                                      coefficient)
                num_child += 1

            scores_array_report = self.get_subject_score(num_child, scores_array, subjects)
        return scores_array_report, longitude

    def get_subject_score(self, num_child, scores_array_child, subjects):
        if num_child > 0:
            num_subjects = len(subjects)
            num_columns = 5
            num_students = 0
            for s in range(num_child):
                try:
                    num_students = len(scores_array_child[s])
                    break
                except:
                    num_students = 0
            num_records = (num_students - 1) * num_subjects + 1
            scores_array = [[0 for j in range(num_columns)] for i in range(num_records)]

            position_x = 0
            for w in range(num_child):
                data = scores_array_child[w]
                try:
                    longitude = len(data[0])
                except:
                    longitude = 0
                if longitude > 0:
                    for x in range(num_students):
                        if x == 0:
                            if w == 0:
                                scores_array[position_x + x][0] = data[x][3]
                                scores_array[position_x + x][1] = 'MATERIAS'
                                scores_array[position_x + x][2] = 'PROMEDIO'
                                scores_array[position_x + x][3] = 'COEFICIENTE'
                                scores_array[position_x + x][4] = 'NOTA FINAL'
                        else:
                            scores_array[position_x + x][0] = data[x][3]
                            scores_array[position_x + x][1] = subjects[w].name

                            prom = data[x][longitude - 2]
                            prom_text = '%s' % prom
                            scores_array[position_x + x][2] = prom_text.replace('.', ',')

                            coefficient = util.round_sie(subjects[w].coefficient, '7')
                            coefficient_text = util.format_sie(coefficient, self.get_sie_digits_certificate())
                            scores_array[position_x + x][3] = coefficient_text.replace('.', ',')

                            score = float(prom) * coefficient
                            score_text = util.format_sie(util.round_sie(score, self.get_sie_digits()),
                                                         self.get_sie_digits())
                            scores_array[position_x + x][4] = score_text.replace('.', ',')
                    position_x += num_students - 1

        else:
            scores_array = []
        return scores_array

    ######## Integrator Product ########

    def get_coe_integrator(self, parameter_id):
        parameter = self.get_parameter_by_id(parameter_id)
        coefficient = parameter.coefficient
        return coefficient

    def get_judge(self, game_id, judge_id):
        sie_faculty = http.request.env['sie.faculty']
        judge = sie_faculty.search([('id', '=', judge_id)])
        return judge.display_title_name

    def get_coe_integrator_thesis_child_ids(self, parameter_id):
        parameter = self.get_parameter_by_id(parameter_id)
        coefficient = parameter.coefficient
        parameter_child_ids = parameter.child_ids
        return coefficient, parameter_child_ids

    def get_integrator_thesis(self, parameter_id, course_id):
        integrator_product_sie = http.request.env['sie.integrator.product']
        integrator = integrator_product_sie.search([('course_id', '=', int(course_id)),
                                                    ('parameter_id', '=', parameter_id)])
        return integrator

    def get_war_game_name(self, war_games_id):
        war_games = http.request.env['sie.war.games']
        game = war_games.search([('id', '=', int(war_games_id))])
        return game.name

    def get_integrator_child_ids(self, war_games_id, parameter_id, matrix_id):
        parameter = self.get_parameter_by_id(parameter_id)
        coefficient = parameter.coefficient
        parameter_child_ids = parameter.child_ids

        return coefficient, parameter_child_ids

    def get_integrator_groups(self, games_id):
        war_games_enrollment = http.request.env['sie.war.games.enrollment']
        groups = war_games_enrollment.search([('war_games_id', '=', int(games_id))])
        return groups

    def get_integrator_students(self, course_id):
        integrator_enrollment = http.request.env['sie.enrollment']
        students = integrator_enrollment.search([('course_id', '=', int(course_id))])
        students = students.student_ids.sorted(key=attrgetter('last_name_1', 'last_name_2')). \
            filtered(lambda r: r.inactive == False)
        return students

    def get_integrator_games(self, course_id):
        war_games = http.request.env['sie.war.games']
        games = war_games.search([('course_id', '=', int(course_id))])
        return games

    def get_integrator_game(self, parameter_id, course_id, war_games_id, judge_id):
        integrator_sie = http.request.env['sie.integrator.product']
        integrator = integrator_sie.search([('course_id', '=', int(course_id)),
                                            ('war_games_id', '=', int(war_games_id)),
                                            ('parameter_id', '=', parameter_id),
                                            ('judge_id', '=', int(judge_id))])
        return integrator

    def get_detail_te(self, num_child, scores_array_child, coefficient, title):
        num_columns = 0
        if num_child == 1:
            data = scores_array_child[0]
            num_students = len(data)
            longitude = len(data[0])
            num_columns = longitude + 2
            scores_array = [[0 for j in range(num_columns)] for i in range(num_students)]
            scores_array_prom = [[0 for j in range(1)] for i in range(num_students)]

            for x in range(num_students):
                for y in range(longitude):
                    scores_array[x][y] = data[x][y]
                if x == 0:
                    scores_array_prom[x][0] = title
                else:
                    if data[x][y] == '--':
                        scores_array_prom[x][0] = data[x][y - 1]
                    else:
                        scores_array_prom[x][0] = decimal.Decimal(data[x][y - 1])
            for x in range(num_students):
                if x == 0:
                    scores_array[x][num_columns - 2] = scores_array_prom[x][0]
                    scores_array[x][num_columns - 1] = '*%s' % coefficient
                else:
                    if scores_array_prom[x][0] == '--':
                        scores_array[x][num_columns - 2] = '--'
                        scores_array[x][num_columns - 1] = '--'
                    else:
                        prom = util.round_sie(decimal.Decimal(scores_array_prom[x][0]), self.get_sie_digits())
                        score_coefficient = util.round_sie(decimal.Decimal(prom) * decimal.Decimal(coefficient),
                                                           self.get_sie_digits())
                        scores_array[x][num_columns - 2] = util.format_sie(prom)
                        scores_array[x][num_columns - 1] = util.format_sie(score_coefficient)

        elif num_child == 2:
            num_students = len(scores_array_child[0])
            for y in range(num_child):
                data = scores_array_child[y]
                num_columns += len(data[0])
            scores_array = [[0 for j in range(num_columns - 1)] for i in range(num_students)]
            scores_array_prom = [[0 for j in range(1)] for i in range(num_students)]
            data = scores_array_child[0]
            position = len(data[0]) - 1
            for w in range(num_child):
                data = scores_array_child[w]
                longitude = len(data[0])
                if w == 0:
                    for x in range(num_students):
                        for y in range(longitude):
                            scores_array[x][y] = data[x][y]
                        if x == 0:
                            scores_array_prom[x][0] = title
                        else:
                            scores_array_prom[x][0] = decimal.Decimal(data[x][y])
                else:
                    for x in range(num_students):
                        z = 1
                        for y in range(longitude):
                            if y > 2:
                                scores_array[x][position + z] = data[x][y]
                                z += 1
                        if x == 0:
                            scores_array_prom[x][0] = title
                        else:
                            scores_array_prom[x][0] += decimal.Decimal(data[x][y])
            for x in range(num_students):
                if x == 0:
                    scores_array[x][num_columns - 3] = scores_array_prom[x][0]
                    scores_array[x][num_columns - 2] = '*%s' % coefficient
                else:
                    if scores_array_prom[x][0] == '--':
                        scores_array[x][num_columns - 3] = '--'
                        scores_array[x][num_columns - 2] = '--'
                    else:
                        prom = util.round_sie(scores_array_prom[x][0], self.get_sie_digits())
                        score_coefficient = util.round_sie(decimal.Decimal(prom) * decimal.Decimal(coefficient),
                                                           self.get_sie_digits())
                        scores_array[x][num_columns - 3] = util.format_sie(prom, self.get_sie_digits())
                        scores_array[x][num_columns - 2] = util.format_sie(score_coefficient, self.get_sie_digits())
        else:
            scores_array = []
        return scores_array

    def get_detail_thesis(self, parameter_id, matrix_id, course_id, title):
        coefficient, parameter_child_ids = self.get_coe_integrator_thesis_child_ids(parameter_id)
        num_child = 0
        scores_array_child = [0 for u in range(len(parameter_child_ids))]
        x = 0
        for parameter in parameter_child_ids:
            data = self.get_integrator_thesis(parameter.id, course_id)
            if data:
                num_child += 1
                scores_array_child[x] = self.get_scores_array_by_score_number(data, parameter.coefficient, True,
                                                                              'sie.integrator.product.student', '', 'N')
            x += 1
        scores_array = self.get_detail(num_child, scores_array_child, coefficient, title)
        return scores_array

    def get_detail_war(self, war_games_id, judge_id, parameter_id, matrix_id, course_id):
        coefficient = self.get_coe_integrator(parameter_id)
        groups = self.get_integrator_groups(war_games_id)
        game_name = self.get_war_game_name(war_games_id)
        parameter_child_ids = self.get_parameter_childs(parameter_id, matrix_id)
        num_child = 0
        scores_array_child = [0 for u in range(len(parameter_child_ids))]
        scores_array_eo = []
        scores_array_sim = []
        x = 0
        for parameter in parameter_child_ids:
            course = self.get_course(course_id)
            if course.new_table:
                if parameter.param_name.code == '020':
                    parameter_eo = parameter
                    coefficient_eje = self.get_coe_integrator(parameter_eo.id)
                    data = self.get_integrator_game(parameter.id, course_id, war_games_id, judge_id)
                    if data:
                        scores_array_child_sim = self.get_scores_array_by_score_number(data, coefficient_eje, True,
                                                                                       'sie.integrator.product.student',
                                                                                       '',
                                                                                       'N', groups)
                        scores_array_sim = self.get_detail_one(1, scores_array_child_sim, coefficient_eje, 'EJE')
                elif parameter.param_name.code == '019':
                    coefficient_eo = parameter.coefficient
                    data = self.get_integrator_game(parameter.id, course_id, war_games_id, judge_id)
                    if data:
                        scores_array_child_eo = self.get_scores_array_by_score_number(data, parameter.coefficient, True,
                                                                                      'sie.integrator.product.student',
                                                                                      '', 'N', groups)
                        scores_array_eo = self.get_detail_one(1, scores_array_child_eo, coefficient_eo, 'E.O.')
                else:
                    data = self.get_integrator_game(parameter.id, course_id, war_games_id, judge_id)
                    if parameter.param_name.code == '018':
                        x = 1
                    else:
                        x = 0
                    if data:
                        num_child += 1
                        scores_array_child[x] = self.get_scores_array_by_score_number(data, parameter.coefficient, True,
                                                                                      'sie.integrator.product.student',
                                                                                      '', 'N', groups)
            else:
                if parameter.param_name.code == '037':
                    parameter_eo = self.get_parameter_by_param_name('020', matrix_id, '014')
                    coefficient_eje = self.get_coe_integrator(parameter_eo.id)
                    data = self.get_integrator_game(parameter.id, course_id, war_games_id, judge_id)
                    if data:
                        scores_array_child_sim = self.get_scores_array_by_score_number(data, coefficient_eje, True,
                                                                                       'sie.integrator.product.student',
                                                                                       '',
                                                                                       'N', groups)
                        scores_array_sim = self.get_detail_one(1, scores_array_child_sim, coefficient_eje, 'EJE')
                elif parameter.param_name.code == '019':
                    coefficient_eo = parameter.coefficient
                    data = self.get_integrator_game(parameter.id, course_id, war_games_id, judge_id)
                    if data:
                        scores_array_child_eo = self.get_scores_array_by_score_number(data, parameter.coefficient, True,
                                                                                      'sie.integrator.product.student',
                                                                                      '', 'N', groups)
                        scores_array_eo = self.get_detail_one(1, scores_array_child_eo, coefficient_eo, 'E.O.')
                else:
                    data = self.get_integrator_game(parameter.id, course_id, war_games_id, judge_id)
                    if parameter.param_name.code == '018':
                        x = 1
                    else:
                        x = 0
                    if data:
                        num_child += 1
                        scores_array_child[x] = self.get_scores_array_by_score_number(data, parameter.coefficient, True,
                                                                                      'sie.integrator.product.student',
                                                                                      '', 'N', groups)

        scores_array_teeo = [0 for u in range(2)]
        scores_array_planeje = [0 for u in range(2)]
        parameter_plante = self.get_parameter_by_param_name('016', matrix_id, '015')
        coefficient_plante = self.get_coe_integrator(parameter_plante.id)
        scores_array_teeo[0] = self.get_detail(num_child, scores_array_child, coefficient_plante, 'T.E.')
        scores_array_teeo[1] = scores_array_eo
        num_child = 0
        if scores_array_teeo[0]:
            num_child += 1
        if scores_array_teeo[1]:
            num_child += 1
        parameter_plan = self.get_parameter_by_param_name('015', matrix_id, '014')
        coefficient_plan = self.get_coe_integrator(parameter_plan.id)
        scores_array_planeje[0] = self.get_detail(num_child, scores_array_teeo, coefficient_plan, 'PLAN')
        scores_array_planeje[1] = scores_array_sim
        num_child = 0
        if scores_array_planeje[0]:
            num_child += 1
        if scores_array_planeje[1]:
            num_child += 1
        scores_array = self.get_detail(num_child, scores_array_planeje, coefficient, 'J.C.')

        return game_name, scores_array

    def get_score_game_judges(self, array_game_judges, num_students, index):
        scores_array_prom = []
        # num_judges = len(array_game_judges)
        if array_game_judges:
            scores_array_prom = [[0 for j in range(1)] for i in range(num_students)]
            num_judges = [[0 for j in range(1)] for i in range(num_students)]
            for data in array_game_judges:
                if data:
                    if num_students == len(data):  # TODO: add 16 de Septiembre 2016
                        longitude = len(data[0])
                        for x in range(num_students):
                            if x != 0:
                                if data[x][longitude - 2] != '--':
                                    scores_array_prom[x][0] += decimal.Decimal(data[x][longitude - 2])
                                    num_judges[x][0] += 1
            for x in range(num_students):
                if x == 0:
                    scores_array_prom[0][0] = 'J.%s' % index
                else:
                    cant = num_judges[x][0]
                    if cant == 0:
                        scores_array_prom[x][0] = decimal.Decimal(0.0)
                    else:
                        scores_array_prom[x][0] = util.round_sie(decimal.Decimal(scores_array_prom[x][0] /
                                                                                 cant), self.get_sie_digits())

        return scores_array_prom

    def get_detail_war_report(self, parameter_id, matrix_id, course_id):
        games = self.get_integrator_games(course_id)
        students = self.get_integrator_students(course_id)
        num_students = len(students) + 1
        z = 0
        array_games = [0 for u in range(len(games))]
        for game in games:
            judges = game.faculty_ids
            array_game_judges = [0 for u in range(len(judges))]
            x = 0
            for judge in judges:
                game_name, array_game_judges[x] = self.get_detail_war(game.id, judge.id, parameter_id, matrix_id,
                                                                      course_id)
                x += 1
            array_games[z] = self.get_score_game_judges(array_game_judges, num_students, z + 1)

            z += 1
        columns = len(array_games) + 6
        coefficient = self.get_coe_integrator(parameter_id)
        scores_array = [[0 for j in range(columns)] for i in range(num_students)]
        for x in range(num_students):
            for y in range(columns):
                if x == 0:
                    if y == 0:
                        scores_array[x][0] = 'No.'
                    elif y == 1:
                        scores_array[x][1] = 'Grado'
                    elif y == 2:
                        scores_array[x][2] = 'Nombre'
                    elif y == 3:
                        scores_array[x][3] = 'Id'
                    elif y == columns - 2:
                        scores_array[x][y] = 'J.G.'
                    elif y == columns - 1:
                        coefficient_text = '*%s' % coefficient
                        scores_array[x][y] = coefficient_text.replace('.', '.')
                    else:
                        value = array_games[y - 4][0]
                        scores_array[x][y] = u'%s' % value[0]
                if x != 0:
                    if y == 0:
                        scores_array[x][0] = '%s' % x
                    elif y == 1:
                        scores_array[x][1] = u'%s-%s' % (students[x - 1].grade_id.acronym,
                                                         students[x - 1].specialty_id.acronym)
                    elif y == 2:
                        scores_array[x][2] = u'%s' % students[x - 1].full_name
                    elif y == 3:
                        scores_array[x][3] = u'%s' % students[x - 1].id
                    elif y == columns - 2:
                        scores_array[x][y] = '--'
                    elif y == columns - 1:
                        scores_array[x][y] = '--'
                    else:
                        value = array_games[y - 4][x]
                        if value[0] == decimal.Decimal(0):
                            scores_array[x][y] = '--'
                        else:
                            scores_array[x][y] = util.format_sie(value[0], self.get_sie_digits())

        for x in range(num_students):
            sum_judge = 0
            z = 0
            for y in range(columns):
                if y > 3 and y < (columns - 1) and x != 0:
                    if scores_array[x][y] != '--':
                        sum_judge += decimal.Decimal(scores_array[x][y])
                        z += 1
            if x != 0 and z > 0:
                prom = util.round_sie(decimal.Decimal(sum_judge / z), self.get_sie_digits())
                prom_coefficient = util.round_sie(decimal.Decimal(prom) * decimal.Decimal(coefficient),
                                                  self.get_sie_digits())
                scores_array[x][columns - 2] = util.format_sie(prom, self.get_sie_digits())
                scores_array[x][columns - 1] = util.format_sie(prom_coefficient, self.get_sie_digits())
        return '', scores_array

    def get_summary_integrator_array_2column(self, course):
        data = self.get_summary_integrator_array(course)
        if data:
            scores_array = self.get_summary_array_2column(data)
        else:
            scores_array = []
        return scores_array

    def get_summary_integrator_array_1column(self, course):
        data = self.get_summary_integrator_array(course)
        scores_array = self.get_summary_array_1column(data)
        return scores_array

    ######## productivity ########

    def get_productivity_coe_child_ids(self, parameter_id):
        parameter = self.get_parameter_by_id(parameter_id)
        coefficient = parameter.coefficient
        parameter_child_ids = parameter.child_ids
        return coefficient, parameter_child_ids

    def get_productivity_parameter(self, param_code, matrix_id):
        parameter = self.get_parameter_by_param_name(param_code, matrix_id, '022')
        return parameter

    def get_productivity_coe(self, param_code, matrix_id):
        parameter = self.get_parameter_by_param_name(param_code, matrix_id, '022')
        coefficient = parameter.coefficient
        return coefficient

    def get_productivity_coe_by_parameter_id(self, parameter_id):
        parameter = self.get_parameter_by_id(parameter_id)
        coefficient = parameter.coefficient
        return coefficient

    def get_productivity(self, parameter_id, matrix_id, course_id):
        productivity_sie = http.request.env['sie.productivity']
        productive = productivity_sie.search([('course_id', '=', int(course_id)),
                                              ('parameter_id', '=', parameter_id)])
        return productive

    def get_productivity_work_child_ids(self, work_id, parameter_id, matrix_id):
        register_work = http.request.env['sie.register.work']
        work = register_work.search([('id', '=', int(work_id))])
        work_name = work.work_name

        parameter = self.get_parameter_by_id(parameter_id)
        coefficient = parameter.coefficient
        parameter_child_ids = parameter.child_ids

        return work_name, coefficient, parameter_child_ids

    def get_productivity_groups(self, work_id):
        register_work_enrollment = http.request.env['sie.register.work.enrollment']
        groups = register_work_enrollment.search([('register_work_id', '=', int(work_id))])
        return groups

    def get_seminaries(self, course_id):
        register_seminary = http.request.env['sie.register.seminary']
        seminaries = register_seminary.search([('course_id', '=', int(course_id))])
        return seminaries

    def get_productivity_work(self, work_id, parameter_id, matrix_id, course_id):
        productivity_sie = http.request.env['sie.productivity']
        productive = productivity_sie.search([('course_id', '=', int(course_id)),
                                              ('direction_work_id', '=', int(work_id)),
                                              ('parameter_id', '=', parameter_id)])
        return productive

    def get_detail_con_tdi(self, parameter_id, matrix_id, title):
        coefficient, parameter_child_ids = self.get_productivity_coe_child_ids(parameter_id)
        num_child = 0
        scores_array_child = [0 for u in range(len(parameter_child_ids))]
        x = 0
        for parameter in parameter_child_ids:
            data = self.get_productivity(parameter.id, matrix_id, self.course_id)
            if data:
                num_child += 1
                scores_array_child[x] = self.get_scores_array_by_score_number(data, parameter.coefficient, True,
                                                                              'sie.productivity.student',
                                                                              'productivity', 'N')
            x += 1
        scores_array = self.get_detail(num_child, scores_array_child, coefficient, title)
        return scores_array

    def get_detail_tdd(self, direction_work_id, parameter_id, matrix_id):
        groups = self.get_productivity_groups(direction_work_id)
        work_name, coefficient, parameter_child_ids = self.get_productivity_work_child_ids(direction_work_id,
                                                                                           parameter_id,
                                                                                           matrix_id)
        num_child = 0
        scores_array_child = [0 for u in range(len(parameter_child_ids))]
        x = 0
        for parameter in parameter_child_ids:
            data = self.get_productivity_work(direction_work_id, parameter.id, matrix_id, self.course_id)
            if data:
                num_child += 1
                scores_array_child[x] = self.get_scores_array_by_score_number(data, parameter.coefficient, True,
                                                                              'sie.productivity.student',
                                                                              'productivity', 'N', groups)
                x += 1
        scores_array = self.get_detail(num_child, scores_array_child, coefficient, 'TDD')
        return work_name, self.get_sort_array(scores_array)

    def get_detail_conference_summary(self, matrix_id):
        if self.get_course(self.course_id).new_table:
            parent_code = '013'
            param_code = '023'
        else:
            parent_code = '022'
            param_code = '023'
        parameter = self.get_parameter_by_param_name(param_code, matrix_id, parent_code)
        scores_array_con = self.get_detail_con_tdi(parameter.id, matrix_id, parameter.param_name.short_name)
        columns_con = 0
        if parameter:
            flag_con = "P"
        else:
            flag_con = "E"
        if scores_array_con:
            columns_con += 2
            flag_con = "OK"
            num_students = len(scores_array_con)
            columns_pro = 2
            scores_array_users = [[0 for j in range(4)] for i in range(num_students)]
            scores_array_con_prom = [[0 for j in range(columns_pro)] for i in range(num_students)]
            w = 0
            for x in range(num_students):
                z = zz = 0
                longitude = len(scores_array_con[x])
                for y in range(longitude):
                    if y < 4:
                        scores_array_users[w][zz] = scores_array_con[x][y]
                        zz += 1
                    elif y == longitude - 2:
                        scores_array_con_prom[w][z] = scores_array_con[x][y]
                        z += 1
                    elif y == longitude - 1:
                        scores_array_con_prom[w][z] = scores_array_con[x][y]
                        z += 1
                w += 1
        else:
            scores_array_con_prom = []
            scores_array_users = []
        return flag_con, columns_con, scores_array_con_prom, scores_array_users

    def get_detail_tdd_summary(self, matrix_id):
        columns_dir = 0
        if self.get_course(self.course_id).new_table:
            parameter = self.get_parameter_by_param_name('024', matrix_id, '013')
        else:
            parameter = self.get_productivity_parameter('024', matrix_id)
        if parameter:
            flag_dir = "P"
        else:
            flag_dir = "E"
        register_work = http.request.env['sie.register.work']
        direction_work_ids = register_work.search([('course_id', '=', int(self.course_id)), ('work_type', '=',
                                                                                             'direction')])
        scores_array_childs = [0 for u in range(len(direction_work_ids))]
        if scores_array_childs:
            x = 0
            for direction_work_id in direction_work_ids:
                work_name, scores_array = self.get_detail_tdd(direction_work_id, parameter.id, matrix_id)
                if scores_array:
                    scores_array_childs[x] = scores_array
                    x += 1
            if x > 0:
                longitude = len(scores_array_childs)
                for i in range(x):
                    try:
                        num_students = len(scores_array_childs[i])
                        break
                    except:
                        num_students = 0
                if num_students > 1:
                    scores_array_childs_dir = [[0 for j in range(longitude)] for i in range(num_students)]
                    for i in range(len(scores_array_childs_dir)):
                        for j in range(len(scores_array_childs_dir[i])):
                            scores_array_childs_dir[i][j] = '--'
                    columns_dir += 2
                    flag_dir = "OK"
                    columns_pro = 2
                    scores_array_users = [[0 for j in range(4)] for i in range(num_students)]
                    scores_array_child_dir_prom = [[0 for j in range(columns_pro)] for i in range(num_students)]
                    z = 0
                    for scores_array_child in scores_array_childs:
                        if scores_array_child:
                            for x in range(len(scores_array_child)):  # TODO 15 Septiembre 2016
                                zz = 0
                                longitude = len(scores_array_child[x])
                                for y in range(longitude):
                                    if y < 4:
                                        scores_array_users[x][zz] = scores_array_child[x][y]
                                        zz += 1
                                    elif y == longitude - 2:
                                        if x == 0:
                                            scores_array_childs_dir[x][z] = scores_array_child[x][y]
                                        else:
                                            scores_array_childs_dir[x][z] = scores_array_child[x][y]
                            z += 1

                    coefficient_tdd = self.get_productivity_coe_by_parameter_id(parameter.id)
                    for x in range(num_students):
                        longitude = len(scores_array_childs_dir[0])
                        num_scores = 0
                        for y in range(longitude):
                            if x == 0:
                                if scores_array_childs_dir[x][y] != '--':
                                    scores_array_child_dir_prom[x][0] = scores_array_childs_dir[x][y]
                            else:
                                if scores_array_childs_dir[x][y] == '--':
                                    scores_array_child_dir_prom[x][0] += 0
                                else:
                                    scores_array_child_dir_prom[x][0] += decimal.Decimal(
                                        str(scores_array_childs_dir[x][y]))
                                    num_scores += 1
                        if x == 0:
                            scores_array_child_dir_prom[x][1] = '*%s' % coefficient_tdd
                        else:
                            prom = util.round_sie(decimal.Decimal(scores_array_child_dir_prom[x][0] / num_scores),
                                                  self.get_sie_digits())
                            score_coefficient = util.round_sie(decimal.Decimal(prom) * decimal.Decimal(coefficient_tdd),
                                                               self.get_sie_digits())
                            scores_array_child_dir_prom[x][0] = util.format_sie(prom, self.get_sie_digits())
                            scores_array_child_dir_prom[x][1] = util.format_sie(score_coefficient,
                                                                                self.get_sie_digits())

                    scores_array_dir_prom = [[0 for j in range(columns_pro)] for i in range(num_students)]
                    for x in range(num_students):
                        longitude = len(scores_array_child_dir_prom[x])
                        for y in range(longitude):
                            if x == 0:
                                scores_array_dir_prom[x][y] = scores_array_child_dir_prom[x][y]
                            else:
                                scores_array_dir_prom[x][y] = scores_array_child_dir_prom[x][y]
                else:
                    scores_array_dir_prom = []
                    scores_array_users = []
            else:
                scores_array_dir_prom = []
                scores_array_users = []
        else:
            scores_array_dir_prom = []
            scores_array_users = []

        return flag_dir, columns_dir, scores_array_dir_prom, scores_array_users

    def get_detail_tdi_summary(self, matrix_id):
        columns_inv = 0
        if self.get_course(self.course_id).new_table:
            parameter = self.get_parameter_by_param_name('032', matrix_id, '013')
        else:
            parameter = self.get_productivity_parameter('032', matrix_id)
        scores_array_childs = [0 for u in range(1)]
        x = 0
        num_child = 0

        if parameter:
            flag_inv = "P"
        else:
            flag_inv = "E"
        scores_array_tdi = self.get_detail_con_tdi(parameter.id, matrix_id, 'TDI')
        if scores_array_tdi:
            scores_array_childs[x] = scores_array_tdi
            x += 1
            num_child += 1

        if num_child > 0:
            columns_inv += 2
            flag_inv = "OK"
            num_students = len(scores_array_childs[0])
            columns_pro = 2
            scores_array_users = [[0 for j in range(4)] for i in range(num_students)]
            scores_array_child_inv_prom = [[0 for j in range(columns_pro)] for i in range(num_students)]
            num_scores = 0
            for scores_array_child in scores_array_childs:
                if scores_array_child:
                    num_scores += 1
                    w = 0
                    for x in range(num_students):
                        z = zz = 0
                        longitude = len(scores_array_child[x])
                        for y in range(longitude):
                            if y < 4:
                                scores_array_users[w][zz] = scores_array_child[x][y]
                                zz += 1
                            elif y == longitude - 2:
                                if x == 0:
                                    scores_array_child_inv_prom[w][z] = scores_array_child[x][y]
                                else:
                                    scores_array_child_inv_prom[w][z] += decimal.Decimal(scores_array_child[x][y])
                                z += 1
                            elif y == longitude - 1:
                                if x == 0:
                                    scores_array_child_inv_prom[w][z] = scores_array_child[x][y]
                                else:
                                    scores_array_child_inv_prom[w][z] += decimal.Decimal(scores_array_child[x][y])
                                z += 1
                        w += 1
            scores_array_inv_prom = [[0 for j in range(columns_pro)] for i in range(num_students)]
            w = 0
            for x in range(num_students):
                z = zz = 0
                longitude = len(scores_array_child_inv_prom[x])
                for y in range(longitude):
                    if x == 0:
                        if y == longitude - 2:
                            scores_array_inv_prom[w][z] = scores_array_child_inv_prom[w][z]
                            z += 1
                        elif y == longitude - 1:
                            scores_array_inv_prom[w][z] = scores_array_child_inv_prom[x][y]
                            z += 1
                    else:
                        if y == longitude - 2:
                            prom = util.round_sie(decimal.Decimal(str(scores_array_child_inv_prom[w][z] / num_scores)),
                                                  self.get_sie_digits())
                            scores_array_inv_prom[w][z] = util.format_sie(prom, self.get_sie_digits())
                            z += 1
                        elif y == longitude - 1:
                            prom = util.round_sie(decimal.Decimal(str(scores_array_child_inv_prom[w][z] / num_scores)),
                                                  self.get_sie_digits())
                            scores_array_inv_prom[w][z] = util.format_sie(prom, self.get_sie_digits())
                            z += 1
                w += 1
        else:
            scores_array_inv_prom = []
            scores_array_users = []
        return flag_inv, columns_inv, scores_array_inv_prom, scores_array_users

    def get_summary_productivity_array(self, course):
        matrix_id = course.matrix_id.id
        parameter = self.get_parameter_by_param_name('022', matrix_id)
        coefficient_pro = parameter.coefficient

        scores_array = []
        columns = 4

        # Conference
        flag_con, columns_con, scores_array_con_prom, scores_array_users_con = self.get_detail_conference_summary(
            matrix_id)

        # Work Direction
        flag_dir, columns_dir, scores_array_dir_prom, scores_array_users_dir = self.get_detail_tdd_summary(matrix_id)

        # Search
        flag_inv, columns_inv, scores_array_inv_prom, scores_array_users_inv = self.get_detail_tdi_summary(matrix_id)

        len_users = 0
        len_users_con = 0
        len_users_dir = 0
        len_users_inv = 0
        scores_array_users = []
        if flag_con == "OK":
            scores_array_users = scores_array_users_con
            len_users_con = len(scores_array_users)
            len_users = len_users_con
        else:
            if flag_con == "P":
                columns_con = 2
                scores_array_users_con = self.get_students_course(course)
                scores_array_users = scores_array_users_con
                len_users_con = len(scores_array_users)
                len_users = len_users_con
            else:
                columns_con = 0

        if flag_dir == "OK":
            len_users_dir = len(scores_array_users_dir)
            if len_users_dir > len_users:
                scores_array_users = scores_array_users_dir
                len_users = len(scores_array_users)
        else:
            if flag_dir == "P":
                columns_dir = 2
                scores_array_users_dir = self.get_students_course(course)
                scores_array_users = scores_array_users_dir
                len_users_dir = len(scores_array_users)
                len_users = len_users_dir
            else:
                columns_dir = 0

        if flag_inv == "OK":
            len_users_inv = len(scores_array_users_inv)
            if len_users_inv > len_users:
                scores_array_users = scores_array_users_inv
        else:
            if flag_inv == "P":
                columns_inv = 2
                scores_array_users_inv = self.get_students_course(course)
                scores_array_users = scores_array_users_inv
                len_users_inv = len(scores_array_users)
                len_users = len_users_inv
            else:
                columns_inv = 0

        columns += columns_inv + columns_con + columns_dir

        if columns > 5:
            columns += 2

            num_students = len(scores_array_users)
            scores_array = [[0 for j in range(columns)] for i in range(num_students)]
            w = 0
            for x in range(num_students):
                z = 0
                for y in range(columns):
                    if y < 4:
                        scores_array[w][z] = scores_array_users[x][y]
                    else:
                        scores_array[w][z] = '--'
                    z += 1
                w += 1

            position_array = 4

            if flag_con == "OK":
                w = 0
                longitude = 0
                for x in range(len_users_con):
                    z = position_array
                    longitude = len(scores_array_con_prom[x])
                    for y in range(longitude):
                        if w == 0:
                            scores_array[w][z] = scores_array_con_prom[x][y]
                        else:
                            value = scores_array_users_con[x][3]
                            for g in range(len(scores_array)):
                                try:
                                    scores_array[g].index(value)
                                    index = g
                                    break
                                except ValueError:
                                    index = x
                            scores_array[index][z] = scores_array_con_prom[x][y]
                        z += 1
                    w += 1
                position_array += longitude
            else:
                w = 0
                longitude = 0
                for x in range(len_users_con):
                    z = position_array
                    longitude = 2
                    for y in range(longitude):
                        if w == 0:
                            if z == position_array:
                                scores_array[w][z] = self.get_productivity_parameter('023', matrix_id).param_name. \
                                    short_name
                            else:
                                scores_array[w][z] = ('*%s' % self.get_productivity_coe('023', matrix_id)). \
                                    replace('.', ',')
                        else:
                            value = scores_array_users_con[x][3]
                            for g in range(len(scores_array)):
                                try:
                                    scores_array[g].index(value)
                                    index = g
                                    break
                                except ValueError:
                                    index = x
                            scores_array[index][z] = '--'
                        z += 1
                    w += 1
                position_array += longitude

            if flag_dir == "OK":
                w = 0
                longitude = 0
                for x in range(len_users_dir):
                    z = position_array
                    longitude = len(scores_array_dir_prom[x])
                    for y in range(longitude):
                        if w == 0:
                            scores_array[w][z] = scores_array_dir_prom[x][y]
                        else:
                            value = scores_array_users_dir[x][3]
                            for g in range(len(scores_array)):
                                try:
                                    scores_array[g].index(value)
                                    index = g
                                    break
                                except ValueError:
                                    index = x
                            scores_array[index][z] = scores_array_dir_prom[x][y]
                        z += 1
                    w += 1
                position_array += longitude
            else:
                w = 0
                longitude = 0
                for x in range(len_users_dir):
                    z = position_array
                    longitude = 2
                    for y in range(longitude):
                        if w == 0:
                            if z == position_array:
                                scores_array[w][z] = self.get_productivity_parameter('024', matrix_id).param_name. \
                                    short_name
                            else:
                                scores_array[w][z] = ('*%s' % self.get_productivity_coe('024', matrix_id)). \
                                    replace('.', ',')
                        else:
                            value = scores_array_users_dir[x][3]
                            for g in range(len(scores_array)):
                                try:
                                    scores_array[g].index(value)
                                    index = g
                                    break
                                except ValueError:
                                    index = x
                            scores_array[index][z] = '--'
                        z += 1
                    w += 1
                position_array += longitude

            if flag_inv == "OK":
                w = 0
                longitude = 0
                for x in range(len_users_inv):
                    z = position_array
                    longitude = len(scores_array_inv_prom[x])
                    for y in range(longitude):
                        if w == 0:
                            scores_array[w][z] = scores_array_inv_prom[x][y]
                        else:
                            value = scores_array_users_inv[x][3]
                            for g in range(len(scores_array)):
                                try:
                                    scores_array[g].index(value)
                                    index = g
                                    break
                                except ValueError:
                                    index = x

                            scores_array[index][z] = scores_array_inv_prom[x][y]
                        z += 1
                    w += 1
                position_array += longitude
            else:
                w = 0
                longitude = 0
                for x in range(len_users_inv):
                    z = position_array
                    longitude = 2
                    for y in range(longitude):
                        if w == 0:
                            if z == position_array:
                                scores_array[w][z] = self.get_productivity_parameter('032', matrix_id).param_name. \
                                    short_name
                            else:
                                scores_array[w][z] = ('*%s' % self.get_productivity_coe('032', matrix_id)). \
                                    replace('.', ',')
                        else:
                            value = scores_array_users_inv[x][3]
                            for g in range(len(scores_array)):
                                try:
                                    scores_array[g].index(value)
                                    index = g
                                    break
                                except ValueError:
                                    index = x

                            scores_array[index][z] = '--'
                        z += 1
                    w += 1
                position_array += longitude

            w = 0
            for x in range(num_students):
                if w == 0:
                    scores_array[w][columns - 2] = 'PROD.'
                    coefficient_text = '*%s' % coefficient_pro
                    scores_array[w][columns - 1] = coefficient_text.replace('.', ',')
                else:
                    if columns == 8:
                        if (scores_array[w][columns - 3] == '--'):
                            scores_array[w][columns - 2] = '--'
                            scores_array[w][columns - 1] = '--'
                        else:
                            prom = util.round_sie(decimal.Decimal(scores_array[w][columns - 3]), self.get_sie_digits())
                            score_coefficient = util.round_sie(decimal.Decimal(prom) *
                                                               decimal.Decimal(coefficient_pro), self.get_sie_digits())
                            scores_array[w][columns - 2] = util.format_sie(prom, self.get_sie_digits())
                            scores_array[w][columns - 1] = util.format_sie(score_coefficient, self.get_sie_digits())
                    if columns == 10:
                        if (scores_array[w][columns - 3] == '--' and scores_array[w][columns - 5] == '--'):
                            scores_array[w][columns - 2] = '--'
                            scores_array[w][columns - 1] = '--'
                        elif (scores_array[w][columns - 3] == '--' and scores_array[w][columns - 5] != '--'):
                            prom = util.round_sie(decimal.Decimal(scores_array[w][columns - 6]), self.get_sie_digits())
                            score_coefficient = util.round_sie(decimal.Decimal(prom) *
                                                               decimal.Decimal(coefficient_pro), self.get_sie_digits())
                            scores_array[w][columns - 2] = util.format_sie(prom, self.get_sie_digits())
                            scores_array[w][columns - 1] = util.format_sie(score_coefficient, self.get_sie_digits())
                        elif (scores_array[w][columns - 3] != '--' and scores_array[w][columns - 5] == '--'):
                            prom = util.round_sie(decimal.Decimal(scores_array[w][columns - 4]), self.get_sie_digits())
                            score_coefficient = util.round_sie(decimal.Decimal(prom) *
                                                               decimal.Decimal(coefficient_pro), self.get_sie_digits())
                            scores_array[w][columns - 2] = util.format_sie(prom, self.get_sie_digits())
                            scores_array[w][columns - 1] = util.format_sie(score_coefficient, self.get_sie_digits())
                        else:
                            prom = util.round_sie(decimal.Decimal(scores_array[w][columns - 3]) + \
                                                  decimal.Decimal(scores_array[w][columns - 5]), self.get_sie_digits())
                            score_coefficient = util.round_sie(decimal.Decimal(prom) *
                                                               decimal.Decimal(coefficient_pro), self.get_sie_digits())
                            scores_array[w][columns - 2] = util.format_sie(prom, self.get_sie_digits())
                            scores_array[w][columns - 1] = util.format_sie(score_coefficient, self.get_sie_digits())
                    if columns == 12:
                        if (scores_array[w][columns - 3] == '--' and scores_array[w][columns - 5] == '--' and
                                    scores_array[w][columns - 7] == '--'):
                            scores_array[w][columns - 2] = '--'
                            scores_array[w][columns - 1] = '--'
                        elif (scores_array[w][columns - 3] != '--' and scores_array[w][columns - 5] == '--' and
                                      scores_array[w][columns - 7] == '--'):
                            prom = util.round_sie((decimal.Decimal(scores_array[w][columns - 6]) + \
                                                   decimal.Decimal(scores_array[w][columns - 8]) / 2),
                                                  self.get_sie_digits())
                            score_coefficient = util.round_sie(decimal.Decimal(prom) *
                                                               decimal.Decimal(coefficient_pro), self.get_sie_digits())
                            scores_array[w][columns - 2] = util.format_sie(prom, self.get_sie_digits())
                            scores_array[w][columns - 1] = util.format_sie(score_coefficient, self.get_sie_digits())
                        elif (scores_array[w][columns - 3] == '--' and scores_array[w][columns - 5] != '--' and
                                      scores_array[w][columns - 7] == '--'):
                            prom = util.round_sie((decimal.Decimal(scores_array[w][columns - 4]) + \
                                                   decimal.Decimal(scores_array[w][columns - 8]) / 2),
                                                  self.get_sie_digits())
                            score_coefficient = util.round_sie(decimal.Decimal(prom) *
                                                               decimal.Decimal(coefficient_pro), self.get_sie_digits())
                            scores_array[w][columns - 2] = util.format_sie(prom, self.get_sie_digits())
                            scores_array[w][columns - 1] = util.format_sie(score_coefficient, self.get_sie_digits())
                        elif (scores_array[w][columns - 3] == '--' and scores_array[w][columns - 5] == '--' and
                                      scores_array[w][columns - 7] != '--'):
                            prom = util.round_sie((decimal.Decimal(scores_array[w][columns - 4]) + \
                                                   decimal.Decimal(scores_array[w][columns - 6]) / 2),
                                                  self.get_sie_digits())
                            score_coefficient = util.round_sie(decimal.Decimal(prom) *
                                                               decimal.Decimal(coefficient_pro), self.get_sie_digits())
                            scores_array[w][columns - 2] = util.format_sie(prom, self.get_sie_digits())
                            scores_array[w][columns - 1] = util.format_sie(score_coefficient, self.get_sie_digits())
                        else:
                            prom = util.round_sie(decimal.Decimal(scores_array[w][columns - 3]) + \
                                                  decimal.Decimal(scores_array[w][columns - 5]) + \
                                                  decimal.Decimal(scores_array[w][columns - 7]), self.get_sie_digits())
                            score_coefficient = util.round_sie(decimal.Decimal(prom) *
                                                               decimal.Decimal(coefficient_pro), self.get_sie_digits())
                            scores_array[w][columns - 2] = util.format_sie(prom, self.get_sie_digits())
                            scores_array[w][columns - 1] = util.format_sie(score_coefficient, self.get_sie_digits())

                w += 1
        return scores_array

    def get_summary_productivity_array_1column(self, course):
        data = self.get_summary_productivity_array(course)
        if data:
            scores_array = self.get_summary_array_1column(data)
        else:
            scores_array = []
        return scores_array

    # Professional Attitude

    def get_professional_attitudes(self, course_id, parameter_id, evaluator_id=None, subject_id=None):
        professional_attitudes = http.request.env['sie.professional.attitude']
        if evaluator_id:
            if subject_id:
                attitudes = professional_attitudes.search([('course_id', '=', int(course_id)),
                                                           ('parameter_id', '=', int(parameter_id)),
                                                           ('faculty_id', '=', int(evaluator_id)),
                                                           ('subject_id', '=', int(self.subject_id)),
                                                           ('state', '=', 'published')]). \
                    sorted(key=lambda x: x.score_number)
            else:
                attitudes = professional_attitudes.search([('course_id', '=', int(course_id)),
                                                           ('parameter_id', '=', int(parameter_id)),
                                                           ('faculty_id', '=', int(evaluator_id)),
                                                           ('state', '=', 'published')]). \
                    sorted(key=lambda x: x.score_number)
        else:
            attitudes = professional_attitudes.search([('course_id', '=', int(course_id)),
                                                       ('parameter_id', '=', int(parameter_id)),
                                                       ('state', '=', 'published')]). \
                sorted(key=lambda x: x.score_number)
        return attitudes

    def get_attitudes_by_official(self, course_id, parameter_id, faculty_id):
        professional_attitudes = http.request.env['sie.professional.attitude']
        attitudes = professional_attitudes.search([('course_id', '=', int(course_id)),
                                                   ('parameter_id', '=', int(parameter_id)),
                                                   ('faculty_id', '=', faculty_id),
                                                   ('state', '=', 'published')]) \
            .sorted(key=lambda x: x.score_number)
        return attitudes

    def get_coe_attitudes(self, param_name_code, matrix_id, course_id, parent_ref_code):
        parameter = self.get_parameter_by_param_name(param_name_code, matrix_id, parent_ref_code)
        coefficient = parameter.coefficient
        professional_attitudes = http.request.env['sie.professional.attitude']
        attitudes = professional_attitudes.search([('course_id', '=', int(course_id)),
                                                   ('parameter_id', '=', parameter.id),
                                                   ('state', '=', 'published')]). \
            sorted(key=lambda x: x.score_number)
        return coefficient, parameter.id, attitudes

    def get_coe_professional_attitude(self, param_name_code, matrix_id, parent_ref_code):
        parameter = self.get_parameter_by_param_name(param_name_code, matrix_id, parent_ref_code)
        coefficient = parameter.coefficient
        return coefficient

    def get_students_professional_attitude(self, attitude):
        students = http.request.env['sie.professional.attitude.student'] \
            .search([('score_id', '=', attitude.id)]). \
            sorted(key=attrgetter('last_name_1', 'last_name_2')).filtered(lambda r: r.student_id.inactive == False)
        return students

    def get_summary_professional_attitudes_array(self, course):
        matrix_id = course.matrix_id.id
        parameter = self.get_parameter_by_param_name('025', matrix_id, None)
        column_name = parameter.param_name.short_name
        coefficient_ap = parameter.coefficient
        scores_array_users = []
        columns = 4
        columns_pro = columns_div = columns_pla = columns_dir = columns_coe = 0
        flag_pro = flag_div = flag_pla = flag_dir = flag_coe = ''
        number_ratings = 5
        # Profesores
        coefficient, parameter_id, attitudes = self.get_coe_attitudes('029', matrix_id, self.course_id, '025')
        if attitudes:
            scores_data = self.get_scores_array_pro_summary(attitudes, coefficient)
            flag_pro, columns_pro, scores_array_pro, scores_array_users = self.get_result_all(scores_data, 'P')
        else:
            flag_pro = 'E'
            columns_pro = 2
            number_ratings -= 1
        # Oficiales de division
        coefficient, parameter_id, attitudes = self.get_coe_attitudes('027', matrix_id, self.course_id, '025')
        if attitudes:
            scores_data = self.get_scores_array_pla_summary(attitudes, coefficient, parameter_id)
            flag_div, columns_div, scores_array_div, scores_array_users = self.get_result(scores_data, 'D')
        else:
            flag_div = 'E'
            columns_div = 2
            number_ratings -= 1
        # Oficiales de planta
        coefficient, parameter_id, attitudes = self.get_coe_attitudes('028', matrix_id, self.course_id, '025')
        if attitudes:
            scores_data = self.get_scores_array_pla_summary(attitudes, coefficient, parameter_id)
            flag_pla, columns_pla, scores_array_pla, scores_array_users = self.get_result_all(scores_data, 'P')
        else:
            flag_pla = 'E'
            columns_pla = 2
            number_ratings -= 1
        # Director
        coefficient, parameter_id, attitudes = self.get_coe_attitudes('026', matrix_id, self.course_id, '025')
        if attitudes:
            scores_data = self.get_scores_array_pla_summary(attitudes, coefficient, parameter_id)
            flag_dir, columns_dir, scores_array_dir, scores_array_users = self.get_result(scores_data, 'D')
        else:
            flag_dir = 'E'
            columns_dir = 2
            number_ratings -= 1
        # Coevaluacion
        coefficient, parameter_id, attitudes = self.get_coe_attitudes('030', matrix_id, self.course_id, '025')
        if attitudes:
            scores_data = self.get_scores_array_coe(attitudes, coefficient)
            flag_coe, columns_coe, scores_array_coe, scores_array_users = self.get_result(scores_data, 'C')
        else:
            flag_coe = 'E'
            columns_coe = 2
            number_ratings -= 1

        columns += columns_pro + columns_div + columns_pla + columns_dir + columns_coe + 2

        if columns > 6:
            num_students = len(scores_array_users)
            scores_array = [[0 for j in range(columns)] for i in range(num_students)]
            scores_array_prom = [[0 for j in range(1)] for i in range(num_students)]
            scores_array_prom_alt = [[0 for j in range(1)] for i in range(num_students)]
            w = 0
            for x in range(num_students):
                z = 0
                for y in range(4):
                    scores_array[w][z] = scores_array_users[x][y]
                    z += 1
                w += 1

            position_array = 4

            if flag_pro == 'P':
                longitude = 0
                w = 0
                for x in range(num_students):
                    z = position_array
                    longitude = len(scores_array_pro[x])
                    for y in range(longitude):
                        scores_array[w][z] = scores_array_pro[x][y]
                        z += 1
                    if w == 0:
                        scores_array_prom[w][0] = '--'
                        scores_array_prom_alt[w][0] = '--'
                    else:
                        if scores_array_prom[w][0] == '--':
                            scores_array[w][columns - 1] = '--'
                        else:
                            prom = util.round_sie(decimal.Decimal(scores_array_prom[w][0]) +
                                                  decimal.Decimal(scores_array_pro[x][y]), self.get_sie_digits())
                            scores_array_prom[w][0] = util.format_sie(prom, self.get_sie_digits())
                        if scores_array_prom_alt[w][0] != '--':
                            prom = util.round_sie(decimal.Decimal(scores_array_prom_alt[w][0]) +
                                                  decimal.Decimal(scores_array_pro[x][y - 1]), self.get_sie_digits())
                            scores_array_prom_alt[w][0] = util.format_sie(prom, self.get_sie_digits())
                    w += 1
                position_array += longitude
            else:
                longitude = 0
                w = 0
                for x in range(num_students):
                    z = position_array
                    longitude = 2
                    for y in range(longitude):
                        if w == 0:
                            if z == position_array:
                                scores_array[w][z] = 'PROF'
                            else:
                                value = '*%s' % self.get_coe_professional_attitude('029', matrix_id, '025')
                                scores_array[w][z] = value.replace('.', ',')
                        else:
                            scores_array[w][z] = '--'
                        z += 1
                    # scores_array_prom[w][0] = '--'
                    w += 1
                position_array += longitude

            if flag_div == 'D':
                longitude = 0
                w = 0
                for x in range(num_students):
                    z = position_array
                    longitude = len(scores_array_div[x])
                    for y in range(longitude):
                        scores_array[w][z] = scores_array_div[x][y]
                        z += 1
                    if w == 0:
                        scores_array_prom[w][0] = '---'
                        scores_array_prom_alt[w][0] = '---'
                    else:
                        if scores_array_prom[w][0] == '--':
                            scores_array[w][columns - 1] = '--'
                        else:
                            prom = util.round_sie(decimal.Decimal(scores_array_prom[w][0]) +
                                                  decimal.Decimal(scores_array_div[x][y]), self.get_sie_digits())
                            scores_array_prom[w][0] = util.format_sie(prom, self.get_sie_digits())
                        if scores_array_prom_alt[w][0] != '--':
                            prom = util.round_sie(decimal.Decimal(scores_array_prom_alt[w][0]) +
                                                  decimal.Decimal(scores_array_div[x][y - 1]), self.get_sie_digits())
                            scores_array_prom_alt[w][0] = util.format_sie(prom, self.get_sie_digits())
                    w += 1
                position_array += longitude
            else:
                longitude = 0
                w = 0
                for x in range(num_students):
                    z = position_array
                    longitude = 2
                    for y in range(longitude):
                        if w == 0:
                            if z == position_array:
                                scores_array[w][z] = 'O.D.'
                            else:
                                value = '*%s' % self.get_coe_professional_attitude('027', matrix_id, '025')
                                scores_array[w][z] = value.replace('.', ',')
                        else:
                            scores_array[w][z] = '--'
                        z += 1
                    # scores_array_prom[w][0] = '--'
                    w += 1
                position_array += longitude

            if flag_pla == 'P':
                longitude = 0
                w = 0
                for x in range(num_students):
                    z = position_array
                    longitude = len(scores_array_pla[x])
                    for y in range(longitude):
                        scores_array[w][z] = scores_array_pla[x][y]
                        z += 1
                    if w == 0:
                        scores_array_prom[w][0] = '---'
                        scores_array_prom_alt[w][0] = '---'
                    else:
                        if scores_array_prom[w][0] == '--':
                            scores_array[w][columns - 1] = '--'
                        else:
                            prom = util.round_sie(decimal.Decimal(scores_array_prom[w][0]) +
                                                  decimal.Decimal(scores_array_pla[x][y]), self.get_sie_digits())
                            scores_array_prom[w][0] = util.format_sie(prom, self.get_sie_digits())
                        if scores_array_prom_alt[w][0] != '--':
                            prom = util.round_sie(decimal.Decimal(scores_array_prom_alt[w][0]) +
                                                  decimal.Decimal(scores_array_pla[x][y - 1]), self.get_sie_digits())
                            scores_array_prom_alt[w][0] = util.format_sie(prom, self.get_sie_digits())
                    w += 1
                position_array += longitude
            else:
                longitude = 0
                w = 0
                for x in range(num_students):
                    z = position_array
                    longitude = 2
                    for y in range(longitude):
                        if w == 0:
                            if z == position_array:
                                scores_array[w][z] = 'O.P.'
                            else:
                                value = '*%s' % self.get_coe_professional_attitude('028', matrix_id, '025')
                                scores_array[w][z] = value.replace('.', ',')
                        else:
                            scores_array[w][z] = '--'
                        z += 1
                    # scores_array_prom[w][0] = '--'
                    w += 1
                position_array += longitude

            if flag_dir == 'D':
                longitude = 0
                w = 0
                for x in range(num_students):
                    z = position_array
                    longitude = len(scores_array_dir[x])
                    for y in range(longitude):
                        scores_array[w][z] = scores_array_dir[x][y]
                        z += 1
                    if w == 0:
                        scores_array_prom[w][0] = '---'
                        scores_array_prom_alt[w][0] = '---'
                    else:
                        if scores_array_prom[w][0] == '--':
                            scores_array[w][columns - 1] = '--'
                        else:
                            prom = util.round_sie(decimal.Decimal(scores_array_prom[w][0]) +
                                                  decimal.Decimal(scores_array_dir[x][y]), self.get_sie_digits())
                            scores_array_prom[w][0] = util.format_sie(prom, self.get_sie_digits())
                        if scores_array_prom_alt[w][0] != '--':
                            prom = util.round_sie(decimal.Decimal(scores_array_prom_alt[w][0]) +
                                                  decimal.Decimal(scores_array_dir[x][y]), self.get_sie_digits())
                            scores_array_prom_alt[w][0] = util.format_sie(prom, self.get_sie_digits())
                    w += 1
                position_array += longitude
            else:
                longitude = 0
                w = 0
                for x in range(num_students):
                    z = position_array
                    longitude = 2
                    for y in range(longitude):
                        if w == 0:
                            if z == position_array:
                                scores_array[w][z] = 'DIR'
                            else:
                                value = '*%s' % self.get_coe_professional_attitude('026', matrix_id, '025')
                                scores_array[w][z] = value.replace('.', ',')
                        else:
                            scores_array[w][z] = '--'
                        z += 1
                    # scores_array_prom[w][0] = '--'
                    w += 1
                position_array += longitude

            if flag_coe == 'C':
                w = 0
                for x in range(num_students):
                    z = position_array
                    longitude = len(scores_array_coe[x])
                    for y in range(longitude):
                        scores_array[w][z] = scores_array_coe[x][y]
                        z += 1
                    if w == 0:
                        scores_array_prom[w][0] = '---'
                        scores_array_prom_alt[w][0] = '---'
                    else:
                        if scores_array_coe[x][y] != '--':
                            if scores_array_prom[w][0] == '--':
                                prom = util.round_sie(decimal.Decimal(0) +
                                                      decimal.Decimal(scores_array_coe[x][y]), self.get_sie_digits())
                            else:
                                prom = util.round_sie(decimal.Decimal(scores_array_prom[w][0]) +
                                                      decimal.Decimal(scores_array_coe[x][y]), self.get_sie_digits())
                            scores_array_prom[w][0] = util.format_sie(prom, self.get_sie_digits())
                        else:
                            prom = float("0.0000")
                            scores_array_prom[w][0] = util.format_sie(prom, self.get_sie_digits())
                        if scores_array_coe[x][y - 1] != '--':
                            if scores_array_prom_alt[w][0] == '--':
                                prom_alt = util.round_sie(decimal.Decimal(0) +
                                                          decimal.Decimal(scores_array_coe[x][y - 1]),
                                                          self.get_sie_digits())
                            else:
                                prom_alt = util.round_sie(decimal.Decimal(scores_array_prom_alt[w][0]) +
                                                          decimal.Decimal(scores_array_coe[x][y - 1]),
                                                          self.get_sie_digits())
                            scores_array_prom_alt[w][0] = util.format_sie(prom_alt, self.get_sie_digits())
                        else:
                            prom_alt = float("0.0000")
                            scores_array_prom_alt[w][0] = util.format_sie(prom_alt, self.get_sie_digits())
                    w += 1
            else:
                longitude = 0
                w = 0
                for x in range(num_students):
                    z = position_array
                    longitude = 2
                    for y in range(longitude):
                        if w == 0:
                            if z == position_array:
                                scores_array[w][z] = 'COEV'
                            else:
                                value = '*%s' % self.get_coe_professional_attitude('030', matrix_id, '025')
                                scores_array[w][z] = value.replace('.', ',')
                        else:
                            scores_array[w][z] = '--'
                        z += 1
                    # scores_array_prom[w][0] = '--'
                    w += 1
                position_array += longitude

            w = 0
            for x in range(num_students):
                if w == 0:
                    scores_array[w][columns - 2] = column_name
                    scores_array[w][columns - 1] = '%s' % (coefficient_ap)
                else:
                    if number_ratings == 5:
                        if scores_array_prom[w][0] == '--':
                            scores_array[w][columns - 1] = '--'
                            scores_array[w][columns - 2] = '--'
                        else:
                            scores_array[w][columns - 2] = util.format_sie(float(scores_array_prom[w][0]),
                                                                           self.get_sie_digits())
                            prom = util.round_sie(decimal.Decimal(scores_array_prom[w][0]) *
                                                  decimal.Decimal(coefficient_ap), self.get_sie_digits())
                            scores_array[w][columns - 1] = util.format_sie(prom, self.get_sie_digits())
                    else:
                        if number_ratings > 0:
                            value = util.round_sie((decimal.Decimal(scores_array_prom_alt[w][0])
                                                    / number_ratings), self.get_sie_digits())
                            scores_array[w][columns - 2] = util.format_sie(value, self.get_sie_digits())
                        else:
                            scores_array[w][columns - 2] = '--'
                        if scores_array_prom_alt[w][0] == '--':
                            scores_array[w][columns - 1] = '--'
                        else:
                            prom = util.round_sie(decimal.Decimal(scores_array_prom_alt[w][0]) / number_ratings *
                                                  decimal.Decimal(coefficient_ap), self.get_sie_digits())
                            scores_array[w][columns - 1] = util.format_sie(prom, self.get_sie_digits())
                w += 1
        else:
            scores_array = []
        return scores_array

    def get_summary_professional_attitudes_array_1column(self, course):
        data = self.get_summary_professional_attitudes_array(course)
        if data:
            scores_array = self.get_summary_array_1column(data)
        else:
            scores_array = []
        return scores_array

    def get_scores_array_coe(self, scores_data, coefficient):
        scores_array = self.get_scores_array_by_score_number(scores_data, coefficient, True,
                                                             'sie.professional.attitude.student', 'COEVALUACION', 'No')
        return scores_array

    def get_scores_array_dir(self, scores_data, coefficient):
        scores_array = self.get_scores_array_by_score_number(scores_data, coefficient, True,
                                                             'sie.professional.attitude.student', 'OFICIALES')
        return scores_array

    def get_scores_array_pla(self, scores_data, coefficient):
        scores_array = self.get_scores_array_by_score_number(scores_data, coefficient, False,
                                                             'sie.professional.attitude.student', 'OFICIALES')
        return scores_array

    def get_scores_array_div(self, scores_data, coefficient):
        scores_array = self.get_scores_array_by_score_number(scores_data, coefficient, True,
                                                             'sie.professional.attitude.student', 'OFICIALES')
        return scores_array

    def get_scores_array_pro(self, scores_data, coefficient):
        scores_array = self.get_scores_array_by_score_number(scores_data, coefficient, False,
                                                             'sie.professional.attitude.student', 'PROFESORES')
        return scores_array

    def get_scores_array_pro_summary(self, scores_data, coefficient):
        scores_array = self.get_scores_array_by_score_number(scores_data, coefficient, True,
                                                             'sie.professional.attitude.student', 'PROFESORES')
        return scores_array

    def get_scores_array_div_summary(self, scores_data, coefficient, parameter_id):
        students = self.get_students(scores_data)
        num_students = len(students) + 1
        num_scores = len(scores_data)
        parameter = self.get_parameter_by_id(parameter_id)
        column_name = parameter.param_name.short_name

        # Get official_list
        official_list = [0 for u in range(num_scores)]
        u = 0
        for attitude in scores_data:
            official_list[u] = attitude.faculty_id.id
            u += 1
        officials = set(official_list)
        scores_official = [0 for r in range(len(officials))]

        u = 0
        for official in officials:
            attitudes = self.get_attitudes_by_official(int(self.course_id), parameter.id, official)
            if attitudes:
                scores_array_official = self.get_scores_array_by_score_number(attitudes, coefficient, True,
                                                                              'sie.professional.attitude.student',
                                                                              'OFICIALES')
                num_students = len(scores_array_official)
                scores_array_tmp = [0 for j in range(num_students)]
                w = 0
                for x in range(num_students):
                    longitude = len(scores_array_official[x])
                    for y in range(longitude):
                        if y == longitude - 2:
                            if x == 0:
                                evaluator = http.request.env['sie.faculty'].search([('id', '=', int(official))])
                                scores_array_tmp[w] = evaluator.acronym
                            else:
                                scores_array_tmp[w] = scores_array_official[x][y]
                    w += 1
                scores_official[u] = scores_array_tmp
                u += 1
        # students names
        num_scores = len(scores_official)
        scores_array = [[0 for j in range(num_scores + 6)] for i in range(num_students)]
        scores_array[0][0] = 'No.'
        scores_array[0][1] = 'Grado'
        scores_array[0][2] = 'Nombre'
        scores_array[0][3] = 'Id'
        i = 1
        for student in students:
            scores_array[i][0] = str(i)
            scores_array[i][1] = '%s-%s' % (student.student_id.grade_id.acronym,
                                            student.student_id.specialty_id.acronym)
            scores_array[i][2] = student.student_id.full_name
            scores_array[i][3] = student.student_id.id
            i += 1
        # scores
        x = 4
        for score_official in scores_official:
            y = 0
            for w in range(0, num_students):
                score = score_official[w]
                if score == 'False':
                    score_str = '--'
                else:
                    score_str = score.replace(',', '.')
                scores_array[y][x] = score_str
                y += 1
            x += 1

        # average
        scores_array[0][num_scores + 4] = column_name
        scores_array[0][num_scores + 5] = '*%s' % (coefficient)
        for z in range(1, num_students):
            sum_score = 0
            cant = num_scores
            for w in range(0, num_scores):
                if scores_array[z][w + 4] == '--':
                    cant -= 1
                else:
                    sum_score += decimal.Decimal(scores_array[z][w + 4])
            prom = 0
            if cant > 0:
                prom = util.round_sie(sum_score / cant, self.get_sie_digits())
                score_coefficient = util.round_sie(decimal.Decimal(prom) * decimal.Decimal(coefficient),
                                                   self.get_sie_digits())
                scores_array[z][num_scores + 4] = util.format_sie(prom, self.get_sie_digits())
                scores_array[z][num_scores + 5] = util.format_sie(score_coefficient, self.get_sie_digits())
            else:
                scores_array[z][num_scores + 4] = '--'
                scores_array[z][num_scores + 5] = '--'
        return scores_array

    def get_scores_array_month(self, month_columns, num_students, longitude, scores_array, month):
        scores_array_month_tmp = [[0 for j in range(month_columns)] for i in range(num_students)]
        w = 0
        for x in range(num_students):
            z = 0
            for y in range(longitude):
                if y > (longitude - month_columns - 1):
                    scores_array_month_tmp[w][z] = scores_array[x][y]
                    z += 1
            w += 1

        officials = set(scores_array_month_tmp[0])
        longitude = len(scores_array_month_tmp[0])
        num_officials = len(officials)
        num_students = len(scores_array_month_tmp)
        scores_array_official = [[0 for j in range(num_officials)] for i in range(num_students)]
        z = 0
        count = 0
        for official in officials:
            w = 0
            for x in range(num_students):
                for y in range(longitude):
                    if x != 0:
                        if scores_array_month_tmp[0][y] == official:
                            if scores_array_month_tmp[x][y] != '--':
                                scores_array_official[w][z] += decimal.Decimal(scores_array_month_tmp[x][y])
                            count += 1
                    else:
                        if scores_array_month_tmp[0][y] == official:
                            scores_array_official[w][z] = scores_array_month_tmp[x][y]
                if w != 0:
                    if scores_array_official[w][z] != '--':
                        # count reemplazado por 1 para no promediar las notas de cada oficial
                        prom = util.round_sie(decimal.Decimal(scores_array_official[w][z]) / count,
                                              self.get_sie_digits())
                        # prom = util.round_sie(decimal.Decimal(scores_array_official[w][z]),self.get_sie_digits())
                        scores_array_official[w][z] = util.format_sie(prom, self.get_sie_digits())
                    else:
                        scores_array_official[w][z] = '--'
                    count = 0
                w += 1
            z += 1
        scores_array_official_final = [[0 for j in range(1)] for i in range(num_students)]
        longitude = len(scores_array_official[0])
        z = 0
        w = 0
        for x in range(num_students):
            for y in range(longitude):
                if x != 0:
                    if scores_array_official[x][y] != '--':
                        scores_array_official_final[w][z] += decimal.Decimal(scores_array_official[x][y])
                    count += 1
                else:
                    scores_array_official_final[w][z] = scores_array_official[x][y]
            if w != 0:
                if scores_array_official_final[w][z] != '--':
                    prom = util.round_sie(decimal.Decimal(scores_array_official_final[w][z]) / count,
                                          self.get_sie_digits())
                    scores_array_official_final[w][z] = util.format_sie(prom, self.get_sie_digits())
                else:
                    scores_array_official_final[w][z] = '--'
                count = 0
            else:
                scores_array_official_final[w][z] = month
            w += 1
        return scores_array_official_final

    def get_scores_array_pla_summary(self, attitudes, coefficient, parameter_id):
        students = attitudes[0].student_ids.sorted(key=attrgetter('last_name_1', 'last_name_2')). \
            filtered(lambda r: r.student_id.inactive == False)
        num_students = len(students) + 1
        num_scores = len(attitudes)
        parameter = self.get_parameter_by_id(parameter_id)
        column_name = parameter.param_name.short_name

        scores_array = [[0 for j in range(num_scores + 4)] for i in range(num_students)]  # cambio
        scores_array[0][0] = 'No.'
        scores_array[0][1] = 'Grado'
        scores_array[0][2] = 'Nombre'
        scores_array[0][3] = 'Id'
        # column header
        y = 4
        month_columns_a = month_columns_b = month_columns_c = month_columns_d = month_columns_e = month_columns_f = \
            month_columns_g = month_columns_h = month_columns_i = month_columns_j = month_columns_k = \
            month_columns_l = 0
        for attitude in attitudes:
            if attitude.month == 'a':
                month_columns_a += 1
            if attitude.month == 'b':
                month_columns_b += 1
            if attitude.month == 'c':
                month_columns_c += 1
            if attitude.month == 'd':
                month_columns_d += 1
            if attitude.month == 'e':
                month_columns_e += 1
            if attitude.month == 'f':
                month_columns_f += 1
            if attitude.month == 'g':
                month_columns_g += 1
            if attitude.month == 'h':
                month_columns_h += 1
            if attitude.month == 'i':
                month_columns_i += 1
            if attitude.month == 'j':
                month_columns_j += 1
            if attitude.month == 'k':
                month_columns_k += 1
            if attitude.month == 'l':
                month_columns_l += 1

            heading_text = u'%s' % (attitude.month)
            # heading_text = u'%s-%s' % (attitude.month, attitude.faculty_id.id)
            scores_array[0][y] = heading_text
            y += 1
        # students names
        i = 1
        for student in students:
            scores_array[i][0] = str(i)
            scores_array[i][1] = '%s-%s' % (student.student_id.grade_id.acronym,
                                            student.student_id.specialty_id.acronym)
            scores_array[i][2] = student.student_id.full_name
            scores_array[i][3] = student.student_id.id
            i += 1
        # scores
        x = 4
        for attitude in attitudes:
            students_score = self.get_students_professional_attitude(attitude)
            y = 1
            for student in students_score:
                score = str(student.score)
                if score == 'False':
                    score = '--'
                else:
                    score = score.replace(',', '.')
                scores_array[y][x] = score
                y += 1
            x += 1
        # arreglo final
        num_months = 0
        if month_columns_a > 0:
            num_months += 1
        if month_columns_b > 0:
            num_months += 1
        if month_columns_c > 0:
            num_months += 1
        if month_columns_d > 0:
            num_months += 1
        if month_columns_e > 0:
            num_months += 1
        if month_columns_f > 0:
            num_months += 1
        if month_columns_g > 0:
            num_months += 1
        if month_columns_h > 0:
            num_months += 1
        if month_columns_i > 0:
            num_months += 1
        if month_columns_j > 0:
            num_months += 1
        if month_columns_k > 0:
            num_months += 1
        if month_columns_l > 0:
            num_months += 1
        scores_array_tmp = [[0 for j in range(num_months + 6)] for i in range(num_students)]
        scores_array_tmp[0][0] = 'No.'
        scores_array_tmp[0][1] = 'Grado'
        scores_array_tmp[0][2] = 'Nombre'
        scores_array_tmp[0][3] = 'Id'
        # students names
        i = 1
        for student in students:
            scores_array_tmp[i][0] = str(i)
            scores_array_tmp[i][1] = '%s-%s' % (student.student_id.grade_id.acronym,
                                                student.student_id.specialty_id.acronym)
            scores_array_tmp[i][2] = student.student_id.full_name
            scores_array_tmp[i][3] = student.student_id.id
            i += 1
        # Scores by month
        p = 4
        longitude = 4

        if month_columns_a > 0:
            longitude += month_columns_a
            scores_array_a = self.get_scores_array_month(month_columns_a, num_students, longitude, scores_array, 'ENE')
            if scores_array_a:
                for x in range(num_students):
                    scores_array_tmp[x][p] = scores_array_a[x][0]
            p += 1
        if month_columns_b > 0:
            longitude += month_columns_b
            scores_array_b = self.get_scores_array_month(month_columns_b, num_students, longitude, scores_array, 'FEB')
            if scores_array_b:
                for x in range(num_students):
                    scores_array_tmp[x][p] = scores_array_b[x][0]
            p += 1
        if month_columns_c > 0:
            longitude += month_columns_c
            scores_array_c = self.get_scores_array_month(month_columns_c, num_students, longitude, scores_array, 'MAR')
            if scores_array_c:
                for x in range(num_students):
                    scores_array_tmp[x][p] = scores_array_c[x][0]
            p += 1
        if month_columns_d > 0:
            longitude += month_columns_d
            scores_array_d = self.get_scores_array_month(month_columns_d, num_students, longitude, scores_array, 'ABR')
            if scores_array_d:
                for x in range(num_students):
                    scores_array_tmp[x][p] = scores_array_d[x][0]
            p += 1
        if month_columns_e > 0:
            longitude += month_columns_e
            scores_array_e = self.get_scores_array_month(month_columns_e, num_students, longitude, scores_array, 'MAY')
            if scores_array_e:
                for x in range(num_students):
                    scores_array_tmp[x][p] = scores_array_e[x][0]
            p += 1
        if month_columns_f > 0:
            longitude += month_columns_f
            scores_array_f = self.get_scores_array_month(month_columns_f, num_students, longitude, scores_array, 'JUN')
            if scores_array_f:
                for x in range(num_students):
                    scores_array_tmp[x][p] = scores_array_f[x][0]
            p += 1
        if month_columns_g > 0:
            longitude += month_columns_g
            scores_array_g = self.get_scores_array_month(month_columns_g, num_students, longitude, scores_array, 'JUL')
            if scores_array_g:
                for x in range(num_students):
                    scores_array_tmp[x][p] = scores_array_g[x][0]
            p += 1
        if month_columns_h > 0:
            longitude += month_columns_h
            scores_array_h = self.get_scores_array_month(month_columns_h, num_students, longitude, scores_array, 'AGO')
            if scores_array_h:
                for x in range(num_students):
                    scores_array_tmp[x][p] = scores_array_h[x][0]
            p += 1
        if month_columns_i > 0:
            longitude += month_columns_i
            scores_array_i = self.get_scores_array_month(month_columns_i, num_students, longitude, scores_array, 'SEP')
            if scores_array_i:
                for x in range(num_students):
                    scores_array_tmp[x][p] = scores_array_i[x][0]
            p += 1
        if month_columns_j > 0:
            longitude += month_columns_j
            scores_array_j = self.get_scores_array_month(month_columns_j, num_students, longitude, scores_array, 'OCT')
            if scores_array_j:
                for x in range(num_students):
                    scores_array_tmp[x][p] = scores_array_j[x][0]
            p += 1
        if month_columns_k > 0:
            longitude += month_columns_k
            scores_array_k = self.get_scores_array_month(month_columns_k, num_students, longitude, scores_array, 'NOV')
            if scores_array_k:
                for x in range(num_students):
                    scores_array_tmp[x][p] = scores_array_k[x][0]
            p += 1
        if month_columns_l > 0:
            longitude += month_columns_l
            scores_array_l = self.get_scores_array_month(month_columns_l, num_students, longitude, scores_array, 'DIC')
            if scores_array_l:
                for x in range(num_students):
                    scores_array_tmp[x][p] = scores_array_l[x][0]
            p += 1
        scores_array_tmp[0][num_months + 4] = column_name
        coefficient_text = '*%s' % coefficient
        scores_array_tmp[0][num_months + 5] = coefficient_text.replace('.', ',')

        # average
        for z in range(1, num_students):
            sum_score = 0
            cant = num_months
            for w in range(0, num_months):
                if scores_array_tmp[z][w + 4] == '--':
                    cant -= 1
                else:
                    sum_score += decimal.Decimal(scores_array_tmp[z][w + 4])
            prom = 0
            if cant > 0:
                prom = util.round_sie(sum_score / cant, self.get_sie_digits())
                score_coefficient = util.round_sie(decimal.Decimal(prom) * decimal.Decimal(coefficient),
                                                   self.get_sie_digits())
                scores_array_tmp[z][num_months + 4] = util.format_sie(prom, self.get_sie_digits())
                scores_array_tmp[z][num_months + 5] = util.format_sie(score_coefficient, self.get_sie_digits())
            else:
                scores_array_tmp[z][num_months + 4] = '--'
                scores_array_tmp[z][num_months + 5] = '--'

        return scores_array_tmp

    @staticmethod
    def get_month_spanish(month):
        month_spanish = ''
        if month == u'a':
            month_spanish = 'Ene'
        if month == u'b':
            month_spanish = 'Feb'
        if month == u'c':
            month_spanish = 'Mar'
        if month == u'd':
            month_spanish = 'Abr'
        if month == u'e':
            month_spanish = 'May'
        if month == u'f':
            month_spanish = 'Jun'
        if month == u'g':
            month_spanish = 'Jul'
        if month == u'h':
            month_spanish = 'Ago'
        if month == u'i':
            month_spanish = 'Sep'
        if month == u'j':
            month_spanish = 'Oct'
        if month == u'k':
            month_spanish = 'Nov'
        if month == u'l':
            month_spanish = 'Dic'
        return month_spanish

    @staticmethod
    def get_month_spanish_fullname(month):
        month_spanish = ''
        if month == u'01':
            month_spanish = 'Enero'
        if month == u'02':
            month_spanish = 'Febrero'
        if month == u'03':
            month_spanish = 'Marzo'
        if month == u'04':
            month_spanish = 'Abril'
        if month == u'05':
            month_spanish = 'Mayo'
        if month == u'06':
            month_spanish = 'Junio'
        if month == u'07':
            month_spanish = 'Julio'
        if month == u'08':
            month_spanish = 'Agosto'
        if month == u'09':
            month_spanish = 'Septiembre'
        if month == u'10':
            month_spanish = 'Octubre'
        if month == u'11':
            month_spanish = 'Noviembre'
        if month == u'12':
            month_spanish = 'Diciembre'
        return month_spanish

    # common methods

    def get_students(self, scores_data):
        students = scores_data[0].student_ids.sorted(key=attrgetter('last_name_1', 'last_name_2')). \
            filtered(lambda r: r.student_id.inactive == False)
        return students

    def get_scores_array_by_score_number(self, scores_data, coefficient, average,
                                         table_name, type, title=None, groups=None):
        students = []
        if groups:
            for group in groups:
                students += group.student_ids.sorted(key=attrgetter('last_name_1', 'last_name_2')). \
                    filtered(lambda r: r.student_id.inactive == False)
        else:
            students = scores_data[0].student_ids.sorted(key=attrgetter('last_name_1', 'last_name_2')). \
                filtered(lambda r: r.student_id.inactive == False)
        students = sorted(students, key=attrgetter('last_name_1', 'last_name_2'))
        num_scores = 0
        teachers = []
        notes = []
        if type == 'productivity':
            teachers_list = []
            for data_teacher in scores_data:
                teachers_list += data_teacher.evaluator_id
            teachers = set(teachers_list)
            num_scores = len(teachers)
            column_name = scores_data[0].parameter_id.param_name.short_name
        elif type == '':
            note_list = []
            for data_note in scores_data:
                note_list += data_note.score_number
            notes = sorted(set(note_list))
            num_scores = len(notes)
            column_name = scores_data[0].parameter_id.param_name.short_name
        elif type == 'EXAMENPU':
            note_list = []
            for data_note in scores_data:
                if data_note.score_number:
                    note_list += data_note.score_number
                else:
                    note_list.append(1)
            notes = set(note_list)
            num_scores = len(notes)
            column_name = 'EXPU'
        elif type == 'EXAMENVF':
            note_list = []
            for data_note in scores_data:
                if data_note.score_number:
                    note_list += data_note.score_number
                else:
                    note_list.append(1)
            notes = set(note_list)
            num_scores = len(notes)
            column_name = 'EXVF'
        elif type == 'COEVALUACION':
            num_scores = len(scores_data)
            column_name = (self.get_parameter_by_id(scores_data[0].parameter_id)).param_name.short_name
        elif type == 'PROFESORES':
            num_scores = len(scores_data)
            column_name = (self.get_parameter_by_id(scores_data[0].parameter_id)).param_name.short_name
        elif type == 'OFICIALES':
            num_scores = len(scores_data)
            column_name = (self.get_parameter_by_id(scores_data[0].parameter_id)).param_name.short_name
        else:
            note_list = []
            for data_note in scores_data:
                note_list += data_note.score_number
            notes = set(note_list)
            num_scores = len(notes)
            column_name = scores_data[0].parameter_id.param_name.short_name
        num_students = len(students) + 1
        if average:
            scores_array = [[0 for j in range(num_scores + 6)] for i in range(num_students)]
        else:
            scores_array = [[0 for j in range(num_scores + 4)] for i in range(num_students)]
        for i in range(len(scores_array)):
            for j in range(len(scores_array[i])):
                scores_array[i][j] = '--'
        scores_array[0][0] = 'No.'
        scores_array[0][1] = 'Grado'
        scores_array[0][2] = 'Nombre'
        scores_array[0][3] = 'Id'

        y = 4
        if type == 'productivity':
            for teacher in teachers:
                heading_text = u'%s' % (teacher.acronym)
                scores_array[0][y] = heading_text
                y += 1
        elif type == '':
            for note in notes:
                heading_text = u'%s-%s' % (title, note)
                scores_array[0][y] = heading_text
                y += 1
        elif type == 'COEVALUACION':
            for attitude in scores_data:
                heading_text = u'%s-%s' % (title, attitude.score_number)
                scores_array[0][y] = heading_text
                y += 1
        elif type == 'PROFESORES':
            for attitude in scores_data:
                heading_text = u'%s' % attitude.subject_id.acronym
                scores_array[0][y] = heading_text
                y += 1
        elif type == 'OFICIALES':
            for attitude in scores_data:
                heading_text = u'%s-%s' % (self.get_month_spanish(attitude.month), attitude.fortnight)
                scores_array[0][y] = heading_text
                y += 1
        else:
            for note in notes:
                heading_text = u'%s-%s' % (title, note)
                scores_array[0][y] = heading_text
                y += 1
        i = 1
        for student in students:
            scores_array[i][0] = str(i)
            scores_array[i][1] = '%s-%s' % (student.student_id.grade_id.acronym,
                                            student.student_id.specialty_id.acronym)
            scores_array[i][2] = student.student_id.full_name
            scores_array[i][3] = '%s' % student.student_id.id
            i += 1
        list_students = [row[2] for row in scores_array]
        x = 4
        for data in scores_data:
            students_score = http.request.env[table_name].search([('score_id', '=', data.id)]). \
                sorted(key=attrgetter('last_name_1', 'last_name_2')).filtered(lambda r: r.student_id.inactive == False)
            for student in students_score:
                score = str(student.score)
                if score == 'False':
                    score = '--'
                else:
                    score = score.replace(',', '.')

                name_student = student.student_id.full_name
                y = list_students.index(name_student)

                if type == 'productivity':
                    acronym = data.evaluator_id.acronym
                    x = scores_array[0].index(acronym)
                elif type == '':
                    note = data.score_number
                    x = scores_array[0].index('%s-%s' % (title, note))
                elif type == 'attitude':
                    note = data.score_number
                    x = scores_array[0].index('%s-%s' % ('No', note))
                elif type == 'COEVALUACION':
                    note = data.score_number
                    x = scores_array[0].index('%s-%s' % (title, note))
                elif type == 'PROFESORES':
                    heading_text = u'%s' % data.subject_id.acronym
                    x = scores_array[0].index(heading_text)
                elif type == 'OFICIALES':
                    heading_text = u'%s-%s' % (self.get_month_spanish(data.month), data.fortnight)
                    x = scores_array[0].index(heading_text)
                elif type == 'EXAMENPU':
                    note = data.score_number
                    x = scores_array[0].index('%s-%s' % (title, note))
                elif type == 'EXAMENVF':
                    note = 1
                    x = scores_array[0].index('%s-%s' % (title, note))
                else:
                    note = data.score_number
                    x = scores_array[0].index('%s-%s' % (title, note))

                scores_array[y][x] = score

        if average:
            scores_array[0][num_scores + 4] = column_name
            scores_array[0][num_scores + 5] = '*%s' % (coefficient)

            for z in range(1, num_students):
                sum_score = 0
                cant = num_scores
                for w in range(0, num_scores):
                    if scores_array[z][w + 4] == '--':
                        cant -= 1
                    else:
                        sum_score += decimal.Decimal(scores_array[z][w + 4])
                # prom = 0
                if cant > 0:
                    prom = util.round_sie(sum_score / cant, self.get_sie_digits())
                    score_coefficient_tmp = prom * coefficient
                    score_coefficient = util.round_sie(float(score_coefficient_tmp),
                                                       self.get_sie_digits())
                    scores_array[z][num_scores + 4] = util.format_sie(prom, self.get_sie_digits())
                    scores_array[z][num_scores + 5] = util.format_sie(score_coefficient, self.get_sie_digits())
                else:
                    scores_array[z][num_scores + 4] = '--'
                    scores_array[z][num_scores + 5] = '--'

        return scores_array

    # Separa la data de usuarios de las notas
    def get_result_all(self, scores_data, flag):
        num_students = len(scores_data)

        columns = len(scores_data[0]) - 4
        scores_array_users = [[0 for j in range(4)] for i in range(num_students)]
        scores_array_tmp = [[0 for j in range(columns)] for i in range(num_students)]
        w = 0
        for x in range(num_students):
            z = zz = 0
            longitude = len(scores_data[x])
            for y in range(longitude):
                if y < 4:
                    scores_array_users[w][zz] = scores_data[x][y]
                    zz += 1
                else:
                    scores_array_tmp[w][z] = scores_data[x][y]
                    z += 1
            w += 1
        return flag, columns, scores_array_tmp, scores_array_users

    # Separa la data de usuarios de los promedios de las notas
    def get_result(self, scores_data, flag):
        num_students = len(scores_data)
        scores_array = [[0 for j in range(6)] for i in range(num_students)]
        w = 0
        for x in range(num_students):
            z = 0
            longitude = len(scores_data[x])
            for y in range(longitude):
                if (y < 4) or (y > longitude - 3):
                    scores_array[w][z] = scores_data[x][y]
                    z += 1
            w += 1

        num_students = len(scores_array)
        columns = len(scores_array[0]) - 4
        scores_array_users = [[0 for j in range(4)] for i in range(num_students)]
        scores_array_tmp = [[0 for j in range(columns)] for i in range(num_students)]
        w = 0
        for x in range(num_students):
            z = zz = 0
            longitude = len(scores_array[x])
            for y in range(longitude):
                if y < 4:
                    scores_array_users[w][zz] = scores_array[x][y]
                    zz += 1
                else:
                    scores_array_tmp[w][z] = scores_array[x][y]
                    z += 1
            w += 1

        return flag, columns, scores_array_tmp, scores_array_users

    def get_scores_array_not_score_number(self, scores_data, coefficient, average, table_name, title,
                                          groups=None):
        students = []
        if groups:
            for group in groups:
                students += group.student_ids.sorted(key=attrgetter('last_name_1', 'last_name_2')). \
                    filtered(lambda r: r.student_id.inactive == False)
        else:
            students = scores_data[0].student_ids.sorted(key=attrgetter('last_name_1', 'last_name_2')). \
                filtered(lambda r: r.student_id.inactive == False)
        column_name = scores_data[0].parameter_id.param_name.short_name
        note_list = []
        f = 0
        for data_note in scores_data:
            f += 1
            if data_note.score_number:
                note_list.append(data_note.score_number)
            else:
                index = u'%s' % f
                note_list.append(index)
        num_students = len(students) + 1
        notes = sorted(set(note_list))
        num_scores = len(notes)
        scores_array = [[0 for j in range(num_scores + 6)] for i in range(num_students)]
        for i in range(len(scores_array)):
            for j in range(len(scores_array[i])):
                scores_array[i][j] = '--'
        scores_array[0][0] = 'No.'
        scores_array[0][1] = 'Grado'
        scores_array[0][2] = 'Nombre'
        scores_array[0][3] = 'Id'

        y = 4
        for note in notes:
            heading_text = u'%s-%s' % (title, note)
            scores_array[0][y] = heading_text
            y += 1

        i = 1
        for student in students:
            scores_array[i][0] = str(i)
            scores_array[i][1] = '%s-%s' % (student.student_id.grade_id.acronym,
                                            student.student_id.specialty_id.acronym)
            scores_array[i][2] = student.student_id.full_name
            scores_array[i][3] = '%s' % student.student_id.id
            i += 1
        list_students = [row[2] for row in scores_array]
        x = 4
        f = 0
        for data in scores_data:
            students_score = http.request.env[table_name] \
                .search([('score_id', '=', data.id)]). \
                sorted(key=attrgetter('last_name_1', 'last_name_2')).filtered(lambda r: r.student_id.inactive == False)
            f += 1
            for student in students_score:
                score = str(student.score)
                if score == 'False':
                    score = '--'
                else:
                    score = score.replace(',', '.')

                name_student = student.student_id.full_name

                if data.score_number:
                    note = data.score_number
                else:
                    note = u'%s' % f
                x = scores_array[0].index('%s-%s' % (title, note))
                y = list_students.index(name_student)
                scores_array[y][x] = score
        if average:
            scores_array[0][num_scores + 4] = column_name
            scores_array[0][num_scores + 5] = '%s' % util.format_sie(coefficient, u'3')

            for z in range(1, num_students):
                sum_score = 0
                cant = num_scores
                for w in range(0, num_scores):
                    if scores_array[z][w + 4] == '--':
                        cant -= 1
                    else:
                        sum_score += decimal.Decimal(scores_array[z][w + 4])
                # prom = 0
                if cant > 0:
                    prom = util.round_sie(sum_score / cant, self.get_sie_digits())
                    score_coefficient_tmp = prom * coefficient
                    score_coefficient = util.round_sie(float(score_coefficient_tmp),
                                                       self.get_sie_digits())
                    scores_array[z][num_scores + 4] = util.format_sie(prom, self.get_sie_digits())
                    scores_array[z][num_scores + 5] = util.format_sie(score_coefficient, self.get_sie_digits())
                else:
                    scores_array[z][num_scores + 4] = '--'
                    scores_array[z][num_scores + 5] = '--'

        return scores_array

    def get_sie_digits(self):
        config_parameter = http.request.env['ir.config_parameter']
        parameter = config_parameter.search([('key', '=', 'sie_round_digits')])
        if parameter:
            value = parameter.value
            try:
                data = int(value)
                if data > 5:
                    value = u'5'
            except:
                value = u'5'
        else:
            value = u'3'
        return value

    def get_sie_digits_certificate(self):
        config_parameter = http.request.env['ir.config_parameter']
        parameter = config_parameter.search([('key', '=', 'sie_round_digits_certificate')])
        if parameter:
            value = parameter.value
            try:
                data = int(value)
                if data > 6:
                    value = u'6'
            except:
                value = u'6'
        else:
            value = u'6'
        return value

    def get_detail_one(self, num_child, scores_array_child, coefficient, title):
        num_columns = 0
        if num_child == 1:
            data = scores_array_child
            num_students = len(data)
            longitude = len(data[0])
            num_columns = longitude
            scores_array = [[0 for j in range(num_columns)] for i in range(num_students)]

            for x in range(num_students):
                for y in range(longitude):
                    if x == 0:
                        if y == longitude - 2:
                            scores_array[x][y] = title
                        elif y == longitude - 1:
                            scores_array[x][y] = '%s' % str(coefficient)
                        else:
                            scores_array[x][y] = data[x][y]
                    else:
                        scores_array[x][y] = data[x][y]

        else:
            scores_array = []
        return scores_array

    def get_detail(self, num_child, scores_array_child, coefficient, title):
        num_columns = 0
        scores_array = []
        if num_child == 1:
            x = -2
            longitude = len(scores_array_child)
            for y in range(longitude):
                try:
                    if len(scores_array_child[y]) > 0:
                        x = y
                except:
                    if x == -2:
                        x = -1
            if x != -1:
                data = scores_array_child[x]
                num_students = len(data)
                longitude = len(data[x])
                num_columns = longitude + 2
                scores_array = [[0 for j in range(num_columns)] for i in range(num_students)]
                scores_array_prom = [[0 for j in range(1)] for i in range(num_students)]

                for x in range(num_students):
                    for y in range(longitude):
                        scores_array[x][y] = data[x][y]
                    if x == 0:
                        scores_array_prom[x][0] = title
                    else:
                        if data[x][y] == '--':
                            scores_array_prom[x][0] = data[x][y - 1]
                        else:
                            scores_array_prom[x][0] = decimal.Decimal(data[x][y - 1])
                for x in range(num_students):
                    if x == 0:
                        scores_array[x][num_columns - 2] = scores_array_prom[x][0]
                        scores_array[x][num_columns - 1] = '%s' % (coefficient)
                    else:
                        if scores_array_prom[x][0] == '--':
                            scores_array[x][num_columns - 2] = '--'
                            scores_array[x][num_columns - 1] = '--'
                        else:
                            prom = util.round_sie(decimal.Decimal(scores_array_prom[x][0]), self.get_sie_digits())
                            score_coefficient_tmp = prom * float(coefficient)
                            score_coefficient = util.round_sie(float(score_coefficient_tmp),
                                                               self.get_sie_digits())
                            scores_array[x][num_columns - 2] = util.format_sie(prom, self.get_sie_digits())
                            scores_array[x][num_columns - 1] = util.format_sie(score_coefficient, self.get_sie_digits())

        elif num_child > 1:
            num_students = len(scores_array_child[0])
            for y in range(num_child):
                data = scores_array_child[y]
                if data:
                    num_columns += len(data[0])
                else:
                    num_child -= 1
            num_columns = num_columns - 4 * (num_child - 1) + 2
            scores_array = [[0 for j in range(num_columns)] for i in range(num_students)]
            scores_array_prom = [[0 for j in range(1)] for i in range(num_students)]
            position = 0
            for w in range(num_child):
                data = scores_array_child[w]
                longitude = len(data[0])

                if w == 0:
                    position = longitude
                    for x in range(num_students):
                        for y in range(longitude):
                            scores_array[x][y] = data[x][y]
                        if x == 0:
                            scores_array_prom[x][0] = title
                        else:
                            if data[x][y] == '--':
                                scores_array_prom[x][0] = '--'
                            else:
                                scores_array_prom[x][0] = decimal.Decimal(data[x][y])
                else:
                    z = 0
                    for x in range(num_students):
                        z = position
                        for y in range(longitude):
                            if y > 3:
                                scores_array[x][z] = data[x][y]
                                z += 1
                        if x == 0:
                            scores_array_prom[x][0] = title
                        else:
                            if data[x][y] != '--':
                                if scores_array_prom[x][0] != '--':
                                    scores_array_prom[x][0] += decimal.Decimal(data[x][y])
                                else:
                                    scores_array_prom[x][0] = decimal.Decimal(data[x][y - 1])
                            else:
                                data_0 = scores_array_child[w - 1]
                                y_0 = len(data_0[0]) - 2
                                if data_0[x][y_0] == '--':
                                    scores_array_prom[x][0] = data_0[x][y_0]
                                else:
                                    scores_array_prom[x][0] = decimal.Decimal(data_0[x][y_0])
                    position = z
            for x in range(num_students):
                if x == 0:
                    scores_array[x][num_columns - 2] = scores_array_prom[x][0]
                    scores_array[x][num_columns - 1] = '%s' % (coefficient)
                else:
                    if scores_array_prom[x][0] == '--':
                        scores_array[x][num_columns - 2] = '--'
                        scores_array[x][num_columns - 1] = '--'
                    else:
                        prom = util.round_sie(decimal.Decimal(scores_array_prom[x][0]), self.get_sie_digits())
                        score_coefficient_tmp = prom * float(coefficient)
                        score_coefficient = util.round_sie(float(score_coefficient_tmp),
                                                           self.get_sie_digits())
                        scores_array[x][num_columns - 2] = util.format_sie(prom, self.get_sie_digits())
                        scores_array[x][num_columns - 1] = util.format_sie(score_coefficient, self.get_sie_digits())
        else:
            scores_array = []
        return scores_array

    def get_detail_final(self, num_child, scores_array_child, coefficient, title):
        value = 0
        for x in range(num_child):
            value += float(scores_array_child[x][0][len(scores_array_child[x][0]) - 1])

        num_columns = 0
        scores_array = []
        if num_child == 1:
            x = -2
            longitude = len(scores_array_child)
            for y in range(longitude):
                try:
                    if len(scores_array_child[y]) > 0:
                        x = y
                except:
                    if x == -2:
                        x = -1
            if x != -1:
                data = scores_array_child[x]
                num_students = len(data)
                longitude = len(data[x])
                num_columns = longitude + 2
                scores_array = [[0 for j in range(num_columns)] for i in range(num_students)]
                scores_array_prom = [[0 for j in range(1)] for i in range(num_students)]

                for x in range(num_students):
                    for y in range(longitude):
                        scores_array[x][y] = data[x][y]
                    if x == 0:
                        scores_array_prom[x][0] = title
                    else:
                        if data[x][y] == '--':
                            scores_array_prom[x][0] = data[x][y - 1]
                        else:
                            scores_array_prom[x][0] = decimal.Decimal(data[x][y - 1])
                for x in range(num_students):
                    if x == 0:
                        scores_array[x][num_columns - 2] = scores_array_prom[x][0]
                        scores_array[x][num_columns - 1] = util.format_sie(util.round_sie(coefficient,
                                                                                          self.get_sie_digits()),
                                                                           self.get_sie_digits()).replace('.', ',')
                    else:
                        if scores_array_prom[x][0] == '--':
                            scores_array[x][num_columns - 2] = '--'
                            scores_array[x][num_columns - 1] = '--'
                        else:
                            prom = util.round_sie(decimal.Decimal(scores_array_prom[x][0]), self.get_sie_digits())
                            score_coefficient_tmp = prom * float(coefficient)
                            score_coefficient = util.round_sie(float(score_coefficient_tmp),
                                                               self.get_sie_digits_certificate())
                            scores_array[x][num_columns - 2] = util.format_sie(prom, self.get_sie_digits())
                            scores_array[x][num_columns - 1] = util.format_sie(score_coefficient,
                                                                               self.get_sie_digits_certificate())

        elif num_child > 1:

            num_students = len(scores_array_child[0])
            for y in range(num_child):
                data = scores_array_child[y]
                num_columns += len(data[0])
            num_columns = num_columns - 4 * (num_child - 1) + 2
            scores_array = [[0 for j in range(num_columns)] for i in range(num_students)]
            scores_array_prom = [[0 for j in range(1)] for i in range(num_students)]
            scores_array_prom_alt = [[0 for j in range(1)] for i in range(num_students)]
            scores_array_num = [[0 for j in range(1)] for i in range(num_students)]
            position = 0
            for w in range(num_child):
                data = scores_array_child[w]
                longitude = len(data[0])

                if w == 0:
                    position = longitude
                    for x in range(num_students):
                        number_scores = num_child
                        for y in range(longitude):
                            scores_array[x][y] = data[x][y]
                        if x == 0:
                            scores_array_prom[x][0] = title
                        else:
                            if value == 1:
                                if data[x][y] == '--':
                                    scores_array_prom[x][0] = '--'
                                    scores_array_num[x][0] += 1
                                else:
                                    scores_array_prom[x][0] = decimal.Decimal(data[x][y])
                                    scores_array_prom_alt[x][0] = decimal.Decimal(data[x][y - 1])
                            else:
                                if data[x][y] == '--':
                                    scores_array_prom_alt[x][0] = '--'
                                    scores_array_num[x][0] += 1
                                else:
                                    scores_array_prom_alt[x][0] = decimal.Decimal(data[x][y - 1])
                else:
                    z = 0
                    for x in range(num_students):
                        number_scores = num_child
                        z = position
                        for y in range(longitude):
                            if y > 3:
                                scores_array[x][z] = data[x][y]
                                z += 1
                        if x == 0:
                            scores_array_prom[x][0] = title
                        else:
                            if value == 1:
                                if data[x][y] != '--':
                                    if scores_array_prom[x][0] != '--':
                                        scores_array_prom[x][0] += decimal.Decimal(data[x][y])
                                    if scores_array_prom_alt[x][0] != '--':
                                        scores_array_prom_alt[x][0] += decimal.Decimal(data[x][y - 1])
                                else:
                                    scores_array_num[x][0] += 1
                            else:
                                if data[x][y] != '--':
                                    if scores_array_prom_alt[x][0] != '--':
                                        scores_array_prom_alt[x][0] += decimal.Decimal(data[x][y - 2])
                                    else:
                                        scores_array_prom_alt[x][0] = decimal.Decimal(data[x][y - 2])
                                else:
                                    scores_array_num[x][0] += 1
                    position = z
            for x in range(num_students):
                if x == 0:
                    scores_array[x][num_columns - 2] = scores_array_prom[x][0]
                    scores_array[x][num_columns - 1] = util.format_sie(util.round_sie(coefficient,
                                                                                      self.get_sie_digits()),
                                                                       self.get_sie_digits()).replace('.', ',')
                else:
                    if scores_array_num[x][0] == 0:
                        if scores_array_prom[x][0] == '--':
                            scores_array[x][num_columns - 2] = '--'
                            scores_array[x][num_columns - 1] = '--'
                        else:
                            prom = util.round_sie(decimal.Decimal(scores_array_prom[x][0]), self.get_sie_digits())
                            score_coefficient_tmp = prom * float(coefficient)
                            score_coefficient = util.round_sie(float(score_coefficient_tmp),
                                                               self.get_sie_digits_certificate())
                            scores_array[x][num_columns - 2] = util.format_sie(prom, self.get_sie_digits())
                            scores_array[x][num_columns - 1] = util.format_sie(score_coefficient,
                                                                               self.get_sie_digits_certificate())
                    else:
                        if scores_array_prom_alt[x][0] == '--':
                            scores_array[x][num_columns - 2] = '--'
                            scores_array[x][num_columns - 1] = '--'
                        else:
                            prom_zero = (number_scores - scores_array_num[x][0])
                            if prom_zero == 0:
                                prom = 0
                            else:
                                prom = util.round_sie(decimal.Decimal(scores_array_prom_alt[x][0] / prom_zero),
                                                      self.get_sie_digits())
                            if scores_array_num[x][0] > 0:
                                score_coefficient_tmp = prom * float(coefficient)
                                score_coefficient = util.round_sie(float(score_coefficient_tmp),
                                                                   self.get_sie_digits_certificate())
                                scores_array[x][num_columns - 2] = util.format_sie(prom, self.get_sie_digits())
                                scores_array[x][num_columns - 1] = util.format_sie(score_coefficient,
                                                                                   self.get_sie_digits_certificate())
                            else:
                                scores_array[x][num_columns - 2] = '--'
                                scores_array[x][num_columns - 1] = '--'

        else:
            scores_array = []
        return scores_array

    def get_detail_examen(self, num_child, scores_array_child, coefficient, title):
        num_columns = 0
        scores_array = []
        if num_child == 1:
            x = -2
            longitude = len(scores_array_child)
            for y in range(longitude):
                try:
                    if len(scores_array_child[y]) > 0:
                        x = y
                except:
                    if x == -2:
                        x = -1
            if x != -1:
                data = scores_array_child[x]
                num_students = len(data)
                longitude = len(data[x]) - 2
                num_columns = longitude + 1
                scores_array = [[0 for j in range(num_columns)] for i in range(num_students)]
                scores_array_prom = [[0 for j in range(1)] for i in range(num_students)]

                for x in range(num_students):
                    for y in range(longitude):
                        scores_array[x][y] = data[x][y]
                    if x == 0:
                        scores_array_prom[x][0] = title
                    else:
                        if data[x][y] == '--':
                            scores_array_prom[x][0] = '--'
                        else:
                            scores_array_prom[x][0] = decimal.Decimal(data[x][y])
                for x in range(num_students):
                    if x == 0:
                        scores_array[x][num_columns - 1] = scores_array_prom[x][0]
                    else:
                        if scores_array_prom[x][0] == '--':
                            scores_array[x][num_columns - 1] = '--'
                        else:
                            prom = util.round_sie(decimal.Decimal(scores_array_prom[x][0]), self.get_sie_digits())
                            scores_array[x][num_columns - 1] = util.format_sie(prom, self.get_sie_digits())

        elif num_child > 1:
            num_students = len(scores_array_child[0])
            for y in range(num_child):
                data = scores_array_child[y]
                num_columns += len(data[0])
            num_columns = num_columns - 6 * (num_child - 1) - 1
            scores_array = [[0 for j in range(num_columns)] for i in range(num_students)]
            scores_array_prom = [[0 for j in range(1)] for i in range(num_students)]
            position = 0
            for w in range(num_child):
                data = scores_array_child[w]
                longitude = len(data[0]) - 2

                if w == 0:
                    position = longitude
                    for x in range(num_students):
                        for y in range(longitude):
                            scores_array[x][y] = data[x][y]
                        if x == 0:
                            scores_array_prom[x][0] = title
                        else:
                            if data[x][y] == '--':
                                scores_array_prom[x][0] = '--'
                            else:
                                scores_array_prom[x][0] = decimal.Decimal(data[x][y])
                else:
                    z = 0
                    for x in range(num_students):
                        z = position
                        for y in range(longitude):
                            if y > 3:
                                scores_array[x][z] = data[x][y]
                                z += 1
                        if x == 0:
                            scores_array_prom[x][0] = title
                        else:
                            if data[x][y] != '--':
                                if scores_array_prom[x][0] != '--':
                                    scores_array_prom[x][0] += decimal.Decimal(data[x][y])
                            else:
                                data_0 = scores_array_child[w - 1]
                                y_0 = len(data_0[0]) - 2
                                if data_0[x][y_0] == '--':
                                    scores_array_prom[x][0] = data_0[x][y_0]
                                else:
                                    scores_array_prom[x][0] = decimal.Decimal(data_0[x][y_0])
                    position = z
            for x in range(num_students):
                if x == 0:
                    scores_array[x][num_columns - 1] = scores_array_prom[x][0]
                else:
                    if scores_array_prom[x][0] == '--':
                        scores_array[x][num_columns - 1] = '--'
                    else:
                        prom = util.round_sie(decimal.Decimal(scores_array_prom[x][0] / num_child),
                                              self.get_sie_digits())
                        scores_array[x][num_columns - 1] = util.format_sie(prom, self.get_sie_digits())

        else:
            scores_array = []
        return scores_array

    def get_detail_examen_vf(self, num_child, scores_array_child, coefficient, title):
        num_columns = 0
        scores_array = []
        if num_child == 1:
            x = -2
            longitude = len(scores_array_child)
            for y in range(longitude):
                try:
                    if len(scores_array_child[y]) > 0:
                        x = y
                except:
                    if x == -2:
                        x = -1
            if x != -1:
                data = scores_array_child[x]
                num_students = len(data)
                longitude = len(data[x]) - 2
                num_columns = longitude + 2
                scores_array = [[0 for j in range(num_columns)] for i in range(num_students)]
                scores_array_prom = [[0 for j in range(1)] for i in range(num_students)]

                for x in range(num_students):
                    for y in range(longitude):
                        scores_array[x][y] = data[x][y]
                    if x == 0:
                        scores_array_prom[x][0] = title
                    else:
                        if data[x][y] == '--':
                            scores_array_prom[x][0] = '--'
                        else:
                            scores_array_prom[x][0] = decimal.Decimal(data[x][y])
                for x in range(num_students):
                    if x == 0:
                        scores_array[x][num_columns - 2] = scores_array_prom[x][0]
                        scores_array[x][num_columns - 1] = '%s' % (coefficient)
                    else:
                        if scores_array_prom[x][0] == '--':
                            scores_array[x][num_columns - 2] = '--'
                            scores_array[x][num_columns - 1] = '--'
                        else:
                            prom = util.round_sie(decimal.Decimal(scores_array_prom[x][0]), self.get_sie_digits())
                            score_coefficient_tmp = prom * util.round_sie(coefficient,
                                                                          self.get_sie_digits_certificate())
                            score_coefficient = util.round_sie(float(score_coefficient_tmp),
                                                               self.get_sie_digits())
                            scores_array[x][num_columns - 2] = util.format_sie(prom, self.get_sie_digits())
                            scores_array[x][num_columns - 1] = util.format_sie(score_coefficient, self.get_sie_digits())

        elif num_child > 1:
            num_students = len(scores_array_child[0])
            for y in range(num_child):
                data = scores_array_child[y]
                num_columns += len(data[0])
            num_columns = num_columns - 6 * (num_child - 1)
            scores_array = [[0 for j in range(num_columns)] for i in range(num_students)]
            scores_array_prom = [[0 for j in range(1)] for i in range(num_students)]
            position = 0
            for w in range(num_child):
                data = scores_array_child[w]
                longitude = len(data[0]) - 2

                if w == 0:
                    position = longitude
                    for x in range(num_students):
                        for y in range(longitude):
                            scores_array[x][y] = data[x][y]
                        if x == 0:
                            scores_array_prom[x][0] = title
                        else:
                            if data[x][y] == '--':
                                scores_array_prom[x][0] = '--'
                            else:
                                scores_array_prom[x][0] = decimal.Decimal(data[x][y])
                else:
                    z = 0
                    for x in range(num_students):
                        z = position
                        for y in range(longitude):
                            if y > 3:
                                scores_array[x][z] = data[x][y]
                                z += 1
                        if x == 0:
                            scores_array_prom[x][0] = title
                        else:
                            if data[x][y] != '--':
                                if scores_array_prom[x][0] != '--':
                                    scores_array_prom[x][0] += decimal.Decimal(data[x][y])
                            else:
                                data_0 = scores_array_child[w - 1]
                                y_0 = len(data_0[0]) - 2
                                if data_0[x][y_0] == '--':
                                    scores_array_prom[x][0] = data_0[x][y_0]
                                else:
                                    scores_array_prom[x][0] = decimal.Decimal(data_0[x][y_0])
                    position = z
            for x in range(num_students):
                if x == 0:
                    scores_array[x][num_columns - 2] = scores_array_prom[x][0]
                    scores_array[x][num_columns - 1] = '%s' % (coefficient)
                else:
                    if scores_array_prom[x][0] == '--':
                        scores_array[x][num_columns - 2] = '--'
                        scores_array[x][num_columns - 1] = '--'
                    else:
                        prom = util.round_sie(decimal.Decimal(scores_array_prom[x][0]), self.get_sie_digits())
                        score_coefficient_tmp = prom * coefficient
                        score_coefficient = util.round_sie(float(score_coefficient_tmp),
                                                           self.get_sie_digits())
                        scores_array[x][num_columns - 2] = util.format_sie(prom, self.get_sie_digits())
                        scores_array[x][num_columns - 1] = util.format_sie(score_coefficient, self.get_sie_digits())

        else:
            scores_array = []
        return scores_array

    def get_detail_pu(self, scores_array_child, scores_array_child_ex, coefficient):
        num_columns = 0
        num_child = 0
        flag_child = 0
        flag_child_x = 0
        if scores_array_child:
            num_child += 1
            flag_child = 1
        if scores_array_child_ex:
            num_child += 1
            flag_child_x = 1
        if num_child == 1 and flag_child == 1:
            num_students = len(scores_array_child)
            num_columns += len(scores_array_child[0])
            num_columns = num_columns - 4 * (num_child - 1) + 1
            scores_array = [[0 for j in range(num_columns)] for i in range(num_students)]
            scores_array_prom = [[0 for j in range(1)] for i in range(num_students)]
            data = scores_array_child
            data = scores_array_child
            longitude = len(data[0]) - 1
            for x in range(num_students):
                for y in range(longitude):
                    scores_array[x][y] = data[x][y]
                if x == 0:
                    scores_array_prom[x][0] = 'PU'
                    scores_array[x][longitude - 1] = 'TRA'
                else:
                    if data[x][y] == '--':
                        scores_array_prom[x][0] = '--'
                    else:
                        scores_array_prom[x][0] = decimal.Decimal(data[x][y])
            for x in range(num_students):
                if x == 0:
                    scores_array[x][num_columns - 2] = scores_array_prom[x][0]
                    scores_array[x][num_columns - 1] = '%s' % (coefficient)
                else:
                    if scores_array_prom[x][0] == '--':
                        scores_array[x][num_columns - 2] = '--'
                        scores_array[x][num_columns - 1] = '--'
                    else:
                        prom = util.round_sie(decimal.Decimal(scores_array_prom[x][0] / num_child),
                                              self.get_sie_digits())
                        score_coefficient_tmp = prom * coefficient
                        score_coefficient = util.round_sie(float(score_coefficient_tmp),
                                                           self.get_sie_digits())
                        scores_array[x][num_columns - 2] = util.format_sie(prom, self.get_sie_digits())
                        scores_array[x][num_columns - 1] = util.format_sie(score_coefficient, self.get_sie_digits())
        elif num_child == 1 and flag_child_x == 1:
            num_students = len(scores_array_child_ex)
            num_columns += len(scores_array_child_ex[0])
            num_columns = num_columns + 2
            scores_array = [[0 for j in range(num_columns)] for i in range(num_students)]
            scores_array_prom = [[0 for j in range(1)] for i in range(num_students)]
            data = scores_array_child_ex
            data = scores_array_child_ex
            longitude = len(data[0])
            for x in range(num_students):
                for y in range(longitude):
                    scores_array[x][y] = data[x][y]
                if x == 0:
                    scores_array_prom[x][0] = 'PU'
                    # scores_array[x][longitude - 1] = 'EXA'
                else:
                    if data[x][y] == '--':
                        scores_array_prom[x][0] = '--'
                    else:
                        scores_array_prom[x][0] = decimal.Decimal(data[x][y])

            for x in range(num_students):
                if x == 0:
                    scores_array[x][num_columns - 2] = scores_array_prom[x][0]
                    scores_array[x][num_columns - 1] = '%s' % (coefficient)
                else:
                    if scores_array_prom[x][0] == '--':
                        scores_array[x][num_columns - 2] = '--'
                        scores_array[x][num_columns - 1] = '--'
                    else:
                        prom = util.round_sie(decimal.Decimal(scores_array_prom[x][0] / num_child),
                                              self.get_sie_digits())
                        score_coefficient_tmp = prom * coefficient
                        score_coefficient = util.round_sie(float(score_coefficient_tmp),
                                                           self.get_sie_digits())
                        scores_array[x][num_columns - 2] = util.format_sie(prom, self.get_sie_digits())
                        scores_array[x][num_columns - 1] = util.format_sie(score_coefficient, self.get_sie_digits())

        elif num_child == 2:
            num_students = len(scores_array_child)
            num_columns += len(scores_array_child[0])
            num_columns += len(scores_array_child_ex[0])
            num_columns = num_columns - 4 * (num_child - 1) + 1

            scores_array = [[0 for j in range(num_columns)] for i in range(num_students)]
            scores_array_prom = [[0 for j in range(1)] for i in range(num_students)]
            data = scores_array_child
            position = len(data[0]) - 2
            for w in range(num_child):
                if w == 0:
                    data = scores_array_child
                    longitude = len(data[0]) - 1
                else:
                    data = scores_array_child_ex
                    longitude = len(data[0])
                if w == 0:
                    for x in range(num_students):
                        for y in range(longitude):
                            scores_array[x][y] = data[x][y]
                        if x == 0:
                            scores_array_prom[x][0] = 'PU'
                            scores_array[x][longitude - 1] = 'TRA'
                        else:
                            if data[x][y] == '--':
                                scores_array_prom[x][0] = '--'
                            else:
                                scores_array_prom[x][0] = decimal.Decimal(data[x][y])
                else:
                    for x in range(num_students):
                        z = 1
                        for y in range(longitude):
                            if y > 3:
                                scores_array[x][position + z] = data[x][y]
                                z += 1
                        if x == 0:
                            scores_array_prom[x][0] = 'PU'
                        else:
                            if data[x][y] != '--':
                                if scores_array_prom[x][0] != '--':
                                    scores_array_prom[x][0] += decimal.Decimal(data[x][y])
                                else:
                                    scores_array_prom[x][0] = decimal.Decimal(data[x][y]) * 2
                            else:
                                if scores_array_prom[x][0] != '--':
                                    scores_array_prom[x][0] = scores_array_prom[x][0] * 2
                                else:
                                    scores_array_prom[x][0] = '--'

            for x in range(num_students):
                if x == 0:
                    scores_array[x][num_columns - 2] = scores_array_prom[x][0]
                    scores_array[x][num_columns - 1] = '%s' % (coefficient)
                else:
                    if scores_array_prom[x][0] == '--':
                        scores_array[x][num_columns - 2] = '--'
                        scores_array[x][num_columns - 1] = '--'
                    else:
                        prom = util.round_sie(decimal.Decimal(scores_array_prom[x][0] / num_child),
                                              self.get_sie_digits())
                        score_coefficient_tmp = prom * coefficient
                        score_coefficient = util.round_sie(float(score_coefficient_tmp),
                                                           self.get_sie_digits())
                        scores_array[x][num_columns - 2] = util.format_sie(prom, self.get_sie_digits())
                        scores_array[x][num_columns - 1] = util.format_sie(score_coefficient, self.get_sie_digits())


        else:
            scores_array = []
        return scores_array

    def get_summary_scores(self, scores_array_child, coefficient, title):
        num_columns = 10
        num_students = len(scores_array_child[0])

        scores_array = [[0 for j in range(num_columns)] for i in range(num_students)]
        scores_array_prom = [[0 for j in range(1)] for i in range(num_students)]
        data = scores_array_child[0]

        position = len(data[0]) - 1
        for w in range(len(scores_array_child)):
            data = scores_array_child[w]
            longitude = len(data[0])
            if w == 0:
                for x in range(num_students):
                    for y in range(longitude):
                        scores_array[x][y] = data[x][y]
                    if x == 0:
                        scores_array_prom[x][0] = title
                    else:
                        if data[x][y] == '--':
                            scores_array_prom[x][0] = '--'
                        else:
                            scores_array_prom[x][0] = decimal.Decimal(data[x][y])
            else:
                for x in range(num_students):
                    z = 1
                    for y in range(longitude):
                        if y > 3:
                            scores_array[x][position + z] = data[x][y]
                            z += 1
                    if x == 0:
                        scores_array_prom[x][0] = title
                    else:
                        if data[x][y] != '--':
                            if scores_array_prom[x][0] != '--':
                                scores_array_prom[x][0] += decimal.Decimal(data[x][y])
                            else:
                                scores_array_prom[x][0] = decimal.Decimal(data[x][y - 1])
                        else:
                            data_0 = scores_array_child[w - 1]
                            y_0 = len(data_0[0]) - 2
                            if data_0[x][y_0] == '--':
                                scores_array_prom[x][0] = data_0[x][y_0]
                            else:
                                scores_array_prom[x][0] = decimal.Decimal(data_0[x][y_0])
        for x in range(num_students):
            if x == 0:
                scores_array[x][num_columns - 2] = title
                scores_array[x][num_columns - 1] = '%s' % (coefficient)
            else:
                if scores_array_prom[x][0] == '--':
                    scores_array[x][num_columns - 2] = '--'
                    scores_array[x][num_columns - 1] = '--'
                else:
                    prom = util.round_sie(decimal.Decimal(scores_array_prom[x][0]), self.get_sie_digits())
                    score_coefficient_tmp = prom * coefficient
                    score_coefficient = util.round_sie(float(score_coefficient_tmp),
                                                       self.get_sie_digits())
                    scores_array[x][num_columns - 2] = util.format_sie(prom, self.get_sie_digits())
                    scores_array[x][num_columns - 1] = util.format_sie(score_coefficient, self.get_sie_digits())

        return scores_array

    def get_summary_scores_final(self, scores_array_child, child):

        cant = len(scores_array_child)
        num_columns = 6 + cant
        for w in range(cant):
            num_students = len(scores_array_child[w])
            if num_students > 0:
                break
        title = 'P.FINAL'
        if num_students > 0:
            scores_array = [[0 for j in range(num_columns)] for i in range(num_students)]
            for x in range(num_students):
                for y in range(cant):
                    scores_array[x][4 + cant] = '0.00'

            scores_array_prom = [[0 for j in range(1)] for i in range(num_students)]
            for x in range(num_students):
                scores_array[x][0] = '0.00'

            for w in range(cant):
                position = 0
                data = scores_array_child[w]
                if data:
                    position = len(data[0]) - 1
                if position > 0:
                    break

            for w in range(cant):
                data = scores_array_child[w]
                if data:
                    longitude = len(data[0])
                    if w == 0:
                        for x in range(num_students):
                            for y in range(longitude):
                                scores_array[x][y] = data[x][y]
                            if x == 0:
                                scores_array_prom[x][0] = title
                            else:
                                if data[x][y] == '--':
                                    scores_array_prom[x][0] = '--'
                                else:
                                    scores_array_prom[x][0] = decimal.Decimal(data[x][y])
                    else:
                        for x in range(num_students):
                            z = w
                            for y in range(longitude):
                                if y > 3:
                                    scores_array[x][position + z] = data[x][y]
                                    z += 1
                            if x == 0:
                                scores_array_prom[x][0] = title
                            else:
                                if data[x][y] == '--':
                                    if scores_array_prom[x][0] == '--':
                                        scores_array_prom[x][0] == data[x][y]
                                else:
                                    if scores_array_prom[x][0] == '--':
                                        scores_array_prom[x][0] = decimal.Decimal(data[x][y])
                                    else:
                                        scores_array_prom[x][0] += decimal.Decimal(data[x][y])

            for x in range(num_students):
                if x == 0:
                    scores_array[x][num_columns - 2] = title
                    scores_array[x][num_columns - 1] = 'Antig'
                else:
                    if scores_array_prom[x][0] == '--':
                        scores_array[x][num_columns - 2] = '--'
                        scores_array[x][num_columns - 1] = '--'
                    else:
                        prom = util.round_sie(decimal.Decimal(scores_array_prom[x][0]),
                                              self.get_sie_digits_certificate())
                        scores_array[x][num_columns - 2] = util.format_sie(prom, self.get_sie_digits())
                        scores_array[x][num_columns - 1] = '--'

            scores_array_final = self.get_summary_array_antiquity_with_title(scores_array, child, cant)
        else:
            scores_array_final = []
        return scores_array_final

    def get_summary_array_antiquity(self, data=None):
        num_students = len(data)
        longitude = len(data[0])
        scores_array = [[0 for j in range(longitude)] for i in range(num_students)]
        antiquity = 1
        for x in range(num_students):
            for y in range(longitude):
                scores_array[x][y] = data[x][y]
            scores_array[x][longitude - 1] = '%s' % antiquity
            antiquity += 1
        return scores_array

    def get_summary_array_antiquity_with_title(self, data, child, cant):
        num_students = len(data)
        longitude = len(data[0])
        scores_array = [[0 for j in range(longitude)] for i in range(num_students - 1)]
        scores_array_final = [[0 for j in range(longitude)] for i in range(num_students)]
        a = -1
        for x in range(num_students):
            b = 0
            for y in range(longitude):
                if x != 0:
                    scores_array[a][b] = data[x][y]
                    b += 1
            a += 1
        scores_array, scores_array_foreign = self.remove_foreign(scores_array, self.course_id)
        scores_array_sort = sorted(scores_array, key=lambda x: x[longitude - 2], reverse=True)
        scores_array_tmp = self.get_summary_array_antiquity(scores_array_sort)
        z = 0
        flag = False
        for x in range(num_students):
            for y in range(longitude):
                if x == 0:
                    if y == 0:
                        scores_array_final[x][0] = 'No'
                    elif y == 1:
                        scores_array_final[x][1] = 'Grado'
                    elif y == 2:
                        scores_array_final[x][2] = 'Nombre'
                    elif y == 3:
                        scores_array_final[x][3] = 'Id'
                    elif y == (3 + cant + 1):
                        scores_array_final[x][y] = 'Promedio Final'
                    elif y == (3 + cant + 2):
                        scores_array_final[x][y] = 'Antiguedad'
                    else:
                        coefficient = '%s' % child[y - 4].coefficient
                        title = child[y - 4].name.title()
                        scores_array_final[x][y] = '%s %s' % (title, coefficient.replace('.', ','))
                else:
                    if x <= len(scores_array_tmp):
                        scores_array_final[x][y] = scores_array_tmp[x - 1][y]
                    else:
                        scores_array_final[x][y] = scores_array_foreign[z][y]
                        flag = True
            if flag:
                flag = False
                z += 1

        return scores_array_final

    def get_sort_array(self, data):
        try:
            num_students = len(data)
            longitude = len(data[0])
            scores_array = [[0 for j in range(longitude)] for i in range(num_students - 1)]
            scores_array_final = [[0 for j in range(longitude)] for i in range(num_students)]
            a = -1
            for x in range(num_students):
                b = 0
                for y in range(longitude):
                    if x != 0:
                        scores_array[a][b] = data[x][y]
                        b += 1
                a += 1

            scores_array_sort = sorted(scores_array, key=lambda x: x[2], reverse=False)
            a = 1
            for x in range(num_students):
                for y in range(longitude):
                    if x == 0:
                        scores_array_final[x][y] = data[x][y]
                    else:
                        if y == 0:
                            scores_array_final[x][y] = '%s' % a
                            a += 1
                        else:
                            scores_array_final[x][y] = scores_array_sort[x - 1][y]
        except:
            scores_array_final = []
        return scores_array_final

    def get_summary_array_2column(self, data):
        num_students = len(data)
        longitude = len(data[0])
        scores_array = [[0 for j in range(6)] for i in range(num_students)]
        for x in range(num_students):
            for y in range(4):
                scores_array[x][y] = data[x][y]
            scores_array[x][4] = data[x][longitude - 2]
            scores_array[x][5] = data[x][longitude - 1]
        return scores_array

    def get_summary_array_1column(self, data):
        num_students = len(data)
        longitude = len(data[0])
        scores_array = [[0 for j in range(5)] for i in range(num_students)]
        for x in range(num_students):
            for y in range(4):
                scores_array[x][y] = data[x][y]
            scores_array[x][4] = data[x][longitude - 1]
        return scores_array

    def remove_foreign_print(self, data, course_id):
        foreign_students = self.get_enrollment(course_id).student_ids.filtered("guest"). \
            filtered(lambda r: r.inactive == False)
        foreign = []
        if foreign_students:
            longitude_students = len(foreign_students)
            foreign = [0 for j in range(longitude_students)]
            a = 0
            for student in foreign_students:
                foreign[a] = str(student.id)
                a += 1
        else:
            longitude_students = 0
        if data:
            num_students = len(data)
            longitude = len(data[0])
            scores_array = [[0 for j in range(longitude)] for i in range(num_students - longitude_students)]
            a = 0
            for x in range(num_students):
                b = 0
                flag = False
                for y in range(longitude):
                    flag = data[x][3] in foreign
                    if not flag:
                        if x == 0:
                            scores_array[a][b] = data[x][y]
                        else:
                            scores_array[a][b] = data[x][y]
                        b += 1
                if not flag:
                    a += 1
        else:
            scores_array = []
        return scores_array

    def only_foreign_print(self, data, course_id):
        foreign_students = self.get_enrollment(course_id).student_ids.filtered("guest"). \
            filtered(lambda r: r.inactive == False)
        foreign = []
        if foreign_students:
            longitude_students = len(foreign_students)
            foreign = [0 for j in range(longitude_students)]
            a = 0
            for student in foreign_students:
                foreign[a] = str(student.id)
                a += 1
        else:
            longitude_students = 0
        if data:
            num_students = len(data)
            longitude = len(data[0])
            scores_array = [[0 for j in range(longitude)] for i in range(longitude_students + 1)]
            a = 0
            for x in range(num_students):
                b = 0
                flag = False
                for y in range(longitude):
                    if x == 0:
                        scores_array[a][b] = data[x][y]
                        b += 1
                        flag = True
                    else:
                        flag = data[x][3] in foreign
                        if flag:
                            scores_array[a][b] = data[x][y]
                            b += 1
                if flag:
                    a += 1
        else:
            scores_array = []

        return scores_array

    def remove_foreign(self, data, course_id):
        foreign_students = self.get_enrollment(str(course_id)).student_ids.filtered("guest"). \
            filtered(lambda r: r.inactive == False)
        foreign = []
        if foreign_students:
            longitude_students = len(foreign_students)
            foreign = [0 for j in range(longitude_students)]
            a = 0
            for student in foreign_students:
                foreign[a] = str(student.id)
                a += 1
        else:
            longitude_students = 0
        if data:
            num_students = len(data)
            longitude = len(data[0])
            scores_array = [[0 for j in range(longitude)] for i in range(num_students - longitude_students)]
            scores_array_foreign = [[0 for j in range(longitude)] for i in range(longitude_students)]
            a = 0
            a1 = 0
            for x in range(num_students):
                b = 0
                b1 = 0
                flag = False
                for y in range(longitude):
                    flag = data[x][3] in foreign
                    if not flag:
                        if x == 0:
                            scores_array[a][b] = data[x][y]
                        else:
                            scores_array[a][b] = data[x][y]
                        b += 1
                    else:
                        scores_array_foreign[a1][b1] = data[x][y]
                        b1 += 1
                if not flag:
                    a += 1
                else:
                    a1 += 1
        else:
            scores_array = []
            scores_array_foreign = []

        return scores_array, scores_array_foreign

    def get_scores_array_without_prom(self, data):
        if data:
            num_students = len(data)
            longitude = len(data[0])
            scores_array = [[0 for j in range(longitude - 2)] for i in range(num_students)]
            for x in range(num_students):
                for y in range(longitude - 2):
                    scores_array[x][y] = '--'
            for x in range(num_students):
                for y in range(longitude - 2):
                    scores_array[x][y] = data[x][y]
        else:
            scores_array = []
        return scores_array

    def get_scores_array_without_id(self, data, student_id=None):
        if student_id:
            scores_array = self.get_scores_array_without_id_student(data, student_id)
        else:
            if data:
                num_students = len(data)
                longitude = len(data[0])
                scores_array = [[0 for j in range(longitude - 1)] for i in range(num_students)]
                for x in range(num_students):
                    for y in range(longitude - 1):
                        scores_array[x][y] = '--'
                a = 0
                for x in range(num_students):
                    b = 0
                    for y in range(longitude):
                        if y != 3:
                            if x == 0:
                                value = data[x][y]
                                if value == 0:
                                    scores_array[a][b] = '--'
                                else:
                                    scores_array[a][b] = data[x][y]
                            else:
                                value = data[x][y]
                                if value == 0:
                                    # TODO: septiembre 2016
                                    scores_array[a][b] = '--'
                                else:
                                    scores_array[a][b] = (u'%s' % value).replace('.', ',')
                            b += 1
                    a += 1
            else:
                scores_array = []
        return scores_array

    def get_scores_array_without_id_student(self, data, student_id):
        if data:
            index = -1
            num_students = len(data)
            longitude = len(data[0])
            for x in range(num_students):
                if data[x][3] == student_id:
                    index = x
            scores_array = [[0 for j in range(longitude - 1)] for i in range(2)]
            if x > -1:
                a = 0
                flag = False
                for x in range(num_students):
                    b = 0
                    for y in range(longitude):
                        if y != 3:
                            if x == 0:
                                scores_array[a][b] = data[x][y]
                                flag = True
                            else:
                                if x == index:
                                    scores_array[a][b] = ('%s' % data[x][y]).replace('.', ',')
                                    flag = True
                            b += 1
                    if flag:
                        a += 1
                        flag = False
            else:
                scores_array = []
        else:
            scores_array = []
        return scores_array

    def get_scores_array_without_index(self, data, course_state=None, student_id=None):
        if data:
            extra_line = 2
            num_students = len(data)
            line_1 = 0
            line_2 = 0
            count = (num_students - 1) // 3
            z = (num_students - 1) % 3
            if count == 0:
                extra_line = 0
            else:
                if z == 2:
                    line_1 = count + 2
                    line_2 = line_1 + count + 2
                elif z == 0:
                    line_1 = count + 1
                    line_2 = line_1 + count + 1
                else:
                    line_1 = count + 2
                    line_2 = line_1 + count + 1

            longitude = len(data[0])
            scores_array = [[0 for j in range(longitude - 1)] for i in range(num_students + extra_line)]
            flag = False
            a = 0
            w = 0
            for x in range(num_students + extra_line):
                b = 0
                for y in range(longitude):
                    if y != 0:
                        if x != 0 and ((x == line_1) or (x == line_2)):
                            if w < 2:
                                scores_array[a][b] = ' '
                                flag = True
                            else:
                                scores_array[a][b] = data[x - w][y]
                                flag = False
                        else:
                            if w == 0:
                                scores_array[a][b] = data[x][y]
                            else:
                                index = x - w
                                if index < num_students:
                                    scores_array[a][b] = data[index][y]
                                else:
                                    scores_array[a][b] = ' '
                        b += 1
                a += 1
                if flag:
                    flag = False
                    w += 1
                    # if course_state != "finalized" and student_id:
                    #     num_students = len(scores_array)
                    #     columns = len(scores_array[0])
                    #     for x in range(num_students):
                    #         for y in range(columns):
                    #             if y == columns-1 and x != 0:
                    #                 scores_array[x][y] = '--'
        else:
            scores_array = []

        return scores_array

    def get_initials_course(self, course_name):
        initials_array = course_name.split(' ')
        initials = ''
        value = len(initials_array)

        for data in initials_array:
            if value == 1:
                initials = data[0] + data[1]
            else:
                initials += data[0]
        return initials

    def re_number(self, scores_array):
        num_students = len(scores_array)
        for x in range(num_students):
            if x == 0:
                scores_array[x][0] = 'No.'
            else:
                scores_array[x][0] = x
        return scores_array
