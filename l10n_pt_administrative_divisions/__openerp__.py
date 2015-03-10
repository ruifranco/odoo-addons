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
	'version'       : '1.0',
	'category'      : 'Localization',
    'summary'       : 'Geographic/administrative details',
	'description'   : """
	                    Adiciona os campos para 'Distrito', 'Concelho' e 'Freguesia'
                        Adds fields for address in res.partner: distrito, concelho, freguesia\n\n
                                                
                        
                        """,
	'author'        : 'Rui Pedrosa Franco',
	'website'       : 'http://pt.linkedin.com/in/ruipedrosafranco',
	'data'          : [
                        'data/l10n_pt_administrative_divisions_distritos_data.xml',
                        'data/l10n_pt_administrative_divisions_concelhos_data.xml',
                        'data/l10n_pt_administrative_divisions_freguesias_data.xml',

                        'security/ir.model.access.csv',
                        
                        'l10n_pt_administrative_divisions_distritos_view.xml',
                        'l10n_pt_administrative_divisions_concelhos_view.xml',
                        'l10n_pt_administrative_divisions_freguesias_view.xml',
                        'l10n_pt_administrative_divisions_view.xml',
                        ],
    'installable'   : True,
    'active'        : False,
}
