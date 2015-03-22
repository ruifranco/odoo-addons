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
from openerp import tools
from openerp import models, fields, api, _



class caving_cave(models.Model):
    _inherit='caving.cave'

    #auxiliary fields so that the web_gmap widget may be used
    widget_map_latitude     = fields.Char('Latitude', compute='widget_map_fields')
    widget_map_longitude    = fields.Char('Longitude', compute='widget_map_fields')


    @api.one
    @api.onchange('coords_id')
    def widget_map_fields(self):
        if self.coords_id:
            self.widget_map_latitude=self.coords_id.latitude
            self.widget_map_longitude=self.coords_id.longitude
        else:
            self.widget_map_latitude=0
            self.widget_map_longitude=0

