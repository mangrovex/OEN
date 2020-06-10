# -*- coding: utf-8 -*-
###############################################################################
#
#    Manexware S.A.
#    Copyright (C) 2009-TODAY Manexware
#
# noinspection PyStatementEffect
###############################################################################

{
    'name': 'OpenEduNav Reports',
    'version': '13.0.0.1',
    'author': 'Manexware S.A.',
    'category': 'Education',
    'website': 'http://www.manexware.com',
    'summary': '',
    'description': """
        Training Institutes.
        ================================

        You can manage:
        ---------------
        * Learning Techniques
        * Training Shafts
        * Subjects
        * Courses

        """,
    'css': [],
    'qweb': [],
    'summernote': [],
    'images': [],
    'depends': ['openedunav_core',
                'openedunav_cescan',
                'mail',
                'report_py3o'
                ],
    'demo': [

    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/certificate_wizard_view.xml',
        'wizard/certificate_evaluation_wizard_view.xml',
        'views/report_score_act.xml',
        'views/report_subject_act.xml',
        'report/student.xml',
        # 'report/score_act_layout.xml',
        'report/certificado_evaluacion.xml',
        'menu/report_menu.xml'
    ],

    'installable': True,
    'auto_install': False,
    'application': False,
}

