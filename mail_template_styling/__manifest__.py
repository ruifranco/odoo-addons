# -*- coding: utf-8 -*-
# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Mail Template - Styling',
    'version': '2.0',
    'category': 'Discuss',
    'summary': 'Universally manage and style mail templates sent from Odoo',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'license': 'LGPL-3',
    'depends': ['mail'],
    'external_dependencies': {'python': ['premailer']},
    'data': [
        'security/ir.model.access.csv',
        'views/mail_template_style_views.xml',
        'views/mail_template_views.xml'
    ],
    'images': [
        'static/description/banner.png',
    ]
}
