# -*- coding: utf-8 -*-

import base64
import io
import os
from random import randrange

from PIL import Image
from odoo import api, models, tools
from odoo.modules.module import get_resource_path


class ResCompany(models.Model):
    _inherit = 'res.company'

    def _get_default_favicon(self, original=False):
        img_path = get_resource_path('contigo_debrand', 'static/src/img/favicon.ico')
        with tools.file_open(img_path, 'rb') as f:
            if original:
                return base64.b64encode(f.read())
            # Modify the source image to add a colored bar on the bottom
            # This could seem overkill to modify the pixels 1 by 1, but
            # Pillow doesn't provide an easy way to do it, and this
            # is acceptable for a 16x16 image.
            color = (randrange(32, 224, 24), randrange(32, 224, 24), randrange(32, 224, 24))
            original = Image.open(f)
            new_image = Image.new('RGBA', original.size)
            height = original.size[1]
            width = original.size[0]
            bar_size = 1
            for y in range(height):
                for x in range(width):
                    pixel = original.getpixel((x, y))
                    if height - bar_size <= y + 1 <= height:
                        new_image.putpixel((x, y), (color[0], color[1], color[2], 255))
                    else:
                        new_image.putpixel((x, y), (pixel[0], pixel[1], pixel[2], pixel[3]))
            stream = io.BytesIO()
            new_image.save(stream, format="ICO")
            return base64.b64encode(stream.getvalue())

    def _set_wk_favicon(self, favicon):
        for company in self:
            company.favicon = tools.image_process(favicon, size=(180, 0))

    @api.model
    def reset_company_logo(self):
        order_objs = self.search([])
        for order_obj in order_objs:
            order_obj.logo = open(
                os.path.join(tools.config['root_path'], 'addons', 'base', 'res', 'res_company_logo.png'),
                'rb').read().encode('base64')
