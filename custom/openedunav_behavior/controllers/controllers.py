# -*- coding: utf-8 -*-
from odoo import http

# class OpenedunavBehavior(http.Controller):
#     @http.route('/openedunav_behavior/openedunav_behavior/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/openedunav_behavior/openedunav_behavior/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('openedunav_behavior.listing', {
#             'root': '/openedunav_behavior/openedunav_behavior',
#             'objects': http.request.env['openedunav_behavior.openedunav_behavior'].search([]),
#         })

#     @http.route('/openedunav_behavior/openedunav_behavior/objects/<model("openedunav_behavior.openedunav_behavior"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('openedunav_behavior.object', {
#             'object': obj
#         })