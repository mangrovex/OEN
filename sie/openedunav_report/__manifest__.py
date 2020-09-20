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
    'name': 'OpenEduNav Reports CESCAN',
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
        'wizard/score_content_report_wizard_view.xml',
        'wizard/score_knowledge_report_wizard_view.xml',
        'views/report_menu.xml',
        'report/score_content.xml',
        'report/score_knowledge.xml',
        # 'report/cescan_report.xml',

    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

