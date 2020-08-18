# -*- coding: utf-8 -*-
###############################################################################
#
#    Manexware S.A.
#    Copyright (C) 2009-TODAY Manexware
#
# noinspection PyStatementEffect
###############################################################################

{
    'name': 'OpenEduNav Timekeeping',
    'version': '13.0.0.1',
    'author': 'Manexware S.A.',
    'category': 'Education',
    'website': 'http://www.manexware.com',
    'summary': 'Timekeeping',
    'depends': [
        'openedunav_core',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/timekeeping_views.xml',
        'views/timekeeping_calc_views.xml',
        'views/sie_menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
