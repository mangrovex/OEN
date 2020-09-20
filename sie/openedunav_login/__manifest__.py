# -*- encoding: utf-8 -*-
###################################################################################
#
#    Copyright (c) 2017-2019 Manexware S.A.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#    noinspection PyStatementEffect
#
###################################################################################
{
    'name': 'Odoo Web Login Screen',
    'summary': 'The new configurable Odoo Web Login Screen',
    'version': '13.0.1.0',
    'category': 'Website',
    'author': "Manexware S.A.",
    'website': "https://www.xaoxao.vn",
    'license': 'AGPL-3',
    'depends': [
    ],
    'data': [
        'data/ir_config_parameter.xml',
        'templates/website_templates.xml',
        'templates/webclient_templates.xml',
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'images': ['static/description/banner.png'],
}
