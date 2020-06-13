# -*- coding: utf-8 -*-
###############################################################################
#
#    Manexware S.A.
#    Copyright (C) 2009-TODAY Manexware
#
# noinspection PyStatementEffect
###############################################################################

{
    'name': 'OpenEduNav Classroom',
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
    'demo': [

    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/subject_wizard_view.xml',
        'views/promotion_course_views.xml',
        'views/subject_unit_views.xml',
        'views/subject_views.xml',
        'views/subject_content_views.xml',
        'views/course_views.xml',
        'views/faculty_views.xml',
        'views/course_name_views.xml',
        'views/enrollment_views.xml',
        'views/attachment_views.xml',
        'views/student_views.xml',
        'data/promotion_course_data.xml',
        'data/course_name_data.xml',
        'menu/sie_menu.xml',

    ],

    'installable': True,
    'auto_install': False,
    'application': False,
}
