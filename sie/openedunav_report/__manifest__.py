# -*- coding: utf-8 -*-
###############################################################################
#
#    Manexware S.A.
#    Copyright (C) 2009-TODAY Manexware
#
#   noinspection PyStatementEffect
#
###############################################################################

{
    'name': 'OpenEduNav Reports',
    'version': '13.0.0.1',
    'author': 'Manexware S.A.',
    'category': 'Education',
    'website': 'http://www.manexware.com',
    'depends': [
        'openedunav_core',
        'openedunav_classroom',
        'openedunav_score',
        'openedunav_timekeeping',
        'mail',
        'report_py3o'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/certificate_wizard_view.xml',
        'wizard/certificate_evaluation_wizard_view.xml',
        'wizard/integrator_product_wizard_view.xml',
        'wizard/integrator_product_student_wizard_view.xml',
        'wizard/subject_wizard_view.xml',
        'wizard/score_wizard_view.xml',
        'wizard/score_student_wizard_view.xml',
        'wizard/score_professor_wizard_view.xml',
        'views/report_score_act.xml',
        'views/report_subject_act.xml',
        'report/student.xml',
        # 'report/score_act_layout.xml',
        'report/certificado_evaluacion.xml',
        'views/report_menu.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

