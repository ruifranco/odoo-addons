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
from openerp.osv import osv, fields, orm
from openerp import models, api, _
from openerp import tools
import datetime

class project_task_work(orm.Model):
    _inherit = 'project.task.work'

    _columns={
        'event_id'   : fields.many2one('event.event','Event'),
    }  
       


class project_task(orm.Model):
    _inherit = 'project.task'

    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        reads = self.read(cr, uid, ids, ['name','project_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if context.get('event_work',False) and record['project_id']:
                name = record['project_id'][1]+' / '+name
            res.append((record['id'], name))
        return res
    