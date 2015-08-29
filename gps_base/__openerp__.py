# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Rui Pedrosa Franco All Rights Reserved
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
    'name'          : 'GPS - base functions',
	'version'       : '1.1',
	'category'      : 'Extra Tools',
	'summary'       : 'Base functionalities for the use of GPS coordinates',
	'description'   : """
Base GPS functions\n\n
- creates gps.coords records that can be associated to models
- coords are saved in the decimal degrees format
- users can choose wich coordinate format to use throughout Odoo
                        
PS: 
- map widget is based on Dorin Hongu's web_gmaps module
- JavaScript had an invaluable help from Dinil UD

MAKE SURE YOU CHECK MY OTHER MODULES AT... https://www.odoo.com/apps?search=rui+pedrosa+franco
                        """,
	'author'        : 'Rui Pedrosa Franco',
	'website'       : 'http://pt.linkedin.com/in/ruipedrosafranco',
	'depends'       : ['web'],
	'data'          : [
                        'views/gps_base_view.xml',
                        'views/res_users_view.xml',
                        'views/web_gmaps_assets.xml',
                        ],
    'qweb'          : ['static/src/xml/resource.xml'],
    'installable'   : True,
    'active'        : False,
}
