#! -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Rui Pedrosa Franco All Rights Reserved
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

from openerp import addons
from openerp.osv import fields, osv, orm


class res_users(orm.Model):

    _inherit    = 'res.users'
    
    _columns = {
        'coords_format': fields.selection(
                                            (
                                                ('dd','Decimal degrees: N 40.446°, W 79.982°'), 
                                                ('ddm',"Degrees decimal minutes: N 40° 26.767′, W 79° 58.933′"),
                                                ('dms',"Degrees minutes seconds: N 40° 26′ 46″, W 79° 58′ 56''"),
                                            ), 
                                            'Coordinate format', 
                                            help='This is the format in which coordinates will be shown and entered',
                                            ),
    }

    _defaults = {
        'coords_format': 'dd', 
    }
