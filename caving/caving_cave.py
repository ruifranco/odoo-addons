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



class caving_cave(orm.Model):
    _name ='caving.cave'
    _inherit = ['mail.thread']

    def action_button_exploration(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        self.write(cr, uid, ids, {'state':'exploration'})
        return True

    def action_button_done(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        self.write(cr, uid, ids, {'state':'done'})
        return True


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
        'name'                      : fields.char('Name', size=64, required=True),
        'company_id'                : fields.many2one('res.company', 'Company'),
        'aka'                       : fields.char('Also know as...', size=128),
        'visibility'                : fields.selection((
                                                ('public','Public'),
                                                ('restrict','Restrict'),
                                                ('secret','Secret'),
                                                ),'Visibility', help='Use this field in conjunction with user groups and rules'),
        'state'                     : fields.selection((
                                                ('draft','To explore'),
                                                ('exploration','Being explored'),
                                                ('done','Explored'),
                                                ),'State', readonly=True, copy=False,),
        'condition'                 : fields.selection((
                                                ('active','Active'),
                                                ('semiactive','Semi-active'),
                                                ('inactive','Inactive'),
                                                ),'Condition'),
        'kind'                      : fields.selection((
                                                ('natural','Natural'),
                                                ('manmade','Man made'),
                                                ),'Kind',states={'draft': [('readonly', True)]}),

        'url'                       : fields.char('URL', size=100,states={'draft': [('readonly', True)]}),
        'reference_ids'             : fields.one2many('caving.cave.reference', 'cave_id', 'References', 
                                                      help='The same cave may have different references, depending on caving clubs, authorities, etc.\nUse this field to keep track of them all, starting by your own.'),

        'landlord'                  : fields.many2one('res.partner','Landlord'),
        'supervisor'                : fields.many2one('res.partner','Supervisor'),


        'address_ids'               : fields.one2many('caving.cave.address','cave_id','Address'),

        'is_equipped'               : fields.boolean('Is equipped?'),
        'access_vertical'           : fields.boolean('Has vertical access?'),
        'access_horizontal'         : fields.boolean('Has horizontal access?'),
        'has_public_access'         : fields.boolean('Access is public?'),
        'needs_authorization'       : fields.boolean('Needs authorization?'),
        'is_touristic'              : fields.boolean('Tourist site?'),
        'has_animal_remains'        : fields.boolean('Has animal remains?'),
        'is_archaeological_site'    : fields.boolean('Is an archaeological site?'),

        'fauna_ids'                 : fields.many2many('caving.fauna', 'caving_cave_fauna_rel', 'cave_id', 'fauna_id', 'Fauna'),
        'flora_ids'                 : fields.many2many('caving.flora', 'caving_cave_flora_rel', 'cave_id', 'flora_id', 'Flora'),

        'notes'                     : fields.text('Notes'),
        'link_ids'                  : fields.many2many('caving.link', 'caving_cave_link_rel', 'cave_id', 'link_id', 'Links'),
        'tectonics'                 : fields.text('Tectonics',states={'draft': [('readonly', True)]}),
        'filling_ids'               : fields.one2many('caving.cave.filling', 'cave_id', 'Fillings'),
        'lithostratigraphy_ids'     : fields.one2many('caving.cave.lithostratigraphy', 'cave_id', 'Lithostratigraphy'),


        'speleometry_entrance_size_max' : fields.float('Entrance size (max)',digits=(5,2)),
        'speleometry_entrance_size_min' : fields.float('Entrance size (min)',digits=(5,2)),
        'speleometry_deepest_point'     : fields.float('Deepest point',digits=(6,2)),
        'speleometry_how_long'          : fields.float('How long?',digits=(8,2)),
        'speleometry_notes'             : fields.text('Notes'),

        'gas_analysis_ids'              : fields.one2many('caving.cave.gas_analysis', 'cave_id', 'Gas analysis'),
    }

    _defaults={
        'state'     : 'draft',
        'kind'      : 'natural',
        'visibility': 'restrict',
        'country_id': _get_default_country,
        'company_id': lambda self, cr, uid, ctx=None: self.pool.get('res.company')._company_default_get(cr, uid, 'caving.cave', context=ctx),
        
    }
    



class caving_cave_address(orm.Model):
    _name ='caving.cave.address'

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
        'name'      : fields.char('Name', required=True),
        'sequence'  : fields.integer('Sequence', help="Gives the sequence order when displaying a list of addresses."),
        'cave_id'   : fields.many2one('caving.cave','Cave'),
        'country_id': fields.many2one('res.country','Country'),
        'area_id'   : fields.many2one('caving.area','Area'),
        'place'     : fields.char('Place', size=100),
        'coords_id' : fields.many2one('gps_base.coords','Coords'),
        'note'      : fields.text('Notes'),
    }

    _order = 'cave_id desc, sequence, id'

    _defaults={
        'country_id': _get_default_country,
        'sequence': 10,
    }







class caving_cave_reference(orm.Model):
    _name ='caving.cave.reference'

    _columns = {
        'cave_id'       : fields.many2one('caving.cave','Cave', required=True),
        'sequence'      : fields.integer('Sequence'),
        'partner_id'    : fields.many2one('res.partner','Partner'),
        'name'          : fields.char('Name', size=64, required=True),
        'identification': fields.char('Identification', size=50),
        'url'           : fields.char('URL', size=100),
        'notes'         : fields.text('Notes'),
    }







class caving_cave_lithostratigraphy(orm.Model):
    _name ='caving.cave.lithostratigraphy'

    _columns = {
        'cave_id'           : fields.many2one('caving.cave','Cave'),
        'elevation_from'    : fields.integer('Elevation (from)'),
        'elevation_to'      : fields.integer('Elevation (to)'),
        'petrography_id'    : fields.many2one('caving.petrography','Petrography'),
        'geologic_time_id'  : fields.many2one('caving.geologic_time','Geologic time'),
        'notes'             : fields.text('Notes'),
    }








class caving_cave_filling(orm.Model):
    _name ='caving.cave.filling'

    _columns = {
        'cave_id'       : fields.many2one('caving.cave','Cave'),
        'name'          : fields.char('Description', size=100),
        'elevation'     : fields.integer('Elevation'),
    }






class caving_cave_gas_analysis(orm.Model):
    _name ='caving.cave.gas_analysis'

    _columns = {
        'cave_id'       : fields.many2one('caving.cave','Cave', required=True),
        'partner_id'    : fields.many2one('res.partner','Partner'),
        'gas_id'        : fields.many2one('caving.gas','Gas', required=True),
        'date'          : fields.date('Date', required=True),
        'method'        : fields.char('Method',size=128),
        'percentage'    : fields.float('%', digits=(5,2)),
        'notes'         : fields.text('Notes'),
    }

