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
    'name'          : 'HR Holidays - requests reminders',
	'version'       : '1.0',
	'category'      : 'Human Resources',
	'summary'       : """Sets reminders related to employee's leaves""",
	'description'   : """
- adds a field to the request form, so that a deadline can be set
- in 'Leave Requests to Approve' and 'Allocation Requests to Approve' tree views, lines become orange whenever deadlines have been set
- on confirmation: sends email to the employee's manager
- on refusal/approval: sends email to the employee

NOTE:
A valid email server configuration is required
                    """,
	'author'        : 'Odooveloper',
	'website'       : 'http://www.odooveloper.com',
	'depends'       : ['hr_holidays',],
	'data'          : [
                        'hr_holidays_reminders_data.xml',
                        
                        'hr_holidays_view.xml',
                        'hr_holidays_workflow.xml',
                        ],
    'installable'   : True,
    'active'        : False,
}
