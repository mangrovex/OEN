# -*- coding: utf-8 -*-
###############################################################################
#
#    Manexware S.A.
#    Copyright (C) 2009-TODAY Manexware
#
#    noinspection PyStatementEffect
#
###############################################################################

{
    'name': "OpenEduNav Behavior",
    'summary': """
        Módulo para la calificación de la conducta de los estudiantes
        de los cursos impartidos por ESCAPE.
        """,
    'description': """
        Módulo para la calificación de la conducta de los estudiantes
        de los cursos impartidos por ESCAPE.
    """,
    'author': "Manexware S.A.",
    'website': "http://manexware.com",
    'category': 'Educacion',
    'version': '13.0.0.1',
    'depends': ['openedunav_core'],
    'data': [
        # 'security/ir.model.access.csv',
        'menu/behavior_menu.xml',
        'views/views.xml',
        'views/news_views.xml',
        'views/templates.xml',
        'views/license_views.xml',
        'views/brigadier_note_views.xml',
        'views/report_behavior_view.xml',
        'views/aspects_views.xml',
        'report/report_behavior_py3o.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}