# -*- coding: utf-8 -*-
###############################################################################
#
#    Manexware S.A.
#    Copyright (C) 2009-TODAY Manexware
#
# noinspection PyStatementEffect
###############################################################################

{
    'name': 'OpenEduNav Physical Proof',
    'version': '13.0.0.1',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Physical Proof',
    'complexity': "easy",
    'description': """

    """,
    'author': 'Ing. Ingrid Chilan.',
    'website': 'http://www.manexware.com',
    'depends': ['openedunav_escape'],
    'data': [
        'security/sie_physical_proof_security.xml',
        'views/physical_proof_param_view.xml',
        'views/physical_proof_score_view.xml',
        'views/physical_proof_table_view.xml',
        'views/physical_proof_test_view.xml',
        'views/physical_proof_view.xml',
        'report/physical_proof.xml',
        'menu/physical_proof_menu.xml',
        'security/ir.model.access.csv'
    ],
    'demo': [
    ],
    'images': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
