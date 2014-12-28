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




class product_equipment(models.Model):
    _name = 'product.equipment'


    @api.one
    @api.depends('equipment_lines')
    def _get_equipment_text(self):
        fsep = '|'
        lsep = '\n'

        aux=_('Category') + fsep + _('Quantity') + fsep + _('Mandatory') + fsep + _('Comments') + lsep
        for l in self.equipment_lines:
            categ_name=self.pool.get('product.category').name_get(self._cr, self._uid, l.categ_id.id)
            if isinstance(categ_name,(list,tuple)):
                categ_name=categ_name[0]
                if isinstance(categ_name,(list,tuple)):
                    categ_name=categ_name[1]
                
            aux+=_(categ_name) + fsep + str(l.qty) + fsep + _(l.mandatory) + fsep + _(l.notes) + lsep
                
        self.equipment_text = aux

    
    name              = fields.Char(string='Name', size=100, required=True)
    equipment_lines   = fields.One2many('product.equipment.lines','equipment_id',string='Equipment lines', required=True)

    #this field contains the equipment_lines as one piece of text
    equipment_text    = fields.Text(string='Equipment', compute='_get_equipment_text')







class product_equipment_line(models.Model):
    _name = 'product.equipment.lines'

    equipment_id  = fields.Many2one('product.equipment',string='Equipment list')
    categ_id      = fields.Many2one('product.category',string='Category', required=True)
    qty           = fields.Integer(string='Quantity', required=True, default=1)  
    mandatory     = fields.Boolean(string='Mandatory')  
    notes         = fields.Char(string='Comments', size=255)
   
