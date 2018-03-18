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
    'name'          : 'Multicompany enforcement: voucher',
    'version'       : '1.0',
    'category'      : 'Localisation/Account',
    'summary'       : 'Domain and filter enforcement in a multicompany environment',
    'description'   : """
Enforces domains and filters according to chosen company in a multicompany environment.
    
\nField domains applied in:
- Sales receipts
- Customer payments
- Purchase receipts
- Supplier payments
                        
\nFilter and grouping added to search views
                        
\nTo do:
- customer payments, supplier payments: lines not being removed on company change
- apply domains in: view_low_priority_payment_form, view_vendor_receipt_dialog_form 
                        """,
    'author'        : 'Odooveloper',
    'website'       : 'http://www.odooveloper.com',
    'depends'       : ['account_voucher',],
    'update_xml'    : [
                        'ir_sequence_view.xml',
                        'account_voucher_view.xml',
                        ],
    'installable'   : True,
    'active'        : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
