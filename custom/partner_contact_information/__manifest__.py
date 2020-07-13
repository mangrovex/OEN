# -*- coding: utf-8 -*-
###############################################################################
#
#    Manexware S.A.
#    Copyright (C) 2009-TODAY Manexware
#    noinspection PyStatementEffect
#
###############################################################################
{
    "name": "Contact Information",
    "summary": "Add information to contacts",
    "version": "13.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://manexware.com/",
    "author": "Manexware S.A.",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": False,
    "depends": [
        "partner_contact_information_page",
        "percent_field"
                ],
    "data": ["views/res_partner.xml"],
    "post_init_hook": "post_init_hook",
}
