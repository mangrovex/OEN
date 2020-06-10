# -*- coding: utf-8 -*-
# Copyright (C) Manexware 2020
# noinspection PyStatementEffect
{
    'name': 'Base Ecuador',
    'version': '13.0',
    'author': 'Manexware',
    'category': 'Generic Modules/Base',
    'summary': 'Ecuador Modificaciones a res_partner, res_company y res_users',
    'license': 'LGPL-3',
    'contributors': [
        'Manuel Vega <manuel.vega@manexware.com>',
    ],
    'website': 'http://manexware.com',
    'depends': ['contacts'],
    'data': [
        'security/security.xml',
        'data/paperformat_data.xml',
        'data/res_country_data.xml',
        'data/partner_data.xml',
        'data/sequence_data.xml',
        'data/res_country_state.xml',
        'data/res_state_city.xml',
        'data/res_city_parish.xml',
        'data/res_country.xml',
        'data/res_bank_data.xml',
        'data/res_store_data.xml',
        'data/config_parameter_data.xml',
        'views/menu.xml',
        'views/res_partner_views.xml',
        'views/res_company_views.xml',
        'views/res_users_views.xml',
        'views/res_state_city_views.xml',
        'views/res_city_parish_views.xml',
        'views/res_country_views.xml',
        'views/res_store_view.xml',
        'views/res_bank_views.xml',
        'views/report_template.xml',

        'security/ir.model.access.csv'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
