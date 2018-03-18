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
    'name'          : 'Events - equipment',
	'version'       : '1.0',
	'category'      : 'Extra Tools',
    'summary'       : 'Management of equipment lists for events',
	'description'   : """
- Allows to define lists of equipment associated to an event
- Partners may define what kind of equipment they possess (from the ones associated to any event they have registered in)
- Equipment can be associated to the attendants or to the event itself
- Partner field is shown in the event's registration lines
- Equipment lists can be associated to event types
- Event type becomes mandatory
- Shows equipment list in the event type tree view
                        
NOTE:
- (event.event) equipment_host_text and equipment_participants_text hold the equipment list as text
                        """,
	'author'        : 'Odooveloper',
	'website'       : 'http://www.odooveloper.com',
	'depends'       : [
	                   'product_equipment_list',
	                   'event',
	                   ],
	'data'          : [
	                   'security/ir.model.access.csv',
	
	                   'views/event_view.xml',
	                   'views/partner_view.xml',
	                   
                       'views/report_equipment_host.xml',
	                   'equipment_report.xml',
	                   ],
    'installable'   : True,
    'active'        : False,
}
