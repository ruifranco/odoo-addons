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
import datetime


class event_event(models.Model):
    _inherit='event.event' 

    project_work_ids = fields.One2many('project.task.work','event_id','Work')

    count_work = fields.Char(string='Work', compute='_count_work')
    
      
    @api.one
    def button_count_work(self):
        return True


    @api.one
    @api.depends('project_work_ids')
    def _count_work(self):
        people_worked=[]
        time_spent=0
        for i in self.project_work_ids:
            time_spent += i.hours 
            if i.user_id.id not in people_worked:
                people_worked.append(i.user_id.id)

        self.count_work = str(len(people_worked)) + ' (' + str(time_spent) + ')'

