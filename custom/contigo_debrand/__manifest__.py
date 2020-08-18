# -*- coding: utf-8 -*-
###############################################################################
#
#    Manexware S.A.
#    Copyright (C) 2009-TODAY Manexware
#
# noinspection PyStatementEffect
###############################################################################
{
    "name": "Contigo Debrand",
    "summary": "Remove enterprise modules and setting items",
    "version": "13.0.1.0.1",
    "category": "Maintenance",
    "author": "Manexware S.A.",
    "website": "https://manexware.com",
    "license": "AGPL-3",
    "depends": ['web',
                'mail',
                'portal',
                ],
    "external_dependencies": {"python": ["lxml"]},
    'data': [
        'views/res_config_view.xml',
        'views/web_client_template.xml',
        'views/portal_templates.xml',
        'views/templates.xml',
        'data/data.xml',
    ],
    "qweb": [
        'static/src/xml/base.xml',
        'static/src/xml/client_action.xml',
        'static/src/xml/dashboard.xml',
    ],
    "images":  ['static/description/Banner.png'],
    "application":  True,
    "installable":  True,
    "auto_install":  False,
}
