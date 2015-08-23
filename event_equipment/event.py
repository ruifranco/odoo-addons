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


class event_type(models.Model):
    _inherit='event.type' 

    equipment_host_ids = fields.Many2many('product.equipment',
        'product_equipment_event_type_host_rel', 'equipment_id', 'event_type_id', string='Equipment list (host)')
        
    equipment_participants_ids = fields.Many2many('product.equipment',
        'product_equipment_event_type_participants_rel', 'equipment_id', 'event_type_id', string='Equipment list (participants)')

    equipment_host_ids_text = fields.Char('Equipment lists (host)', compute='_get_equipment_host_lists')
    equipment_participants_ids_text = fields.Char('Equipment lists (participants)', compute='_get_equipment_participants_lists')
    
    @api.one
    @api.onchange('equipment_host_ids')
    def _get_equipment_host_lists(self):
        aux=[]
        for e in self.equipment_host_ids:
            aux.append(e.name)
        self.equipment_host_ids_text='\n'.join(aux)

    @api.one
    @api.onchange('equipment_participants_ids')
    def _get_equipment_participants_lists(self):
        aux=[]
        for e in self.equipment_participants_ids:
            aux.append(e.name)
        self.equipment_participants_ids_text='\n'.join(aux)


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
    @api.onchange('type')
    def load_event_type_lists(self):
        if self.type:
            eq=[]
            for eql in self.type.equipment_host_ids:
                for l in eql.equipment_lines:
                    eq.append({
                        'categ_id'  : l.categ_id.id,
                        'qty'       : l.qty,
                        'mandatory' : l.mandatory,
                        'notes'     : l.notes,
                        })
            self.equipment_host_id=False            
            self.equipment_host_ids=eq            

            eq=[]
            for eql in self.type.equipment_participants_ids:
                for l in eql.equipment_lines:
                    eq.append({
                        'categ_id'  : l.categ_id.id,
                        'qty'       : l.qty,
                        'mandatory' : l.mandatory,
                        'notes'     : l.notes,
                        })
            self.equipment_participants_id=False            
            self.equipment_participants_ids=eq            


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
    
    #to be used with the @api
    def _get_partner_equipment(self, cr, uid, partner_id):
        return self.pool.get('res.partner')._get_partner_equipment(cr, uid, partner_id)


    def create(self, cr, uid, data, context=None):
        if 'partner_id' in data:
            #we create the equipment lines in the partner's record
            event_res=self.pool.get('event.event').browse(cr, uid, data['event_id'])
            
            #we create the equipment lines for the partner
            partner_equip=self.pool.get('res.partner')._get_partner_equipment(cr, uid, data['partner_id'])
            for ev in event_res:
                for eqp in ev.equipment_participants_ids:
                    equip_found=False
                    for pequip in partner_equip:
                        if pequip[0]==eqp.categ_id.id:
                            equip_found=True
                            break
                    
                    if not equip_found:
                        self.pool.get('res.partner.equipment').create(cr, uid, {
                                         'partner_id': data['partner_id'],
                                         'categ_id'  : eqp.categ_id.id,
                                         'qty'       : 0,
                                         })

        return super(event_registration, self).create(cr, uid, data, context)



    @api.one
    def check_lacking_equipment_partner(self):
        lacking_equipment=[]
    
        if self.event_id.equipment_participants_ids and self.partner_id:
            partner_equip=self._get_partner_equipment(self.partner_id.id)

            #for each line of equipment defined for this event...
            for eqp in self.event_id.equipment_participants_ids:
                
                equip_found=False
                
                #does the participant have enough quantity?
                for pequip in partner_equip:
                    if pequip[0]==eqp.categ_id.id:
                        if pequip[1]<eqp.qty:
                            diff=eqp.qty-pequip[1]
                            lacking_equipment.append((eqp.categ_id.id, diff))
                        equip_found=True
                        break
                
                if not equip_found:
                    lacking_equipment.append((eqp.categ_id.id, eqp.qty))

        return lacking_equipment


    #converts a list of lacking equipment to text 
    def build_list_lacking_equipment(self, lacking_equipment):
        if lacking_equipment:
            res=[]
            
            for eq in lacking_equipment:
                categ_name=self.pool.get('product.category').name_get(self._cr, self._uid, eq[0])
                if isinstance(categ_name,(list,tuple)):
                    categ_name=categ_name[0]
                    if isinstance(categ_name,(list,tuple)):
                        categ_name=categ_name[1]

                res.append(categ_name + ' => ' + str(eq[1]))
                
            aux='\n'.join(res)
            res=aux    
        else:
            res=''
    
        return res
        
        
    @api.one
    def show_lacking_equipment_partner(self):
        lacking_equipment=self.check_lacking_equipment_partner()
        if isinstance(lacking_equipment,(list)):
            lacking_equipment=lacking_equipment[0]
        
        if lacking_equipment:
            aux=self.build_list_lacking_equipment(lacking_equipment)
            msg=_('%s is lacking:') % _(self.partner_id.name)
            raise osv.except_osv(_('Equipment check!'), msg + '\n\n' + _(aux))
        else:
            raise osv.except_osv(_('Equipment check!'),_('%s lacks no equipment') % _(self.partner_id.name))
            