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
    'name'          : 'Project task repetition',
	'version'       : '1.0',
	'category'      : 'Extra Tools',
    'summary'       : 'Allows to set repetition of project tasks',
	'description'   : """
With this module you are able to repeat project tasks pretty much in the same way as you repeat calendar events.

MAKE SURE YOU CHECK MY OTHER MODULES AT... http://goo.gl/ZNr83u	
	""",
	'author'        : 'Odooveloper (Rui Franco)',
	'website'       : 'http://www.odooveloper.com',
    'depends'       : ['project'],
	'data'          : ['project_task_repetition_view.xml'],
    'installable'   : True,
    'active'        : False,
}
