import logging

from odoo import _, models, fields

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    student_ids = fields.One2many(comodel_name='sie.student', inverse_name='user_id')
