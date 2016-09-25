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
    'name'          : 'Events - invitations',
	'version'       : '1.0',
	'category'      : 'Events',
    'summary'       : 'Provides an easy way to invite partners to your events',
	'description'   : """
Associate mail templates to event types\n
Send individual or bulk invitation messages
	
NOTES:\n
- mail templates should be of the event.invitation.line type\n
- invitations by bulk mail are not individually trackable\n
- in bulk messages, the "TO" field contains all email addresses\n


MAKE SURE YOU CHECK MY OTHER MODULES AT... https://goo.gl/TteO1F
""",

	'author'        : 'Odooveloper (Rui Franco)',
	'website'       : 'http://www.odooveloper.com',
	'depends'       : [
	                   'event',
	                   'email_template',
	                   ],
	'data'          : [
	                   'security/event_security.xml',
                       'security/ir.model.access.csv',
                       
	                   'event_view.xml',
	                   'email_template_view.xml',
	                   'partner_view.xml',
	                   ],
    'qweb'          : [],             
    'installable'   : True,
    'active'        : False,
}
