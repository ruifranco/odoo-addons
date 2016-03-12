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
import re


class name_gender(models.Model):

    _name = 'name.gender'

    name    = fields.Char(string='Name', required=True)
    gender  = fields.Selection([('m','Male'),('f','Female')], string='Gender', required=True)

    _sql_constraints = [('name_uniq', 'unique (name)', "Name already exists!"),]


    @api.model
    def _load_partner_data(self):
        try:
            self._cr.execute("""INSERT INTO name_gender (name,gender)
                                SELECT DISTINCT ON (name) INITCAP(LOWER(TRIM(SUBSTRING((name || ' ') FROM 1 FOR POSITION(' ' IN (name || ' ')))))), 
                                        LOWER(SUBSTRING(TRIM(gender) from 1 for 1))
                                FROM    res_partner
                                WHERE    gender IS NOT NULL
                                ORDER    BY name,gender""")
        except:
            pass



    def validate_name(self, name=False):
        res = ''
        
        if name:
            if re.sub(r"[^A-Za-z_]+", '', name):
                res = name.strip().split(' ')[0].lower().capitalize()
        
        return res


    """
    @name - text to search for
    returns: m/f - if name is found; False if name was not found/name is not text
    """
    @api.model
    def get_name_gender(self, name=False):

        gender=False
        
        name = self.validate_name(name)
        if name:
            name_gender = self.search([('name','=',name)], limit=1)
            if name_gender:
                gender = name_gender.gender

        return gender
    

    
        
    def create_name_gender(self, name=False, gender=False):

        res = False
        
        if name and gender:
            name = self.validate_name(name)
            
            if name:
                try:
                    res = self.create({
                                       'name'  : name,
                                       'gender': gender,
                                       })
                except:
                    res = True
                    pass

        return res