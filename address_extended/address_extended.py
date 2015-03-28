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


class address_extended_places(orm.Model):
    _name ='address_extended.places'
    _order='name'

    country_id  = fields.Many2one('res.country','Country', required=True)
    state_id    = fields.Many2one('res.country.state', 'Fed. State', change_default=True, domain="[('country_id','=',country_id)]")
    parent_id   = fields.Many2one('address_extended.places', 'Parent')
    name        = fields.Char('Name', size=100, required=True)
    active      = fields.Boolean('Active', default=True)



class res_partner(orm.Model):
    _inherit ='res.partner'

    place_id_1  = fields.Many2one('address_extended.places','Place (level 1)')
    place_id_2  = fields.Many2one('address_extended.places','Place (level 2)')
    place_id_3  = fields.Many2one('address_extended.places','Place (level 3)')
    




