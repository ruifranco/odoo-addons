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
from openerp.osv import fields, osv, orm
from openerp import tools
from openerp.tools.translate import _


class l10n_pt_administrative_divisions_distritos(orm.Model):
    _name ='l10n_pt_administrative_divisions.distritos'

    _columns = {
        'country_id': fields.many2one('res.country','Country', required=True),
        'name'      : fields.char('Name', size=64, required=True),
        'active'    : fields.boolean('Active'),
    }
    
    _defaults = {
        'active' : True,
    }





class l10n_pt_administrative_divisions_concelhos(orm.Model):
    _name ='l10n_pt_administrative_divisions.concelhos'

    _columns = {
        'country_id'    : fields.related('distrito_id', 'country_id', type='many2one', relation='res.country', string='Country', store=True, readonly=True),
        'distrito_id'   : fields.many2one('l10n_pt_administrative_divisions.distritos','Distrito', required=True),
        'name'          : fields.char('Name', size=64, required=True),
        'active'        : fields.boolean('Active'),
    }
    
    _defaults = {
        'active' : True,
    }





class l10n_pt_administrative_divisions_freguesias(orm.Model):
    _name ='l10n_pt_administrative_divisions.freguesias'

    _columns = {
        'country_id'    : fields.related('distrito_id', 'country_id', type='many2one', relation='res.country', string='Country', store=True, readonly=True),
        'distrito_id'   : fields.related('concelho_id', 'distrito_id', type='many2one', relation='l10n_pt_administrative_divisions.distritos', string='Distrito', store=True, readonly=True),
        'concelho_id'   : fields.many2one('l10n_pt_administrative_divisions.concelhos','Concelho', required=True),
        'name'          : fields.char('Name', size=64, required=True),
        'active'        : fields.boolean('Active'),
    }
    
    _defaults = {
        'active' : True,
    }







class res_partner(orm.Model):
    _inherit ='res.partner'

    _columns = {
        'distrito_id'   : fields.many2one('l10n_pt_administrative_divisions.distritos','Distrito',),
        'concelho_id'   : fields.many2one('l10n_pt_administrative_divisions.concelhos','Concelho'),
        'freguesia_id'  : fields.many2one('l10n_pt_administrative_divisions.freguesias','Freguesia'),
    }




