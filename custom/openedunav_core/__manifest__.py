# -*- coding: utf-8 -*-
###############################################################################
#
#    Manexware S.A.
#    Copyright (C) 2009-TODAY Manexware
#
# noinspection PyStatementEffect
###############################################################################

{
    'name': 'OpenEdunav Core',
    'version': '13.0.0.1',
    'author': 'Manexware S.A.',
    'category': 'Education',
    'website': 'http://www.manexware.com',
    'summary': 'Sistema Educativo de la Armada del Ecuador',
    'images': [],
    'depends': [
        'base_location',
        'partner_contact_information',
        'hr',
        'board',
        'web',
        'website'
    ],
    'data': [
        'security/sie_security.xml',
        'security/ir.model.access.csv',
        'data/location_data.xml',
        'data/academic_title_data.xml',
        'data/category_data.xml',
        'data/decimal_precision_data.xml',
        'data/grade_data.xml',
        'data/nato_data.xml',
        'data/person_title_data.xml',
        'data/religion_data.xml',
        'data/specialty_data.xml',
        'data/promotion_data.xml',
        'data/sub_specialty_data.xml',
        'views/res_partner_views.xml',
        'views/person_abstract_entity.xml',
        'views/sie_academic_title_views.xml',
        'views/sie_category_views.xml',
        'views/sie_grade_views.xml',
        'views/sie_nato_views.xml',
        'views/sie_person_title_views.xml',
        'views/sie_faculty_views.xml',
        'views/sie_religion_views.xml',
        'views/sie_promotion_views.xml',
        'views/res_company_views.xml',
        'views/sie_specialty_views.xml',
        'views/sie_sub_specialty_views.xml',
        'views/sie_student_views.xml',
        'views/sie_student_category_views.xml',
        'views/sie_location_views.xml',
        'views/hr_view.xml',
        'views/website_assets.xml',
        'views/openedunav_template.xml',
        'views/sie_menu.xml'
    ],

    'installable': True,
    'auto_install': False,
    'application': False,
}
