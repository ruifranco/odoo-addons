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


class clothing_sizes_types(orm.Model):
    _name='clothing_sizes.types'
    _description='Types of clothing or parts of the body'

    _columns={
        'name'      : fields.char('Name', size=50), 
        'active'    : fields.boolean('Active'),
    }

    _defaults = {
        'active': True,
    }

    _base_types=['Hands','Shirt','Trousers','Head','Bra','Bra (cup)','Feet']


    #some types cannot be deleted
    def unlink(self, cr, uid, ids, context=None):

        if context is None:
            context = {}
    
        if isinstance(ids, (int, long)):
            ids = [ids]
    
        for this in self.browse(cr, uid, ids):
            if this.name in self._base_types:
                raise osv.except_osv(_('Error!'), _('%s cannot be deleted because it is a base type') % (this.name))
    
        return super(clothing_sizes_types, self).unlink(cr, uid, ids, context=context)
    
    
    #some types cannot be changed
    def write(self, cr, uid, ids, vals, context=None):
    
        if context is None:
            context = {}
            
        if isinstance(ids, (int, long)):
            ids = [ids]
            
        for this in self.browse(cr, uid, ids):
            if 'name' in vals:
                if this.name in self._base_types:
                    raise osv.except_osv(_('Error!'), _('%s name cannot be changed because it is a base type') % (this.name))

        return super(clothing_sizes_types, self).write(cr, uid, ids, vals, context=context)




    

class clothing_sizes_sizes(orm.Model):
    _name='clothing_sizes.sizes'
    _description='Sizes for clothing'


    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        if isinstance(ids, (int, long)):
            ids = [ids]

        reads = self.read(cr, uid, ids, ['name', 'code', 'age', 'gender', 'type_id'], context=context)
        res = []
        
        size_type_obj=self.pool.get('clothing_sizes.types')
        
        for record in reads:

            if record['code']:
                name = record['code']
            else:
                name = record['name']

            if record['age'] or record['gender'] or record['type_id']:
            
                aux=[]
                
                if record['age']:
                    aux.append(record['age'])
            
                if record['gender']:
                    aux.append(record['gender'])
                 
                if record['type_id']:
                    type_res=size_type_obj.browse(cr, uid, record['type_id'][0])
                    if type_res:
                        aux.append(type_res[0].name)
                
                    
                if aux:
                    name = name + ' ' + '/'.join(aux)

            res.append((record['id'], name))

        return res

    
    _columns={
        'name'          : fields.char('Name', size=50, required=True), 
        'code'          : fields.char('Code', size=5),    
        'age'           : fields.selection((('c','Child'),('a','Adult')), 'Age'),
        'gender'        : fields.selection([('male', 'Male'),('female', 'Female')], 'Gender'),     
        'type_id'       : fields.many2one('clothing_sizes.types', 'Type'),
        'country_ids'   : fields.many2many('res.country', 'clothing_sizes_countries', 'clothing_sizes_id', 'country_id', 'Country'),
        'active'        : fields.boolean('Active'),
    }

    _defaults = {
        'active': True,
    }

