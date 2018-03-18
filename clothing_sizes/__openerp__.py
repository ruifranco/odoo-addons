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
    'name'          : 'Clothing sizes',
	'version'       : '1.0',
	'category'      : 'Technical Settings',
    'summary'       : 'Definition of clothing sizes',
	'description'   : """
Allows to define clothing sizes according to country rules
                        """,
	'author'        : 'Odooveloper',
	'website'       : 'http://www.odooveloper.com',
	'depends'       : ['base'],
	'data'          : [
                        'security/ir.model.access.csv',
	
                        'data/clothing_sizes_types_data.xml',
                        'data/clothing_sizes_general_data.xml',
                        'data/clothing_sizes_feet_data.xml',
                        'data/clothing_sizes_hand_data.xml',
                        'data/clothing_sizes_head_data.xml',
                        
                        'clothing_sizes_view.xml',
                        ],
    'installable'   : True,
    'active'        : False,
}
