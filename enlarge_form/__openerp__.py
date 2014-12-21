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
    'name'          : 'Enlarge form',
	'version'       : '1.0',
	'category'      : 'Tools',
    'summary'       : 'Removal of the page-like look in forms',
	'description'   : """
This will let you remove the page-like look of any form and thus use the whole width of the screen.
Go to the view administration, choose the one you want to change and press the 'Use full width of the screen?' checkbox. Then, save the record.
\n\n
WARNING:\n
- You should always check in the 'Inherited Views' tab for the existence of a view of the '_enlarge_form' type.\n
If it is not there, repeat the operation.""",
	'author'        : 'Rui Pedrosa Franco',
	'website'       : 'http://pt.linkedin.com/in/ruipedrosafranco',
	'depends'       : ['base'],
	'data'          : ['enlarge_form_view.xml',],
	'css'           : ['static/src/css/enlarge_form.css'],
    'installable'   : True,
    'active'        : False,
}
