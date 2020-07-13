# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from addons.web.controllers.main import ReportController
from odoo.http import route, request, Controller, content_disposition
from odoo.tools import html_escape, sys, traceback
import json
from werkzeug import url_decode


class OpenedunavDownloadController(ReportController):
    @route(['/report/download'])
    def report_download(self, data, token):
        response = super(OpenedunavDownloadController, self).report_download(data, token)
        # if we got another content disposition before, ditch the one added
        # by super()
        requestcontent = json.loads(data)
        url, type = requestcontent[0], requestcontent[1]
        try:
            if type == 'qweb-pdf':
                reportname = url.split('/report/pdf/')[1].split('?')[0]
                docids = None
                if '/' in reportname:
                    reportname, docids = reportname.split('/')
                if not docids:
                    cr, uid = request.cr, request.uid
                    report = request.registry['report']._get_report_from_name(cr, uid, reportname)
                    data = dict(url_decode(url.split('?')[1]).items())
                    data = json.loads(data.pop('options'))
                    response.headers['Content-Disposition'] = content_disposition(data['download_name'])
                    return response
        except Exception as e:
            exc_info = sys.exc_info()
            se = traceback.format_exception(*exc_info)
            error = {
                'code': 200,
                'message': "Odoo Server Error",
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))
        return response
