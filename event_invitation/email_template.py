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

import openerp
from openerp.osv import osv, fields, orm
from openerp import tools, api
from openerp.tools.translate import _


class email_template(orm.Model):
    _inherit = 'email.template'

    _columns = {
        'email_template_partner_ids' : fields.many2many('res.partner', string='Partners', domain=[('email','!=',False),('opt_out','=',False)]),

        'email_template_send_type' : fields.selection([
                                                        ('individual', 'Send individual messages'),
                                                        ('general', 'Send one message for all'),
                                                        ], string='How to send?', default='general',
                                                        help='Sending individual messages allows the text to be customized for each partner'),
    }

    @api.onchange('email_template_partner_ids')
    def _onchange_email_template_partner_ids(self):
        aux=[]
        for p in self.email_template_partner_ids:
            aux.append(p.id)
        self.partner_to=','.join(map(str,aux))
            




# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
