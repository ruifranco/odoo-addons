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


class caving_area(orm.Model):
    _name ='caving.area'

    def _get_default_country(self, cr, uid, context=None):
        company_id = self.pool.get('res.users')._get_company(cr, uid, context=context)
        if company_id:
            if not isinstance(company_id,(tuple,list)):
                company_id=[company_id]
            company_res=self.pool.get('res.company').browse(cr, uid, company_id)
            if isinstance(company_res,(tuple,list)):
                company_res=company_res[0]
            if company_res.country_id:
                return company_res.country_id.id
            else:
                return False
        return False
        

    _columns = {
        'name'      : fields.char('Name', size=64, required=True),
        'partner_id': fields.many2one('res.partner','Partner'),
        'country_id': fields.many2one('res.country','Country'),
        'state_id'  : fields.many2one('res.country.state','State'),
        'cave_ids'  : fields.one2many('caving.cave.address', 'area_id', 'Caves', readonly=True),
    }

    _defaults={
        'country_id': _get_default_country,
    }
    