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
    'name'          : 'Contact gender (autofill)',
    'version'       : '1.0',
    'category'      : 'Customer Relationship Management',
    'summary'       : "Automatic selection of a contact's gender",
    'description'   : """This module extends OCA's 'partner_contact_gender' module allowing for contact's gender to be autofilled according to the name.""",
    'author'        : 'Odooveloper (Rui Franco)',
    'website'       : 'http://www.odooveloper.com',
    'depends'       : ['partner_contact_gender'],
    'data'          : [
                       'security/ir.model.access.csv',
                       'data/name_gender_data.xml',
                       'data/odooveloper_data.xml',
                       'views/name_gender_view.xml',
                       ],
    'images'        : ['static/description/main_screenshot.png'],
    'installable'   : True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
