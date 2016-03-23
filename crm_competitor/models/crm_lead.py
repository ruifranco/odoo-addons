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


class crm_lead_competition(models.Model):
    
    _name   = 'crm.lead.competition'
    _order  = 'winner, value ASC'

    lead_id     = fields.Many2one('crm.lead','Oportunity', required=True)
    partner_id  = fields.Many2one('res.partner','Competitor', required=True, domain="[('competitor','=',True)]")
    value       = fields.Float('Value')
    note        = fields.Text('Note')
    winner      = fields.Boolean('Winner', readonly=True)


    _sql_constraints = [('partner_uniq', 'unique (lead_id,partner_id)', "There's already a proposal for this competitor!"),]


    @api.multi
    def name_get(self):
        result = []
        for s in self:
            result.append((s.id, "%s, %s" % (s.partner_id.name, s.value)))
        return result


    @api.depends('winner')
    @api.one
    def set_lead_winner(self):
        if self.winner:
            self._cr.execute("UPDATE crm_lead SET winner_id=%s", self.lead_id.id)




class crm_lead(models.Model):
    
    _inherit = 'crm.lead'

    competitor_ids  = fields.One2many('crm.lead.competition', 'lead_id', string='Competitors')
    winner_id       = fields.Many2one('res.partner', 'Winner', readonly=True)







class CrmLeadLost(models.TransientModel):
    
    _inherit = 'crm.lead.lost'

    winner_id = fields.Many2one('crm.lead.competition', 'Winner')
    
    @api.multi
    def action_lost_reason_apply(self):
        res = False
        for wizard in self:
            self.lead_id.lost_reason = self.lost_reason_id
            
            #set the winning competitor
            if self.winner_id:
                self._cr.execute("UPDATE crm_lead_competition SET winner=True WHERE id=%s" % self.winner_id.id)
                self._cr.execute("UPDATE crm_lead SET winner_id=%s WHERE id=%s" % (self.winner_id.partner_id.id, self.lead_id.id))
            
            res = self.lead_id.action_set_lost()
        return res    
