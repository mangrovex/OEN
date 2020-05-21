# -*- coding: utf-8 -*-
# Copyright 2020 Manexware
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Material Backend Theme V13",
    "summary": "Material Backend Theme V13",
    "version": "13.0.0.1",
    "category": "Theme/Backend",
    "website": "http://www.manexware.com",
	"description": """
		Material Backend theme for Odoo 13.0 community edition.
    """,
	'images':[
        'images/screen.png'
	],
    "author": "Manuel Vega",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        'web',
        'web_responsive',
    ],
    "data": [
        'views/assets.xml',
		'views/res_company_view.xml',
        'views/res_config_settings_views.xml'
		#'views/users.xml',
        #'views/sidebar.xml',
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
}

