# -*- coding: utf-8 -*-
###############################################################################
#
#    Manexware S.A.
#    Copyright (C) 2009-TODAY Manexware
#
# noinspection PyStatementEffect
###############################################################################

{
    'name': 'OpenEduNav Conduct',
    'version': '13.0.0.1',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Conduct',
    'complexity': "easy",
    'description': """

    """,
    'author': 'Manexware S.A.',
    'website': 'http://www.manexware.com',
    'depends': ['openedunav_core'],
    'data': [
        # 'security/sie_conduct_security.xml',
        'views/award_view.xml',
        'views/exempt_kind_view.xml',
        'views/fault_article_view.xml',
        'views/fault_classification_view.xml',
        'views/fault_kind_view.xml',
        'views/fault_literal_view.xml',
        'views/fault_sanction_view.xml',
        'views/medal_kind_view.xml',
        'views/medical_leave_view.xml',
        'views/merit_control_view.xml',
        'views/merit_view.xml',
        'views/sanction_control_view.xml',
        # 'menu/conduct_menu.xml',
        # 'security/ir.model.access.csv'
    ],
    'demo': [
    ],
    'images': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
