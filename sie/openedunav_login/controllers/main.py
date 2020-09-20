# -*- encoding: utf-8 -*-

import ast
from addons.web.controllers.main import Home
import pytz
import datetime
import logging

import odoo
import odoo.modules.registry
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


# ----------------------------------------------------------
# Odoo Web web Controllers
# ----------------------------------------------------------
class LoginHome(Home):

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        param_obj = request.env['ir.config_parameter'].sudo()
        request.params['disable_footer'] = ast.literal_eval(param_obj.get_param('login_form_disable_footer')) or False
        request.params['disable_database_manager'] = ast.literal_eval(
            param_obj.get_param('login_form_disable_database_manager')) or False

        request.params['background_src'] = param_obj.get_param(
            'login_form_background_default') or '/openedunav_login/static/src/img/openedunav.png'
        return super(LoginHome, self).web_login(redirect, **kw)
