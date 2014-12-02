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
  
  
class res_partner_equipment(orm.Model):
    _name='res.partner.equipment'
    
    """
    def _get_allowed_categories(self, cr, uid, context=None):
        res=[]
        equip_obj=self.pool.get('event.equipment.lines')
        lines_ids=equip_obj.search(cr, uid, [('type','=','participant')])
        #raise osv.except_osv('Warning!',str(categ_ids))
        if lines_ids:
            lines_res=equip_obj.browse(cr, uid, lines_ids)
            for l in lines_res:
                aux=(l.categ_id.id,self.pool.get('product.category').name_get(cr,uid,l.categ_id.id))
                if not aux in res:
                    res.append(aux)
        return res    
    """                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
    
    #funções create e write para lidar com os dados e gravar o categ_id
    
    """
    def create(self, cr, uid, data, context=None):
        data['qty']=5
            return super(res_partner_equipment, self).create(cr, uid, data, context)
    """
    
    _columns={
        'partner_id'        : fields.many2one('res.partner','Partner', required=True),

        'categ_id'          : fields.many2one('product.category','Category', readonly=True),
        #'categ_id_domain'   : fields.selection(_get_allowed_categories,'Category domain'),

        'qty'               : fields.integer('Quantity'),    
        'notes'             : fields.char('Comments', size=255),        
    }
    _defaults={
        'qty': 0,
    }

