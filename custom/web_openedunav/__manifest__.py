# -*- coding: utf-8 -*-
###############################################################################
#
#    Manexware S.A.
#    Copyright (C) 2009-TODAY Manexware
#
#    noinspection PyStatementEffect
#
###############################################################################
{
    'name': 'Web OpenEduNav',
    'category': 'Website',
    "sequence": 3,
    'version': '13.0',
    'license': 'LGPL-3',
    'author': 'Manexware S.A.',
    'website': 'http://www.manexware.com',
    'data': [
        'views/assets.xml',
        'views/snippets/slider.xml',
        'views/snippets/about-us.xml',
        'views/snippets/ourcourse.xml',
        'views/snippets/achievement.xml',
        'views/snippets/teacher.xml',
        'views/snippets/event.xml',
        'views/snippets/newsfeed.xml',
        'views/snippets/footer.xml',
        'views/image_library.xml'
    ],
    'demo': [
        'data/homepage_demo.xml',
        'data/footer_template.xml',
    ],
    'images': [
        'static/description/web_openedunav_banner.jpg',
    ],
    'depends': [
        'website',
    ],
}
