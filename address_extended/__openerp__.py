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
    'name'          : 'Address - extended',
	'version'       : '1.3',
	'category'      : 'Localization',
    'summary'       : 'Extra fields to save more info on addresses',
	'description'   : """
Adds three hierarchically dependent fields so that more info can be saved on addresses (typically, region, county, etc.).

MAKE SURE YOU CHECK MY OTHER MODULES AT... http://goo.gl/ZNr83u
                        """,
	'author'        : 'Odooveloper (Rui Franco)',
	'website'       : 'http://www.odooveloper.com',
	'data'          : [
                        'security/ir.model.access.csv',
                        'address_extended_view.xml',
                        'res_partner_view.xml',
                        ],
    'installable'   : True,
    'active'        : False,
}
