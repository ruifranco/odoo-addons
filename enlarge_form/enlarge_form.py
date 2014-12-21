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


class ir_ui_view(orm.Model):

    _inherit = 'ir.ui.view'

    _columns={
        'enlarge_form' : fields.boolean('Use full width of the screen?' ,help='Set to true if you want to widden this form so that it will use full width of the screen.'),
    }

    def create(self, cr, uid, data, context=None):
        result = super(ir_ui_view, self).create(cr, uid, data, context=context)
        if result:
            self.manipulate_sheet_tag(cr, uid, result)
        return result

    
    
    def write(self, cr, uid, ids, data, context=None):
        result = super(ir_ui_view, self).write(cr, uid, ids, data, context=context)
        if result:
            self.manipulate_sheet_tag(cr, uid, ids)
        return result

    
    def has_sheet_tag(self, arch):
        res=False
        if arch.find('<sheet')>=0:
            res=True
        return res



    def manipulate_sheet_tag(self, cr, uid, ids):

        if not isinstance(ids,(tuple,list)):
            ids=[ids]
        
        #Warning(str(ids))

        for this in self.browse(cr, uid, ids):

            enlargement_view = str(this.model).replace('.','_') + '_enlarge_form'
    
            #does a view already exist?
            #view_exists=self.search(cr, uid, [('name','=',enlargement_view),('type','=','form'),('active','in',[True,False])])
            view_exists=self.search(cr, uid, [('name','=',enlargement_view),('type','=','form')])
            if view_exists:
                if isinstance(view_exists,(tuple,list)):
                    view_exists=view_exists[0]
    
            has_sheet_tag=self.has_sheet_tag(this.arch)
    
            #what should we do?
            if view_exists:
                if not has_sheet_tag:
                    operation='deactivate_view'
                else:
                    if this.enlarge_form:
                        operation='activate_view'
                    else:
                        operation='deactivate_view'
            else:
                if has_sheet_tag and this.enlarge_form:
                    operation='create_view'
                else:
                    #nothing to do
                    operation=False


    
            if not operation:
                return True
    
                                
            if operation=='create_view':
                view_arch="""<?xml version='1.0'?><xpath expr='//form/sheet' position='attributes'><attribute name='class'>enlarge_form</attribute></xpath>"""
    
                #model_data_ids_form = model_obj.search(cr, user, [('model','=','ir.ui.view'), ('name', 'in', ['membership_products_form', 'membership_products_tree'])], context=context)
        
                vals={
                        'name'          : enlargement_view,
                        'type'          : 'form',
                        'model'         : this.model,
                        'inherit_id'    : this.id,
                        'arch'          : view_arch,
                        
                        'xml_id'        : 'enlarge_form.'+enlargement_view,
                        'active'        : 'True',
                        }
                res=self.create(cr, uid, vals)
                
                #for some reason, active was always getting saved as false
                if res:
                    cr.execute("UPDATE ir_ui_view SET active=TRUE WHERE id=%s" % res)

            elif operation=='activate_view':
                self.write(cr, uid, view_exists, {'active':True})
    
            elif operation=='deactivate_view':
                self.write(cr, uid, view_exists, {'active':False})
    
    

        return True
