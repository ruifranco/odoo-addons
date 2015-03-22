#! -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Rui Pedrosa Franco All Rights Reserved
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
from openerp import tools
from openerp.tools.translate import _



class caving_gas(orm.Model):
    _name ='caving.gas'

    _columns = {
        'name'      : fields.char('Name', size=100, required=True),
        'aka'       : fields.char('Also known as...', size=100),
        'symbol'    : fields.char('Symbol', size=50),
        'is_toxic'  : fields.boolean('Is toxic?'),          
        'has_smell' : fields.boolean('Has smell?'),         
        'colour'    : fields.char('Colour', size=100),          
        'notes'     : fields.text('Notes'),
        'cave_ids'  : fields.many2many('caving.cave', 'caving_cave_gas_rel', 'gas_id', 'cave_id', 'Caves'),
    }
