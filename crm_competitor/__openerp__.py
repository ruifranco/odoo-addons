#! -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Odooveloper (Rui Pedrosa Franco) All Rights Reserved
#    http://pt.linkedin.com/in/ruipedrosafranco
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name'          : 'CRM Competitor',
    'version'       : '1.0',
    'category'      : 'CRM',
    'summary'       : "Enables following competitor's activity",
    'description'   : """Let's you record competitor's activity for a lead/opportunity""",
    'author'        : 'Rui Pedrosa Franco',
    'website'       : 'http://www.odooveloper.com',
    'depends'       : ['crm'],
    'data'          : [
                       'views/res_partner_view.xml',
                       'views/crm_lead_view.xml',
                       ],
    'installable'   : True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
