# -*- coding: utf-8 -*-
# Copyright (C) Manexware 2020
# noinspection PyStatementEffect
{
    'name': 'Base Location',
    'version': '13.0',
    'author': 'Manexware',
    'category': 'Generic Modules/Base',
    'summary': 'Modificaciones a res_partner',
    'license': 'LGPL-3',
    'contributors': [
        'Manuel Vega <manuel.vega@manexware.com>',
    ],
    'website': 'http://manexware.com',
    'depends': ['contacts'],
    'data': [
        'data/res_country_data.xml',
        'data/res_country_state.xml',
        'data/res_state_city.xml',
        'data/res_city_parish.xml',
        'data/res_country.xml',
        'views/res_partner_views.xml',
        'views/res_state_city_views.xml',
        'views/res_city_parish_views.xml',
        'views/res_country_views.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
