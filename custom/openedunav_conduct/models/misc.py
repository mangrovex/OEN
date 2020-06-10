import logging

from odoo import _

_logger = logging.getLogger(__name__)

CONTROL_STATE = [
    ('draft', _('Draft')),
    ('published', _('Published')),
    ('settled', _('Settled')),
]

KIND_OF_MERIT = [
    ('medal', _('Medal')),
    ('recognition', _('Recognition')),
]
