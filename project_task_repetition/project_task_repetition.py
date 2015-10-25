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

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import datetime
from dateutil.relativedelta import relativedelta
from calendar import monthrange
import sys

import logging
_logger = logging.getLogger(__name__)


class project_task(models.Model):
    _inherit = 'project.task'
    
    
    ptr_parent_id = fields.Many2one('project.task', string='Parent task', 
                                        help='Task from which this one originated', readonly=True)

    ptr_child_ids = fields.One2many('project.task', 'ptr_parent_id', 'Child tasks', 
                                        help='Tasks originated from this one') 


    @api.one
    def ptr_get_has_sisters(self):
        res=False
        if self.ptr_parent_id:
            if self.search([('ptr_parent_id', '=', self.ptr_parent_id.id)], limit=1):
                res = True
        self.ptr_has_sisters = res

    ptr_has_sisters = fields.Boolean('Has sisters?', compute=ptr_get_has_sisters)


    def ptr_call_repetition_wizard(self, cr, uid, ids, context):
        
        if isinstance(ids,(tuple,list)):
            ids=ids[0]
        
        return {
                'view_type' : 'form',
                'view_mode' : 'form',
                'view_id'   : False,
                'res_model' : 'project.task.repetition.wizard',
                'type'      : 'ir.actions.act_window',
                'target'    : 'new',
                'context'   : {'default_task_id':ids},
            }    

        
    @api.one
    def ptr_delete_child_tasks(self):
        if self.ptr_child_ids:
            
            date_now = (datetime.datetime.now()).replace(hour=0, minute=0, second=0, microsecond=0)
            
            for t in self.ptr_child_ids:
                if datetime.datetime.strptime(t.date_deadline, "%Y-%m-%d") > date_now:
                    try:
                        self.pool.get('project.task').unlink(self._cr, self._uid, [t.id])
                    except:
                        _logger.error(str(sys.exc_info()[0]))

        return True

        
    @api.one
    def ptr_delete_sister_tasks(self):
        if self.ptr_parent_id:
            sister_ids=self.search_read([
                                    ('ptr_parent_id','!=',False),
                                    ('ptr_parent_id','=',self.ptr_parent_id.id),
                                    ('id','!=',self.id)
                                    ])
            
            date_now = (datetime.datetime.now()).replace(hour=0, minute=0, second=0, microsecond=0)
            
            for t in sister_ids:
                if datetime.datetime.strptime(t['date_deadline'], "%Y-%m-%d") > date_now:
                    try:
                        self.pool.get('project.task').unlink(self._cr, self._uid, [t['id']])
                    except:
                        _logger.error(str(sys.exc_info()[0]))

        return True



        

class project_task_repetition_wizard(models.TransientModel):
    _name = 'project.task.repetition.wizard'


    DAYS_IN_MONTH = []
    for x in range(0, 31):
        aux_day=x+1
        DAYS_IN_MONTH.append((aux_day,str(aux_day)))
  
  
    task_id         = fields.Many2one('project.task', string='Original task', readonly=True)
    interval        = fields.Integer('Interval', required=True, default=1)
    rrule_type      = fields.Selection([('daily', 'Day(s)'), ('weekly', 'Week(s)'), ('monthly', 'Month(s)'), ('yearly', 'Year(s)')], 'Period', required=True)
    end_type        = fields.Selection([('count', 'Number of repetitions'), ('end_date', 'End date')], 'Until', required=True, default='count')
    count           = fields.Integer('Count', required=True, default=1)
    mo              = fields.Boolean('Mon')
    tu              = fields.Boolean('Tue')
    we              = fields.Boolean('Wed')
    th              = fields.Boolean('Thu')
    fr              = fields.Boolean('Fri')
    sa              = fields.Boolean('Sat')
    su              = fields.Boolean('Sun')
    month_by        = fields.Selection([('date', 'Date of month'), ('day', 'Day of month')], 'Option')
    day             = fields.Selection(DAYS_IN_MONTH,'Date of month')
    week_list       = fields.Selection([('mo', 'Monday'), ('tu', 'Tuesday'), ('we', 'Wednesday'), ('th', 'Thursday'), ('fr', 'Friday'), ('sa', 'Saturday'), ('su', 'Sunday')], 'Weekday')
    byday           = fields.Selection([('1', 'First'), ('2', 'Second'), ('3', 'Third'), ('4', 'Fourth'), ('5', 'Fifth'), ('-1', 'Last')], 'By day')
    change_date     = fields.Selection([('next_day', 'Next available day'), ('previous_day', 'Previous available day') ], 'Change date (if it is invalid)', default='previous_day')
    final_date      = fields.Date('Repeat Until')
    


    def create_task(self, task_id, deadline):
        
        new_id=False
        if task_id and deadline:
            #we create a copy of the task but with the new deadline
            vals={
                  'name'            : task_id.name,
                  'date_deadline'   : deadline, 
                  'ptr_parent_id'   : task_id.id,
                  'date_start'      : deadline,
                  }
            try:
                new_id = self.pool.get('project.task').copy(self._cr, self._uid, task_id.id, default=vals, context=self._context)
            except:
                _logger.error(str(sys.exc_info()[0]))

        return new_id


    def calculate_date(self, date=False, unit=False, amount=0):
        res_date = False

        if date and unit:
            res_date = date
            
            if unit=='daily':
                res_date += relativedelta(days=amount)
            elif  unit=='weekly':
                res_date += relativedelta(weeks=amount)
            elif  unit=='monthly':
                res_date += relativedelta(months=amount)
            elif  unit=='yearly':
                res_date += relativedelta(years=amount)
        
        return res_date

    #If final_date is required but no value was received, let's make some calculations
    def get_default_final_date(self, unit, interval, count):

        res_date = datetime.date.today()
        
        units_to_add = interval * count

        if unit=='daily':
            res_date += relativedelta(days=units_to_add)
        elif  unit=='weekly':
            res_date += relativedelta(weeks=units_to_add)
        elif  unit=='monthly':
            res_date += relativedelta(months=units_to_add)
        elif  unit=='yearly':
            res_date += relativedelta(years=units_to_add)
        
        #so that we don't get stuck in a comparison
        res_date += relativedelta(days=1)
        res_date = datetime.datetime.strptime(str(res_date), "%Y-%m-%d")
        
        return res_date


    @api.one
    def create_repetition(self):
        
        #date of the original task deadline
        deadline = self.task_id.date_deadline 
        if deadline:
            deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d")
        else:
            deadline = datetime.datetime.now()

        
        deadline    = deadline.replace(hour=0, minute=0, second=0, microsecond=0)
        final_date  = self.final_date and datetime.datetime.strptime(self.final_date, "%Y-%m-%d")


        days = ['mo','tu','we','th','fr','sa','su']
        if self.rrule_type == 'weekly':
            days_chosen = False
            for d in days:
                if eval('self.' + d):
                    days_chosen = True
                    break
        else:
            days_chosen = False

        
        #We take the initial date and for COUNT times we add INTERVAL RRULE_TYPE
        for x in range(0, self.count):

            date_ok = True

            if (
                self.rrule_type in ['daily', 'yearly'] 
                or (self.rrule_type == 'weekly' and not days_chosen)
                or (self.rrule_type == 'monthly' and not self.month_by)
                ):
                
                if self.end_type == 'count':
                    deadline = self.calculate_date(deadline, self.rrule_type, self.interval)
                    self.create_task(self.task_id, deadline)
                else:
                    while date_ok:
                        deadline = self.calculate_date(deadline, self.rrule_type, self.interval)
                        if deadline <= final_date:  
                            self.create_task(self.task_id, deadline)
                        else:
                            date_ok = False


            elif (self.rrule_type == 'monthly' and self.month_by):

                #Every INTERVAL months, on day DAY, we create a task
                if self.month_by == 'date':
                    """
                    In this case, we don't start calculations by adding months to the original deadline.
                    We just go to the "next" month and, there, create the task on the chosen day.
                    """
                    date_ok=True
                    if not final_date:
                        final_date = self.get_default_final_date(self.rrule_type, self.interval, self.count)

                    while date_ok:
                        deadline = self.calculate_date(deadline, self.rrule_type, self.interval)
    
                        if deadline <= final_date:
                            
                            this_date_ok= False
                            aux_date    = deadline
                            chosen_day  = self.day
                                    
                            while not this_date_ok:
                                try:
                                    aux_date = datetime.date(aux_date.year, aux_date.month, chosen_day)
                                    this_date_ok = True
                                except:
                                    if self.change_date == 'previous_day':
                                        chosen_day-=1
                                    else:
                                        if chosen_day<31:
                                            chosen_day+=1
                                        else:
                                            chosen_day=1
                                            aux_date = deadline+relativedelta(months=1)
                                         
                                    this_date_ok = False
                                            
                            self.create_task(self.task_id, aux_date)
                        else:
                            date_ok = False
                            
                else:
                    #Specific weekdays
                    date_ok=True
                    if not final_date:
                        final_date = self.get_default_final_date(self.rrule_type, self.interval, self.count)
                        
                        
                    while date_ok:
                        deadline = self.calculate_date(deadline, self.rrule_type, self.interval)
                               
                        if deadline <= final_date:
                            #Let's get the list of dates for the required weekday
                            aux_weekday = days.index(self.week_list)
                            aux_days = []
                            for d in range(0, monthrange(deadline.year, deadline.month)[1]):
                                aux_date = datetime.date(deadline.year, deadline.month, d+1)
                                if aux_date.weekday() == aux_weekday: 
                                    aux_days.append(aux_date)
                                    
                            if self.byday == '-1':
                                aux_by_day = -1
                            else:
                                aux_by_day = int(self.byday)-1
                                    
                            aux_deadline=aux_days[aux_by_day]
        
                            self.create_task(self.task_id, aux_deadline)
                        else:
                            date_ok = False

            elif self.rrule_type == 'weekly' and days_chosen:
                
                #We add INTERVAL weeks to the last date and create a task on each chosen weekday
                date_ok=True
                while date_ok:
                    deadline = self.calculate_date(deadline, self.rrule_type, self.interval)
                    deadline_weekday = deadline.weekday()

                    if (
                        (self.end_type !=' count' and final_date and deadline <= final_date) 
                        or self.end_type == 'count'
                        ):

                        for d in range(0, len(days)):
                            aux_deadline = deadline
                            if eval('self.' + days[d]):
                                if deadline_weekday<=d:
                                    days_to_add = (d-deadline_weekday)
                                else:
                                    days_to_add = 7-(deadline_weekday-d)
                                aux_deadline += relativedelta(days=days_to_add)
                                self.create_task(self.task_id, aux_deadline)
                            
                        if self.end_type == 'count':
                            date_ok = False
                    else:
                        date_ok = False
                
        return True

