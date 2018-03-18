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
	'version'       : '2.0',
	'category'      : 'Tools',
	'summary'       : 'Repository management / module deployment',
	'description'   : """
- creates a README file to be used in repositories to tell people what the module is all about
- packs a module as well as its dependencies so that it can be deployed anywhere

This module assumes you have ZIP installed in your system.
""",
	'author'        : 'Odooveloper',
	'website'       : 'http://www.odooveloper.com',
	'depends'       : ['base'],
	'data'         : [
	                   'repository_manager_view.xml',
	                   'res_config_view.xml',
	                   ],
	'installable'   : True,
}
