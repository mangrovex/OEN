# -*- coding: utf-8 -*-
###############################################################################
#
#    Manexware S.A.
#    Copyright (C) 2009-TODAY Manexware
#
# noinspection PyStatementEffect
###############################################################################

{
    'name': 'OpenEduNav Score',
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
    'images': [],
    'depends': ['openedunav_core',
                ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/score_wizard_view.xml',
        'wizard/score_student_wizard_view.xml',
        'wizard/score_professor_wizard_view.xml',
        'views/score_views.xml',
        'views/score_statistician.xml',
        'views/course_score_views.xml',
        'menu/sie_menu.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': False,
}
