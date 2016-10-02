#! -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Odooveloper (Rui Pedrosa Franco) All Rights Reserved
#    http://www.odooveloper.com
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
    'name'          : 'Task information in sale order line',
    'version'       : '1.0',
    'category'      : 'Sales Management',
    'summary'       : 'Shows tasks information in sale orders',
    'description'   : """
- From a sale order line detail, you can see the associated tasks
- In sale order lines, task completion is shown
- Overall task completion for the sale order is available

WARNING: since there is no sure way to know if a task stage is of the "cancelled" type, 
results may not be accurate in case you cancel tasks.

MAKE SURE YOU CHECK MY OTHER MODULES AT... https://goo.gl/TteO1F
""",
    'author'        : 'Odooveloper (Rui Franco)',
    'website'       : 'http://www.odooveloper.com',
    'depends'       : ['sale_service'],
    'data'          : [
                       'views/sale_order_view.xml',
                       ],
    'images'        : ['static/description/main_screenshot.png'],
    'installable'   : True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
