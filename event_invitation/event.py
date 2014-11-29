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
  
  
        
    email_invitation_id = fields.Many2one(
            'email.template', string='Event invitation Email',
            domain=[('model_id.model','=','event.invitation.line')],
            help="If you set an email template, each member of the mailing list will receive this email announcing the event.")
    
    
    email_invitation_text = fields.Text(string='Text for invitation message', 
            help="Use this field to add text to the template's body.")
    
    email_invitation_allow_sending = fields.Boolean(string='Allow sending?', default=False)

    #these fields are used to send info to the template, whenever we're creating one
    default_invitation_email_template_name      = fields.Char(string='Default title for invitation email')
    default_invitation_email_template_subject   = fields.Char(string='Default subject for invitation email')
    default_invitation_email_template_body_html = fields.Char(string='Default text for invitation email')
    default_invitation_email_template_model     = fields.Integer(string='Default model for invitation email')
    
    #partners to invite (this is an auxiliary field)
    email_invitation_partner_ids = fields.Many2many('res.partner', string='Partners to invite', domain=[('email','!=',False),('opt_out','=',False)])
    
    email_invitation_partner_selection = fields.Selection([
                                                        ('use_template', 'Partners defined in the TEMPLATE'),
                                                        ('use_event', 'Partners defined in the EVENT'),
                                                        ('mix_event_template', 'Partners defined in the EVENT as well as in the TEMPLATE'),
                                                        ], string='Which selection to use?')
    
    email_invitation_partner_selection_replace = fields.Selection([
                                                        ('replace_template', 'REPLACE partners defined in the TEMPLATE'),
                                                        ('add_to_template', 'ADD TO partners defined in the TEMPLATE'),
                                                        ('do_nothing', 'Do nothing'),
                                                        ], string='Behaviour', default='add_to_template')


    
    count_invitations = fields.Char(string='Invitations', compute='_count_invitations')
    invitation_ids    = fields.One2many('event.invitation', 'event_id', string='Invitations')
    invitation_line_ids    = fields.One2many('event.invitation.line', 'event_id', string='Invitated partners')


    @api.one
    def button_count_invitations(self):
        return True


    @api.one
    @api.depends('invitation_ids')
    def _count_invitations(self):
        ok_sent_invitations=0
        for i in self.invitation_line_ids:
            if i.state and 'sent' in i.state:
                ok_sent_invitations+=1
        self.count_invitations = str(len(self.invitation_line_ids)) + ' (' + str(ok_sent_invitations) + ')'


    @api.onchange('email_invitation_partner_selection')
    def _onchange_email_invitation_partner_selection(self):
        if self.email_invitation_partner_selection in ['use_template']:
            self.email_invitation_partner_selection_replace='do_nothing'


    @api.onchange('type')
    def _onchange_type(self):
        aux=super(event_event,self)._onchange_type()
        if self.type:
            self.email_invitation_id = self.type.default_email_invitation.id or False
        return aux

        
        
    @api.onchange('email_invitation_id')
    def _onchange_email_invitation_id(self):
        if self.email_invitation_id:

            model_ids=self.pool.get('ir.model').search(self._cr, self._uid, [('model','=','event.event')])
            if isinstance(model_ids,(tuple,list)):
                model_ids=model_ids[0]
            self.default_invitation_email_template_model = model_ids

            self.default_invitation_email_template_subject = _('Event invitation') + ': ${object.type.name}, ${object.date_begin.split(' ')[0]}'
                
            self.default_invitation_email_template_body_html="""
Hi!<br/><br/>

We would very much like to invite you to attend the <b>${object.name}</b> ${object.type.name.lower()}.<br/>
It will be held from ${object.date_start.split(' ')[0]} to ${object.date_end.split(' ')[0]} at the following location<br/><br/>
${object.address_id and object.address_id.street or ''}<br/>
${object.address_id and object.address_id.street2 or ''}<br/>
${object.address_id and object.address_id.zip or ''} ${object.address_id and object.address_id.city or ''}<br/> 
${object.address_id and object.address_id.country_id and object.address_id.country_id.name or ''}<br/>
<br/><br/>
${object.email_invitation_text or ''}
"""
            self.default_invitation_email_template_name = _('Event invitation') + ' (' + (self.type and self.type.name or '') + ')'


    def str_to_list(self, txt):
        aux_list=[]
        if txt:
            if not isinstance(txt,list):
                aux_list_temp=txt.split(',')
            else:
                aux_list_temp=txt
                
            for l in aux_list_temp:
                l=int(l)
                if l not in aux_list:
                    aux_list.append(l)
        return aux_list

    @api.one
    def button_send_invitations(self):
    
        if self.email_invitation_id:
            template = self.email_invitation_id
            
            partners_to_invite = False
            sel=self.email_invitation_partner_selection
            
            mixed_list=''
            
            if sel=='use_template':
                partners_to_invite=template.partner_to
            else:
                #the partners defined in the event
                aux_list=[]
                for p in self.email_invitation_partner_ids:
                    aux_list.append(p.id)
                
                if sel=='mix_event_template' or self.email_invitation_partner_selection_replace=='add_to_template':
                    aux_list=self.str_to_list(template.partner_to) + aux_list
                    mixed_list=','.join(map(str,aux_list))
                    
                partners_to_invite=','.join(map(str,aux_list))

            
            if not partners_to_invite:
                raise osv.except_osv(
                                _('Error'),
                                _('No partners were indicated as recipients of the invitation message, neither in the email template nor in this event.'))
            
            
            """
            raise osv.except_osv(
                                _('Error'),
                                _(sel) + '\n\nTEMPLATE: ' + _(template.partner_to) + '\n\nEVENT: ' + _(self.email_invitation_partner_ids) + '\n\nRESULT: ' + _(partners_to_invite))
            """
            
            if partners_to_invite:
            
                
                invitation_id=self.pool.get('event.invitation').create(self._cr, self._uid, {
                                                                                'event_id'  : self.id,
                                                                                'send_type' : template.email_template_send_type,
                                                                                'text'      : self.email_invitation_text,
                                                                                })
                invitation_line_obj=self.pool.get('event.invitation.line')
                
            
                #we save the template's original partner list
                aux_list_temp=template.partner_to
                partners_list=self.str_to_list(partners_to_invite)
                
                error_msg=[]

                """
                The ideal thing would be to replace the email_template.send_mail method so that it would
                send messages individually. However, I was not able to override it properly.
                """
                #should we send individual messages?
                if template.email_template_send_type=='individual':
                    #we keep changing the template's partner list,
                    #as well as some auxiliary fields in the event
                    partner_obj=self.pool.get('res.partner')
                    for p in partners_list:
                        template.partner_to=p    
                        
                        partner_res=partner_obj.read(self._cr, self._uid, p, ['name','email'])
                        if isinstance(partner_res,(tuple,list)):
                            partner_res=partner_res[0]
                        
                        mail_message = template.send_mail(self.id)
                        if mail_message:
                            invitation_line_id=invitation_line_obj.create(self._cr, self._uid, {
                                                                                            'invitation_id'  : invitation_id,
                                                                                            'partner_id' : p,
                                                                                            })
                        else:
                            error_msg.append(p)
                else:
                    #we change the template's original partner list for the new one
                    template.partner_to=partners_to_invite
                    mail_message = template.send_mail(self.id)
                    
                    if mail_message:
                        for p in partners_list:
                            invitation_line_id=invitation_line_obj.create(self._cr, self._uid, {
                                                                                            'invitation_id'  : invitation_id,
                                                                                            'partner_id' : p,
                                                                                            })
                    else:
                        error_msg.append(partners_list)
                
                if not error_msg:
                    #we clean the auxiliary invitation list
                    self.email_invitation_partner_ids=False
                    
                    sel=self.email_invitation_partner_selection_replace
                    if sel=='do_nothing':
                        #we put everything as it was in the begining
                        template.partner_to=aux_list_temp
                        template.email_template_partner_ids=self.str_to_list(aux_list_temp)
                    elif sel=='add_to_template':
                        """
                        this is needed as the user might have chosen to use only the partners defined in the event
                        but still wants to add them to the template, a situation that might happen in the case of
                        a second invitation message to be sent
                        """
                        template.partner_to=mixed_list
                        template.email_template_partner_ids=self.str_to_list(mixed_list)
                    elif sel=='replace_template':
                        template.partner_to=','.join(map(str,partners_list))
                        template.email_template_partner_ids=partners_list
                    
                    """
                    raise osv.except_osv(
                                _('Error'),
                                _('Mixed: ') + _(mixed_list) + '\n\n' + _('Partners to invite: ') + partners_to_invite + '\n\n' + _('Template partner list was: ') + _(aux_list_temp) + '\n\n' + _('and became...') + _(template.partner_to))
                    """
                
                else:
                    #Something went wrong. We should put the template list as it was in the begining
                    template.partner_to=aux_list_temp
                    
                    if not isinstance(error_msg,(list)):
                        error_msg=[error_msg]
                    
                    partner_res=self.pool.get('res.partner').browse(self._cr, self._uid, error_msg)
                    partner_error=[]
                    for p in partner_res:
                        partner_error.append(p.name)
                    
                    raise osv.except_osv(_('Error'),_('Something might have gone wrong with these invitations:\n') + '\n'.join(partner_error))
                                
        self.email_invitation_allow_sending=False                    
                
    



class event_invitation(models.Model):
    _name='event.invitation' 
    _rec_name='date'
    
    """
    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        reads = self.read(cr, uid, ids, ['date','event_id'], context=context)
        res = []
        for record in reads:
            name = record['date']
            if record['event_id']:
                name = record['event_id'][1]+' / '+name
            res.append((record['id'], name))
        return res
    """
  
    event_id = fields.Many2one('event.event', string='Event', readonly=True)
    date     = fields.Datetime(string='Date', default=fields.Datetime.now(), readonly=True)
    send_type= fields.Char(string='Send type', readonly=True)
    text     = fields.Text(string='Message', help="This is the custom invitation message and not the template's.", readonly=True)
    line_ids = fields.One2many('event.invitation.line', 'invitation_id', string='Invitated partners', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', related='event_id.company_id',
                        store=True, readonly=True, states={'draft':[('readonly', False)]})  

class event_invitation_line(models.Model):
    _name='event.invitation.line'
    
    invitation_id = fields.Many2one('event.invitation', string='Invitation')
    partner_id    = fields.Many2one('res.partner', string='Partner')
    state         = fields.Char(string='State')
    date          = fields.Datetime(string='Date', default=fields.Datetime.now(), readonly=True)
    event_id      = fields.Many2one('event.event', related='invitation_id.event_id', string='Event', readonly=True, store=True)
    company_id = fields.Many2one('res.company', string='Company', related='event_id.company_id',
                        store=True, readonly=True, states={'draft':[('readonly', False)]})

class event_type(models.Model):
    _inherit='event.type' 
  
    default_email_invitation = fields.Many2one('email.template', string='Event Invitation Email',
                                    domain=[('model_id.model','=','event.invitation.line')],
                                    help="It will select this default invitation mail value when you choose this event")



class mail_mail(osv.Model):
    _inherit='mail.mail'
    
    
    def write(self, cr, uid, ids, vals, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]

        aux=super(mail_mail, self).write(cr, uid, ids, vals, context=context)

        for this in self.browse(cr, uid, ids):
            if 'state' in vals:
                #we write the state of the mail message to the invitation line
                if this.model=='event.invitation.line' and this.res_id:
                    self.pool.get('event.invitation.line').write(cr, uid, this.res_id, {
                                                                    'state' : this.state,
                                                                    'date' : datetime.datetime.now(),
                                                                    } )
        return aux


        