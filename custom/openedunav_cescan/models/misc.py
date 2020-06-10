# # -*- coding: utf-8 -*-
#
# import logging
#
# from odoo import _
#
# _logger = logging.getLogger(__name__)
#
#
# def _check_verification_vat(identification):
#     l = len(identification)
#     if l == 10 or l == 13:  # check right length
#         cp = int(identification[0:2])
#         if 1 <= cp <= 22:  # check right state code
#             tercer_dig = int(identification[2])
#             if 0 <= tercer_dig < 6:  # number between 0 y 6
#                 if l == 10:
#                     return _verification_vat(identification, 0)
#                 elif l == 13:
#                     return _verification_vat(identification, 0) \
#                            and identification[10:13] != '000'  # check last number not 000
#             elif tercer_dig == 6:
#                 return _verification_vat(identification, 1)  # public society
#             elif tercer_dig == 9:  # si es ruc
#                 return _verification_vat(identification, 2)  # public society
#             else:
#                 return False
#         else:
#             return False
#     else:
#         return False
#
#
# def _verification_vat(identification, num):
#     total = 0
#     unicodestring = identification
#     identification_id = str(unicodestring).encode("utf-8")
#     if num == 1:  # r.u.c. public
#         base = 11
#         d_ver = int(identification_id[8])
#         _logger.warning("digit ver %d" % d_ver)
#         multip = (3, 2, 7, 6, 5, 4, 3, 2)
#         longitude = 8
#     elif num == 2:  # r.u.c. legal and foreigners without id
#         base = 11
#         d_ver = int(identification_id[9])
#         _logger.warning("digit ver %d" % d_ver)
#         multip = (4, 3, 2, 7, 6, 5, 4, 3, 2)
#         longitude = 9
#     else:  # cedula y r.u.c persona natural
#         base = 10
#         d_ver = int(identification_id[9])  # check digit
#         multip = (2, 1, 2, 1, 2, 1, 2, 1, 2)
#         longitude = 9
#     for i in range(0, longitude):
#         a = int(identification_id[i])
#         _logger.warning(a)
#         b = multip[i]
#         p = a * b
#         if num == 0:
#             total += p if p < 10 else int(str(p)[0]) + int(str(p)[1])
#         else:
#             total += p
#     mod = total % base
#     val = base - mod if mod != 0 else 0
#     return val == d_ver
#
#
# BLOOD_TYPE = [
#     ('O-', 'O-'),
#     ('O+', 'O+'),
#     ('A-', 'A-'),
#     ('A+', 'A+'),
#     ('B-', 'B-'),
#     ('B+', 'B+'),
#     ('AB-', 'AB-'),
#     ('AB+', 'AB+'),
# ]
#
# GENDER = [
#     ('male', 'Masculino'),
#     ('female', 'Femenino'),
# ]
#
# PERSONAL_TYPE = [
#     ('civil', 'Civil'),
#     ('military', 'Militar'),
# ]
#
# ROL = [
#     ('director', _('Director')),
#     ('planta', _('Oficial de Planta')),
#     ('division', _('Oficial de Division')),
# ]
