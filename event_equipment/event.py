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
from openerp.osv import orm
from openerp import models, fields, api, _
from openerp import tools



class event_event(models.Model):
    _inherit='event.event' 

    type                        = fields.Many2one('event.type',string='Type of Event', required=True, readonly=False, states={'done': [('readonly', True)]})

    equipment_host_id           = fields.Many2one('product.equipment',string='Equipment list (host)', help='What kind of equipment does the host need?')
    equipment_host_ids          = fields.One2many('event.equipment.lines_host', 'event_id', string='Equipment (host)')
    equipment_host_text         = fields.Text(string='Equipment')

    equipment_participants_id   = fields.Many2one('product.equipment',string='Equipment list (participants)', help='What kind of equipment should the participants bring?')
    equipment_participants_ids  = fields.One2many('event.equipment.lines_participants', 'event_id', string='Equipment (participants)')
    equipment_participants_text = fields.Text(string='Equipment')
  
  
    @api.one
    def _get_equipment_text(self, field):
    
        if field=='participants':
            values=self.equipment_participants_ids
        else:
            values=self.equipment_host_ids

        fsep = '|'
        lsep = '\n'

        aux=_('Category') + fsep + _('Quantity') + fsep + _('Mandatory') + fsep + _('Comments') + lsep
        for l in values:
            categ_name=self.pool.get('product.category').name_get(self._cr, self._uid, l.categ_id.id)
            if isinstance(categ_name,(list,tuple)):
                categ_name=categ_name[0]
                if isinstance(categ_name,(list,tuple)):
                    categ_name=categ_name[1]
                
            aux+=_(categ_name) + fsep + str(l.qty) + fsep + _(l.mandatory) + fsep + _(l.notes) + lsep
    
        if not values:
            aux=False
    
        if field=='participants':
            self.equipment_participants_text=aux
        else:
            self.equipment_host_text=aux
        
        
    @api.one
    @api.onchange('equipment_host_ids')
    def _call_get_equipment_text_host(self):
        self._get_equipment_text('host')

    @api.one
    @api.onchange('equipment_participants_ids')
    def _call_get_equipment_text_participants(self):
        self._get_equipment_text('participants')


    @api.one
    def button_load_host_equipment_list(self):
        eq=[]
        if self.equipment_host_id and self.equipment_host_id.equipment_lines:
            for l in self.equipment_host_id.equipment_lines:
                eq.append({
                    'categ_id'  : l.categ_id.id,
                    'qty'       : l.qty,
                    'mandatory' : l.mandatory,
                    'notes'     : l.notes,
                    })
        self.equipment_host_id=False            
        self.equipment_host_ids=eq            
  
    @api.one
    def button_load_participants_equipment_list(self):
        eq=[]
        if self.equipment_participants_id and self.equipment_participants_id.equipment_lines:
            for l in self.equipment_participants_id.equipment_lines:
                eq.append({
                    'categ_id'  : l.categ_id.id,
                    'qty'       : l.qty,
                    'mandatory' : l.mandatory,
                    'notes'     : l.notes,
                    })
        self.equipment_participants_id=False            
        self.equipment_participants_ids=eq            
  
  
  
  
  
class event_equipment_lines(models.Model):
    _name='event.equipment.lines'

    event_id  = fields.Many2one('event.event',string='Event', required=True)
    categ_id  = fields.Many2one('product.category',string='Category', required=True)
    qty       = fields.Integer(string='Quantity', required=True, default=1)    
    mandatory = fields.Boolean(string='Mandatory')
    notes     = fields.Char(string='Comments', size=255)        
    checked   = fields.Boolean(string='Checked')    
    type      = fields.Selection([('participant','Participant'),('host','Host')],'Type', select=True)

  
class event_equipment_lines_host(models.Model):
    _name='event.equipment.lines_host'
    _inherit='event.equipment.lines'

    type = fields.Selection([('participant','Participant'),('host','Host')],'Type', default='host')


class event_equipment_lines_participants(models.Model):
    _name='event.equipment.lines_participants'
    _inherit='event.equipment.lines'

    type = fields.Selection([('participant','Participant'),('host','Host')],'Type', default='participant')






class event_registration(orm.Model):
    _inherit = 'event.registration'
    
    def create(self, cr, uid, data, context=None):
        if 'partner_id' in data:
            #we create the equipment lines in the partner's record
            event_res=self.pool.get('event.event').browse(cr, uid, data['event_id'])
            
            #we load the equipment the partner has
            partner_equip=[]
            partner_equip_obj=self.pool.get('res.partner.equipment')
            partner_equip_ids=partner_equip_obj.search(cr, uid, [('partner_id','=',data['partner_id'])])
            if partner_equip_ids:
                partner_equip_res=partner_equip_obj.browse(cr, uid, partner_equip_ids)
                for peq in partner_equip_res:
                    partner_equip.append(peq.categ_id.id)
            
            #we create the equipment lines for the partner
            for ev in event_res:
                for eqp in ev.equipment_participants_ids:
                    if eqp.categ_id.id not in partner_equip:
                        partner_equip_obj.create(cr, uid, {
                                         'partner_id': data['partner_id'],
                                         'categ_id'  : eqp.categ_id.id,
                                         'qty'       : 0,
                                         })
            
        return super(event_registration, self).create(cr, uid, data, context)
