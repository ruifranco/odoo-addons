# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Multibase.pt (<http://www.multibase.pt>)
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
    'name'          : 'Repository manager',
	'version'       : '1.0',
	'category'      : 'Tools',
	'summary'       : 'Repository management',
	'description'   : """In this very early stage, this module will only let you create a README file to be used in a repository manager.\n
It uses the info on the module to create the file and saves it in the module's folder.\n
Check the Repository tab inside any module's form.""",
	'author'        : 'Rui Pedrosa Franco',
	'website'       : 'http://pt.linkedin.com/in/ruipedrosafranco',
	'depends'       : ['base'],
	'update_xml'    : ['repository_manager_view.xml'],
	'installable'   : True,
}
