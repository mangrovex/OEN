import subprocess
import re
import logging

from odoo import _

_logger = logging.getLogger(__name__)

time_value_pattern = re.compile(r'^[0-9]+,[0-9][0-9]$')

number_value_pattern = re.compile(r'^[0-9]+$')

MEASURE_UNIT = [
    ('time', _('Time')),
    ('number', _('Number')),
]

TIME_CONTROL = [
    ('between', _('Between')),
    ('exceed', _('Exceed')),
    ('not exceed', _('Not Exceed')),
]

GENDER = [
    ('male', _('Male')),
    ('female', _('Female')),
]


SCORE_STATE = [
    ('draft', _('Draft')),
    ('published', _('Published')),
    ('for review', _('For review')),
    ('approved', _('Approved')),
]

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
