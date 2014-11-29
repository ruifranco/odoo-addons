# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Rui Pedrosa Franco All Rights Reserved
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

import logging

from openerp import addons
from openerp.osv import fields, osv
from openerp import tools
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


class hr_holidays(osv.osv):

    _inherit='hr.holidays'

    _columns = {
        'deadline_decision': fields.datetime('Decision deadline', states={'draft':[('readonly',False)], 'confirm':[('readonly',False)]}, select=True, help='Deadline for getting a decision on the leave request')
    }



    def send_reminders_requests_to_approve(self, cr, uid, type):
    
        """
        que pedidos existem por aprovar?
            ordenados por leave/alocation, COM data_limite (ASC), sem data_limite (date_from)
            
        deve indicar quantos dias faltam para a data limite
        
        email enviado para cada gestor
        """

        objH=self.pool.get('hr.holidays')
    
        requests_ids=objH.search(cr, uid, [('state','in',['confirm','validate1']),('type','=',type)])
            
        if requests_ids:
            requests_res=objH.browse(cr, uid, requests_ids)
             
            #who are the managers?
            managers_ids=[]
    
            for rec in requests_res:
                if rec.employee_id.parent_id:
                    if rec.employee_id.parent_id.work_email:
                        managers_ids.append(rec.employee_id.parent_id.id) 
            
            if managers_ids:
                """
                   INDICAR EM TODOS OS PEDIDOS, QUANDO É QUE FORAM CRIADOS E HÁ QUANTOS DIAS ESPERAM RESPOSTA
                """
                
               
                #for each manager found
                for m in self.pool.get('hr.employee').browse(cr, uid, [managers_ids]):
                    
                    mail_body=[]
                    
                    #we find the urgent requests
                    urgent_requests_ids=objH.search(cr, uid, [
                                                                ('id','in',requests_ids),
                                                                ('employee_id','in',m.child_ids),
                                                                ('deadline_decision','!=',False),
                                                                ],
                                                                order='deadline_decision ASC')
                        
                    if urgent_requests_ids:
                        urgent_requests_res=objH.browse(cr, uid, urgent_requests_ids)
                            
                        mail_body.append("REQUESTS WITH A DEADLINE")
                        for req in urgent_requests_res:
                            mail_body.append(req.employee_id.name + ', ' + req.date_from + ' - ' + req.date_to + ' (DEADLINE: ' + req.deadline_decision + ')')
                                 

                        
                    #we find the common requests
                    common_requests_ids=objH.search(cr, uid, [
                                                                ('id','in',requests_ids),
                                                                ('employee_id','in',m.child_ids),
                                                                ('deadline_decision','=',False),
                                                                ],
                                                                order='date_from ASC')
                    
                    if common_requests_ids:
                        common_requests_res=objH.browse(cr, uid, common_requests_ids)
                            
                        mail_body.append("GENERAL REQUESTS")
                        for req in common_requests_res:
                            mail_body.append(req.employee_id.name + ', ' + req.date_from + ' - ' + req.date_to)


                    #Send mail

                    mail_subject='Holiday requests to be approved'
                    mail_body_txt=str(mail_body)

                
                    ir_mail_server = self.pool.get('ir.mail_server')
                    msg = ir_mail_server.build_email(m.company_id.email, m.work_email, mail_subject, mail_body_txt)
                    
                    
                    msg = ir_mail_server.build_email('rui.franco@gmail.com', 'setecolinas@gmail.com', 'teste', 'maria')
                    _logger.debug(str(msg))
                    
                    res_email = ir_mail_server.send_email(cr, uid, msg)
                    if res_email:
                        _logger.debug('Email successfully sent to: %s', m.work_email)
                        _logger.info('Email successfully sent to: %s', m.work_email)
                    else:
                        _logger.warning('Failed to send email to: %s', m.work_email)
                        _logger.debug('Failed to send email to: %s', m.work_email)


        return True

hr_holidays()

