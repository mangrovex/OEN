# -*- coding: utf-8 -*-
###############################################################################
#
#    Manexware S.A.
#    Copyright (C) 2009-TODAY Manexware
#
# noinspection PyStatementEffect
###############################################################################

{
    'name': 'OpenEduNav CESCAN',
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
        'wizard/integrator_product_wizard_view.xml',
        'wizard/integrator_product_student_wizard_view.xml',
        'views/concept_views.xml',
        'views/param_name_views.xml',
        'views/matrix_parameter_views.xml',
        'views/matrix_views.xml',
        'views/integrator_product_views.xml',
        'data/concepts_data.xml',
        'data/training_shaft_data.xml',
        'data/matrix_parameter_name_data.xml',
        'data/matrix_data.xml',
        'data/matrix_param_data.xml',
        'menu/sie_menu.xml'
    ],

    'installable': True,
    'auto_install': False,
    'application': False,
}
