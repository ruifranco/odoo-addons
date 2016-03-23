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


class res_partner(models.Model):
    
    _inherit = 'res.partner'
    
    competitor = fields.Boolean(string='Competitor')


    @api.multi
    def call_won_leads(self):
        
        order_ids = self.get_won_leads(self.id)
        
        if order_ids:
            return {
                    'name'      : _('Won opportunities'),
                    'type'      : 'ir.actions.act_window',
                    'view_type' : 'form',
                    'view_mode' : 'tree,form',
                    'res_model' : 'crm.lead',
                    'domain'    : ['|',('active','=',True),('active','=',False),('id', 'in', order_ids)],
                    'context'   : {},
                    }
        else:
            return True


    @api.multi
    def get_won_leads(self, partner_id=False):
        res = []
   
        if partner_id:
            lead_ids = self.env['crm.lead'].search([
                                                    ('winner_id','=',partner_id),
                                                    ('active','=',False),
                                                    ])
            
            if lead_ids:
                for l in lead_ids:
                    if l.id not in res:
                        res.append(l.id)

        return res

    @api.one
    def _get_won_leads_counter(self):
        self.won_leads_count = len(self.get_won_leads(self.id))
        
        
    won_leads_count = fields.Integer(string='won_leads', compute=_get_won_leads_counter, readonly=True)
        
        