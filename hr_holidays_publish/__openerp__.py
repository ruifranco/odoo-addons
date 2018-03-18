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
    'name'          : 'HR Holidays - Publish',
	'version'       : '1.0',
	'category'      : 'Human Resources',
	'summary'       : """Control who can see your leaves""",
	'description'   : """
By default, Odoo only allows employees to see their own leaves. This is not practical within a company as employee's holidays have to be be combined.
By not being able to know about other's requests, employees have to go through HR in what might be a frustrating process.
With this module, each employee has the chance of letting others know about his leaves, thus contributing to the transparency and easyness inside the company.
""",
	'author'        : 'Odooveloper',
	'website'       : 'http://www.odooveloper.com',
	'depends'       : ['hr_holidays'],
	'data'          : [
                       'security/ir.model.access.csv',
                       'hr_holidays_publish_data.xml',
                       'hr_holidays_publish_view.xml',
                       ],
    'currency'      : 'EUR',
    'installable'   : True,
    'active'        : False,
}
