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


class res_partner(orm.Model):
    _inherit='res.partner'

    _columns={
        'equipment_ids'  : fields.one2many('res.partner.equipment', 'partner_id', 'Equipment'),
        }
  
    #returns an array of tuples (categ_id, quantity)
    def _get_partner_equipment(self, cr, uid, partner_id):
        partner_equip=[]
        if partner_id:
            partner_equip_obj=self.pool.get('res.partner.equipment')
            partner_equip_ids=partner_equip_obj.search(cr, uid, [('partner_id','=',partner_id)])
            if partner_equip_ids:
                partner_equip_res=partner_equip_obj.browse(cr, uid, partner_equip_ids)
                for peq in partner_equip_res:
                    partner_equip.append((peq.categ_id.id,peq.qty))
        return partner_equip
          
  
  
class res_partner_equipment(orm.Model):
    _name='res.partner.equipment'
    
    _columns={
        'partner_id': fields.many2one('res.partner','Partner', required=True),
        'categ_id'  : fields.many2one('product.category','Category', readonly=True),
        'qty'       : fields.integer('Quantity'),    
        'notes'     : fields.char('Comments', size=255),        
    }
    _defaults={
        'qty': 0,
    }

