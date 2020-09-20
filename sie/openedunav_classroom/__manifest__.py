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
    'summary': 'Classroom',
    'depends': [
        'openedunav_core',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/openedunav_code.xml',
        'views/promotion_course_views.xml',
        'views/knowledge_views.xml',
        'views/module_views.xml',
        'views/content_views.xml',
        'views/course_views.xml',
        'views/faculty_views.xml',
        'views/course_name_views.xml',
        'views/enrollment_views.xml',
        'views/attachment_views.xml',
        'views/student_views.xml',
        'views/register_subject_views.xml',
        'views/register_directors_views.xml',
        'views/register_seminary_views.xml',
        'views/concept_views.xml',
        'views/training_shaft_views.xml',
        'views/param_name_views.xml',
        'views/matrix_parameter_views.xml',
        'views/matrix_views.xml',
        'data/concepts_data.xml',
        'data/training_shaft_data.xml',
        'data/matrix_parameter_name_data.xml',
        'data/promotion_course_data.xml',
        'data/course_name_data.xml',
        'views/sie_menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
