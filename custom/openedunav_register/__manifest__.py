# -*- coding: utf-8 -*-
###############################################################################
#
#    Manexware S.A.
#    Copyright (C) 2009-TODAY Manexware
#
# noinspection PyStatementEffect
###############################################################################

{
    'name': 'OpenEduNav Register',
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
        'views/register_subject_views.xml',
        'views/register_directors_views.xml',
        'views/register_seminary_views.xml',
        'menu/sie_menu.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': False,
}
