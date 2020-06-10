import logging

from odoo import _

_logger = logging.getLogger(__name__)

CONTROL_STATE = [
    ('draft', _('Draft')),
    ('published', _('Published')),
    ('settled', _('Settled')),
]

SCORE_NUMBER = [
    ('1', 'Note 1'),
    ('2', 'Note 2'),
    ('3', 'Note 3'),
    ('4', 'Note 4'),
    ('5', 'Note 5'),
    ('6', 'Note 6'),
    ('7', 'Note 7'),
    ('8', 'Note 8'),
    ('9', 'Note 9'),
    ('10', 'Note 10'),
    ('11', 'Note 11'),
    ('12', 'Note 12'),
    ('13', 'Note 13'),
    ('14', 'Note 14'),
    ('15', 'Note 15'),
    ('16', 'Note 16'),
    ('17', 'Note 17'),
]

SCORE_STATE = [
    ('draft', _('Draft')),
    ('published', _('Published')),
    ('for review', _('For review')),
    ('approved', _('Approved')),
]