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


class res_users(osv.osv):
    _inherit = 'res.users'

    def random_password(self, cr, uid):
        characters = string.ascii_letters + string.punctuation  + string.digits
        return "".join(choice(characters) for x in range(randint(8, 16)))

res_users()


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
        
        if partner_id:
            res=self.browse(cr, uid, partner_id)
            if res:
                objE=self.pool.get('hr.employee')
                
                employee={
                        'name'              : res.name,
                        'country_id'        : res.country_id.id,
                        'image'             : res.image,
                        'work_email'        : res.email,
                        'address_home_id'   : partner_id,
                        }

                employee_id=objE.create(cr, uid, employee)

                if employee_id:
                    cr.execute('UPDATE res_partner SET employee=TRUE WHERE id=%s' % (partner_id))

        return employee_id
        

    #check for the existance of an employee associated to the partner        
    def partner_has_employee(self, cr, uid, partner_id):
        employee_id=False
        
        if partner_id:
            employee_id=self.pool.get('hr.employee').search(cr, uid, [('address_home_id','=',partner_id)])
            if employee_id:
                if isinstance(employee_id,(list,tuple)):
                    employee_id=employee_id[0]
    
        return employee_id

res_partner()


class hr_employee(osv.osv):
    _inherit = 'hr.employee'


    def create_user_from_employee(self, cr, uid, employee_id=False):
        user_id=False
        
        if employee_id:
            res=self.browse(cr, uid, employee_id)
            if res:
            
                objU=self.pool.get('res.users')
            
                user={
                    'name'      : res.name,
                    'company_id': res.company_id.id,
                    'image'     : res.image,
                    }        

                #what shall be the user login?
                user_exists=True
                while user_exists:        
                    if res.work_email:
                        user['login']=user['email']=res.work_email
                    else:
                        user['login']=str(uuid.uuid4())[:64]

                    user_exists=objU.search(cr, uid, [('login','=',user['login'])])

                
                #the user's language becomes the same as the company's
                if res.company_id.partner_id:
                    if res.company_id.partner_id.lang:
                        user['lang']=res.company_id.partner_id.lang

                user['password']=objU.random_password(cr, uid)

                user_id=objU.create(cr, uid, user)
        
        return user_id
    

    def create(self, cr, uid, vals, context=None):
        employee_id=super(hr_employee, self).create(cr, uid, vals, context=context)
        
        user_id=self.create_user_from_employee(cr, uid, employee_id)
        if user_id:
            self.write(cr, uid, employee_id, {'user_id':user_id})
        
        return employee_id
    
hr_employee()

