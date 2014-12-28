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
from openerp.osv import osv, orm
from openerp import models, fields, api, _
from openerp import tools


class event_type(models.Model):
    _inherit='event.type' 

    equipment_ids = fields.Many2many('product.equipment',
        'product_equipment_event_type_rel', 'equipment_id', 'event_type_id', string='Equipment list')
        
    equipment_ids_text = fields.Char('Equipment lists', compute='_get_equipment_lists')
    
    @api.one
    @api.onchange('equipment_ids')
    def _get_equipment_lists(self):
        aux=[]
        for e in self.equipment_ids:
            aux.append(e.name)
        
        self.equipment_ids_text='\n'.join(aux)