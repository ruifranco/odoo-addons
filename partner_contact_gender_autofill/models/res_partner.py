#! -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Odooveloper (Rui Pedrosa Franco) All Rights Reserved
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

from openerp import models, fields, api, _


class res_partner(models.Model):
    
    _inherit = 'res.partner'
    

    #Everytime the partner's name is changed, we run the search
    @api.onchange('name')
    def onchange_name(self):

        if self.name:
            name_gender_obj = self.env['name.gender']
            
            gender = name_gender_obj.get_name_gender(self.name)
            
            if gender == 'm':
                self.gender = 'male'
            elif gender == 'f':
                self.gender = 'female'
            elif self.gender:
                name_gender_obj.create_name_gender(self.name, self.gender[:1])


    @api.onchange('gender')
    def onchange_gender(self):

        if self.name and self.gender:
            name_gender_obj = self.env['name.gender']
            
            name_exists = name_gender_obj.get_name_gender(self.name)
            if not name_exists:
                name_gender_obj.create_name_gender(self.name, self.gender[:1])

