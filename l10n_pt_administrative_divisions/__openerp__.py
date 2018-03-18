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
    'name'          : 'Portugal - administrative divisions',
	'version'       : '2.0',
	'category'      : 'Localization',
    'summary'       : 'Geographic/administrative details',
	'description'   : """
Preenche a informação relativa a 'Distrito', 'Concelho' e 'Freguesia'.\n\n
Loads info concerning 'Distrito', 'Concelho', 'Freguesia'\n\n
""",
	'author'        : 'Odooveloper',
    'depends'       : ['address_extended'],
	'website'       : 'http://www.odooveloper.com',
	'data'          : ['data/address_extended.places.csv',],
    'installable'   : True,
    'active'        : False,
}
