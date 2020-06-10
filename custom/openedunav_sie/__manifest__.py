# -*- coding: utf-8 -*-
###############################################################################
#
#    Manexware S.A.
#    Copyright (C) 2009-TODAY Manexware
#
# noinspection PyStatementEffect
###############################################################################


{
    'name': 'OpenEduNav SIE',
    'version': '13.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Students, Faculties and Education Institute',
    'complexity': "easy",
    'author': 'Manexware S.A.',
    'website': 'http://www.manexware.com',
    'depends': [
        'openeducat_core',
        'openeducat_classroom',
        'openeducat_cescan',
        'openeducat_register',
        'openeducat_timekeeping',
        'openeducat_score',
        'openeducat_report',
        'web_openedunav',
    ],
    'images': [
        'static/description/openedunav_sie_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
