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
from openerp.osv import fields, osv
from openerp import tools
from openerp.tools.translate import _

import uuid
import string
from random import *


class res_partner(osv.osv):
    _inherit = 'res.partner'

    #creates employee and redirects to it
    def create_employee(self, cr, uid, partner_id, context):

        employee_id=self.create_employee_from_partner(cr, uid, partner_id, context)
        
        if not employee_id:
            return False
        else:
            view_id = self.pool.get('ir.ui.view').search(cr, uid, [('model','=','hr.employee'),('type','=','form')], order='id ASC')
            if isinstance(view_id,(list,tuple)):
                view_id=view_id[0]

            return {
                'view_type' : 'form',
                'view_mode' : 'form',
                'view_id'   : view_id,
                'res_model' : 'hr.employee',
                'res_id'    : employee_id,
                'type'      : 'ir.actions.act_window',
                'target'    : 'current',
            }


    #creates employee with partner's data
    def create_employee_from_partner(self, cr, uid, partner_id, context):
        employee_id=False

        if isinstance(partner_id,(list,tuple)):
            partner_id=partner_id[0]
 
        if partner_id and not self.partner_has_employee(cr, uid, partner_id):
            partner_res=self.browse(cr, uid, partner_id)
            if partner_res:
                employee_obj=self.pool.get('hr.employee')
        
                employee={
                        'name'              : partner_res.name,
                        'country_id'        : partner_res.country_id.id,
                        'image'             : partner_res.image,
                        'work_email'        : partner_res.email,
                        'address_home_id'   : partner_id,
                        }
                
                employee_id=employee_obj.create(cr, uid, employee)

                if employee_id:
                    cr.execute('UPDATE res_partner SET employee=TRUE WHERE id=%s' % (partner_id))

                    #checks for the existence of a user associated to this partner
                    user_obj=self.pool.get('res.users')
                    
                    if not user_obj.search(cr, uid, [('partner_id','=',partner_id)]):

                        #check for the existence of a user with the same email
                        if partner_res.email and user_obj.search(cr, uid, [('email','=',partner_res.email)]):
                            raise osv.except_osv(_('Error!'), _("There's already a user using %s.\nIt will not be possible to create a user." % (partner_res.email)))
                        
                        #there's no user, so, we'll create one
                        user_exists=True
                        while user_exists:        
                            if partner_res.email:
                                user_login=partner_res.email
                            else:
                                user_login=str(uuid.uuid4())[:64]

                            user_exists=user_obj.search(cr, uid, [('login','=',user_login)])
                        
                        user_id=user_obj.create(cr, uid, {
                                                'partner_id' : partner_id,
                                                'company_id' : partner_res.company_id.id,
                                                'login'      : user_login,
                                                })
                                                
                        #now, we put the user in the employee
                        employee_obj.write(cr, uid, employee_id, {'user_id':user_id})
        return employee_id
        

    #check for the existance of an employee associated to the partner        
    def partner_has_employee(self, cr, uid, partner_id):
        employee_id=False
        
        if partner_id:
            #is there an employee whose user_id is related to the partner?
            
            partner_user=self.pool.get('res.users').search(cr, uid, [('partner_id','=',partner_id)])
            if partner_user:

                employee_id=self.pool.get('hr.employee').search(cr, uid, [('user_id','=',partner_user)])

                if employee_id:
                    if isinstance(employee_id,(list,tuple)):
                        employee_id=employee_id[0]
    
        #raise osv.except_osv(_('Error!'), _(employee_id))
        return employee_id

res_partner()


