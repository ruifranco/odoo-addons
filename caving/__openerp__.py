# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Rui Pedrosa Franco All Rights Reserved
#    http://pt.linkedin.com/in/ruipedrosafranco
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name'          : 'GRUTA - caving',
	'version'       : '1.0',
	'category'      : 'Knowledge Management',
	'summary'       : 'A way to record information on caves',
	'description'   : """
'GRUTA - caving' enables you to save information on caves.

This module is the first piece of an application that aims to be a caving information system with which caving groups will be able to record everything concerning their activities.

Don't hesitate to give some feedback.

MAKE SURE YOU CHECK MY OTHER MODULES AT... https://goo.gl/TteO1F
""",
	'author'        : 'Odooveloper (Rui Franco)',
	'website'       : 'http://www.odooveloper.com',
	'depends'       : [
                        'mail',
                        'document',
                        'gps_base',
                        'contacts',
                        ],
    'demo'          : ['data/caving_demo.xml'],
    'data'          : [
                        'data/caving_geologic_time_data.xml',

                        'security/caving_security.xml',
                        'security/ir.model.access.csv',

                        'view/caving_cave_view.xml',
                        'view/caving_area_view.xml',
                        'view/caving_fauna_view.xml',
                        'view/caving_flora_view.xml',
                        'view/caving_link_view.xml',
                        'view/caving_reference_view.xml',
                        'view/caving_gas_view.xml',
                        'view/caving_view.xml'
                        ],
    'images'        : ['static/description/main_screenshot.png'],
    'installable'   : True,
    'active'        : False,
}
