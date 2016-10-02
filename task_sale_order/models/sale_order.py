#! -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Odooveloper (Rui Pedrosa Franco) All Rights Reserved
#    http://www.odooveloper.com
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

from openerp import models, fields, api, _
import math


class sale_order(models.Model):
    _inherit = 'sale.order'
    
    @api.multi
    @api.depends('tasks_ids')
    def _get_task_completion(self):
        for s in self:
            done = 0
            if s.tasks_ids:
                #mind the name!!! (taskS_ids)
                for t in s.tasks_ids:
                    if t.stage_id.closed:
                        done += 1 
                if done:
                    res = math.ceil((done * 100)/len(s.tasks_ids))
                else:
                    res = 0
            else:
                res = 100
            s.task_completion = res
    
    task_completion = fields.Integer('Task completion', 
                                   compute='_get_task_completion',
                                   help="Percentage of tasks with a stage that is considered as a closing one")



class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    so_tasks_count = fields.Integer('SO task count', related='order_id.tasks_count')
    task_ids = fields.One2many('project.task', 'sale_line_id', 'Tasks')
    
    @api.multi
    @api.depends('task_ids')
    def _get_task_completion(self):
        for s in self:
            done = 0
            if s.task_ids:
                for t in s.task_ids:
                    if t.stage_id.closed:
                        done += 1 
                if done:
                    res = math.ceil((done * 100)/len(s.task_ids))
                else:
                    res = 0
            else:
                res = 100
            s.task_completion = res

    task_completion = fields.Integer('Task completion', 
                                   compute='_get_task_completion',
                                   help="Percentage of tasks with a stage that is considered as a closing one")
    
    