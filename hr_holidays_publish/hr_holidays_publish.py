# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Rui Pedrosa Franco All Rights Reserved
#    http://pt.linkedin.com/in/ruipedrosafranco
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import SUPERUSER_ID, models, api, fields, _
from openerp.exceptions import except_orm, Warning, RedirectWarning


class hr_employee(models.Model):
    _inherit='hr.employee'
    
    holidays_publish_ids = fields.One2many(comodel_name='hr.holidays.publish', 
                                             inverse_name='employee_id', string='Leaves', help='Who should be able to see your leaves?')


    
    
class hr_holidays_publish(models.Model):
    _name       ='hr.holidays.publish'
    _description='Holidays publish'
    _rec_name   ='employee_id'

    @api.one
    def _get_default_employee(self):
        employee_ids=self.env['hr.employee'].search([('user_id','!=',False),('user_id','=',self._uid)])
        if len(employee_ids)==1:
            return employee_ids.id
        else:
            return False
        
    
    employee_id     = fields.Many2one('hr.employee', string='Employee', required=True, default=_get_default_employee)
    user_id         = fields.Many2one('res.users', string='User', related='employee_id.user_id')
    status_id       = fields.Many2one('hr.holidays.status', string='Leave Type')
    visibility      = fields.Selection([('everyone','Everyone'),('department','Same department')], string='Visibility')
    approved_only   = fields.Boolean(string='Only publish approved leaves?', default=True)
    workmate_id     = fields.Many2one('hr.employee', string='Workmate')
    workmate_user_id= fields.Many2one('res.users', string='User', related='workmate_id.user_id', store=True)
    



    def redefine_rules(self, cr, uid, employee_id, context={}):
        rule_obj=self.pool.get('ir.rule')

        aux_name='hr_holidays_publish_leave_'

        args_search=[]
        args_search.append(('name','ilike',aux_name))
        aux="('employee_id.id', '=', " + str(employee_id) + ")" #spaces are vital
        args_search.append(('domain_force','ilike',aux))
        rule_ids=rule_obj.search(cr, uid, args_search)
        if rule_ids:
            rule_obj.unlink(cr, SUPERUSER_ID, rule_ids)

        model_id=self.pool.get('ir.model').search(cr, uid, [('model','=', 'hr.holidays')])
        if isinstance(model_id, (list,tuple)):
            model_id=model_id[0]
        
        #create new rule
        conf_obj=self.pool.get('hr.holidays.publish')
        employee_rule_ids=conf_obj.search(cr, uid, [('employee_id','=',employee_id)])
        group_id=self.pool.get('res.groups').search(cr, uid, [('name','=','Employee')])

        for r in conf_obj.browse(cr, uid, employee_rule_ids):
            domain_force=[]
            domain_force.append(('employee_id','!=',False))
            domain_force.append(('employee_id.id','=',r.employee_id.id))
            
            if r.status_id:
                domain_force.append(('holiday_status_id','=',r.status_id.id))

            if r.visibility == 'department':
                domain_force.append(('employee_id.department_id','!=',False))
                domain_force.append(('employee_id.department_id.id','in','aux_user_id'))

            if r.workmate_id:
                domain_force.append(('employee_id.id','in','aux_user_id2'))

            if r.approved_only:
                domain_force.append(('state','=','validate'))


            aux_domain_force=','.join(map(str,domain_force)).replace("'aux_user_id'",'[user.department_ids]')
            aux_domain_force=aux_domain_force.replace("'aux_user_id2'",'[x.employee_id.id for x in user.publish_leaves_users]')

            vals={
                  'model_id'    : model_id,
                  'domain_force': aux_domain_force,
                  'name'        : aux_name + str(r.id),
                  'groups'      : [(6,0,group_id)],
                  'perm_read'   : True,
                  'perm_create' : False,
                  'perm_write'  : False,
                  'perm_unlink' : False,
                  }
            rule_obj.create(cr, SUPERUSER_ID, vals)

        return True
    

    @api.onchange('workmate_id')
    def onchange_workmate_id(self, context={}):
        if self.workmate_id:
            self.visibility=False
            
    
    @api.onchange('visibility')
    def onchange_visibility(self, context={}):
        if self.visibility:
            self.workmate_id=False


    def create(self, cr, uid, vals, context=None):

        if vals.get('workmate_id'):
            count=self.search_count(cr, uid, [
                                              ('employee_id','=',vals['employee_id']),
                                              ('workmate_id','!=',False)
                                              ])
            if count>=10:
                raise except_orm(_('Error'),_('You can only set 10 rules for specific workmates.'))
                
        aux=super(hr_holidays_publish, self).create(cr, SUPERUSER_ID, vals, context=context)
        self.redefine_rules(cr, uid, vals['employee_id'])
        return aux 


    def write(self, cr, uid, ids, vals, context=None):

        if isinstance(ids,(tuple,list)):
            ids=ids[0]

        if 'workmate_id' in vals:
            if vals.get('workmate_id',False):
                this=self.browse(cr, uid, ids)
                
                count=self.search_count(cr, uid, [
                                                  ('employee_id','=',this.employee_id.id),
                                                  ('workmate_id','!=',False)
                                                  ])
                if count>=10:
                    raise except_orm(_('Error'),_('You can only set 10 rules for specific workmates.'))
        
        aux=super(hr_holidays_publish, self).write(cr, SUPERUSER_ID, ids, vals, context=context)
        for i in self.browse(cr, uid, ids):
            self.redefine_rules(cr, uid, i.employee_id.id)
        return aux 


    def unlink(self, cr, uid, ids, context=None):
        employee_ids=[]
        for i in self.browse(cr, uid, ids):
            employee_ids.append(i.employee_id.id)
        aux=super(hr_holidays_publish, self).unlink(cr, uid, ids, context=context)
        for employee_id in employee_ids:
            self.redefine_rules(cr, uid, employee_id)
        return aux 



class res_users(models.Model):
    _inherit='res.users'

    
    @api.one
    def get_departments(self):
        aux=[]
        for emp in self.employee_ids:
            if emp.department_id:
                if emp.department_id.id not in aux:
                    aux.append(emp.department_id.id)
        if aux:
            self.department_ids=','.join(map(str,aux))
        else:
            self.department_ids=False


    department_ids = fields.Char(string='Departments', compute='get_departments')

    #employees (users) who have allowed this user to see their leaves
    publish_leaves_users        = fields.One2many(comodel_name='hr.holidays.publish', inverse_name='workmate_user_id')
