#! -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Rui Pedrosa Franco All Rights Reserved
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

from __future__ import division
from openerp import addons
from openerp.osv import fields, osv, orm
from openerp.tools.misc import attrgetter
from decimal import Decimal
from openerp.tools.translate import _
import math


class gps_base_base(orm.Model):
    _name='gps_base.base'

    #in wich format has the user decided to see/insert coordinates?
    def _get_user_coords_format(self, cr, uid):
        user_res=self.pool.get('res.users').read(cr, uid, uid, ['coords_format'])
        user_coords_format=user_res['coords_format'] and user_res['coords_format'] or 'dd'
        return user_coords_format


    #**********************************************************
    # conversion functions
    #**********************************************************

    def convert_dd_ddm(self, cr, uid, lat=False, long=False):
        res=[(0,0),(0,0)]
        if lat and long:
            res=[lat, long]
            for i in range(2):
                degrees=int(res[i])
                minutes=(res[i]-degrees)*60
                res[i]=(degrees,minutes)
        return res

    def convert_dd_dms(self, cr, uid, lat=False, long=False):
        res=[(0,0,0),(0,0,0)]
        if lat and long:
            res=[lat, long]
            for i in range(2):
                degrees=int(res[i])
                minutes=int(60*(res[i]-degrees))
                seconds=3600*(res[i]-degrees-minutes/60)
                res[i]=(degrees,minutes,seconds)
        return res

    # TO DO
    def convert_ddm_dd(self, cr, uid, lat=False, long=False):
        res=[0,0]
        
        #Degrees Minutes.m to Decimal Degrees
        #.d = M.m / 60
        #Decimal Degrees = Degrees + .d
        """
        if lat and long:
            res=[lat, long]
            for i in range(2):
        """
        
        #raise osv.except_osv(_('Error'),_(res))
        return res

    # TO DO
    def convert_dms_dd(self, cr, uid, lat=False, long=False):
        res=[0,0]
        return res


    #**********************************************************
    # format functions
    #**********************************************************


    def latChar(self, coord):
        char='N'
        if coord<0:
            char='S'
        return char + ' '

    def longChar(self, coord):
        char='W'
        if coord>0:
            char='E'
        return char + ' '
    
    def dd_format(self, cr, uid, lat=False, long=False):
        #decimal degrees: N 40.446°, W 79.982°
        res=''
        if lat and long:
            res=self.latChar(lat) + str(abs(lat)) + 'º, ' + self.longChar(long) + str(abs(long)) + 'º'
        return res
    
    def ddm_format(self, cr, uid, lat=False, long=False):
        #degrees decimal minutes: N 40° 26.767′, W 79° 58.933′
        res=''
        if lat and long:
            conv=self.convert_dd_ddm(cr, uid, lat, long)
            
            lat=self.latChar(conv[0][0]) + str(abs(conv[0][0])) + 'º ' + str(abs(conv[0][1]))
            long=self.longChar(conv[1][0]) + str(abs(conv[1][0])) + 'º ' + str(abs(conv[1][1]))
            res=lat +', '+long
        return res
    
    def dms_format(self, cr, uid, lat=False, long=False):
        #degrees minutes seconds: N 40° 26′ 46″, W 79° 58′ 56″
        res=''
        if lat and long:
            conv=self.convert_dd_dms(cr, uid, lat, long)
            lat=self.latChar(conv[0][0]) + str(abs(conv[0][0])) + 'º ' + str(abs(conv[0][1])) + "' " + str(abs(conv[0][2])) + '"'
            long=self.longChar(conv[1][0]) + str(abs(conv[1][0])) + 'º ' + str(abs(conv[1][1])) + "' " + str(abs(conv[1][2])) + '"'
            res=lat +', '+long
        return res
     

    #**********************************************************
    # validation functions
    #**********************************************************
     
    """
    Gets a coord (in "natural" input format) and returns an array with its parts converted to elements.
    Thus, N 30.356 becomes [30,356] and W 1º 33' 10.8 becomes [1,33,10,8].
    """
    def clean_coords(self, coord):
        res=[]
        if coord:
            aux=str(coord).strip()
            for c in ['º','"',"'"]:
                aux=aux.replace(c,'.')

            for c in [' ','N','n','W','w']:
                aux=aux.replace(c,'')
                
            res=aux.split('.')
            last_pos=len(res)-1
            if not res[last_pos]:
                del res[last_pos]
                
            res=[int(i) for i in res]
                
        return res


    #validation of input in the dd format - N 40.446°, W 79.982°
    def dd_validate(self, cr, uid, lat=False, long=False):
        res=True
        
        if lat and long:
            lat=self.clean_coords(lat)

            if len(lat)==1:
                lat.append(0)
            
            if len(lat)==2:
                #degrees
                if lat[0]<-90 or lat[0]>90:
                    res=False

                #decimals
                lat[1]=str(abs(lat[1]))
                if len(lat[1])>8:
                    res=False
            else:
                res=False

            long=self.clean_coords(long)
            if len(long)==1:
                long.append(0)

            if len(long)==2:
                #degrees
                if long[0]<-180 or long[0]>180:
                    res=False

                #decimals
                long[1]=str(abs(long[1]))
                if len(long[1])>8:
                    res=False
            else:
                res=False
        else:
            res=False

        if not res:
            error_msg='Coordinates are not in the right format (DD).'
            error_msg+='\n\nExamples:\n'
            error_msg+='N 40.446°, W 79.982°\nN40.446°, W 79.982\n40.446, W79.982º'
            raise osv.except_osv(_('Error'),_(error_msg))
        else:
            #if coords are alright, the method returns a clean version of them
            aux_lat=float(str(lat[0]) + '.' + str(lat[1])) 
            aux_long=float(str(long[0]) + '.' + str(long[1]))
            res=[aux_lat, aux_long]
            
        return res


    
    def ddm_validate(self, cr, uid, lat=False, long=False):
        return True
    
    def dms_validate(self, cr, uid, lat=False, long=False):
        return True




class gps_base_coords(orm.Model):

    _name = 'gps_base.coords'


    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]

        reads = self.read(cr, uid, ids, ['user_coords', 'country_id'], context=context)
        res = []
        for record in reads:
            name = record['user_coords']
            if record['country_id']:
                name = name + ' (' + record['country_id'][1] + ')'
            res.append((record['id'], name))
        return res


  

    #this shows coords in the format the user has defined in his preferences
    def _get_user_coords(self, cr, uid, ids, field_name, arg, context):
        res={}
        
        for i in ids:
            this=self.browse(cr, uid, i)
            res[i]=eval('this.' + self.pool.get('gps_base.base')._get_user_coords_format(cr, uid) + '_coords')
        return res  

        
    def _get_dd_coords(self, cr, uid, ids, field_name, arg, context):
        res={}
        for i in ids:
            this=self.browse(cr, uid, i)
            res[i]=self.pool.get('gps_base.base').dd_format(cr, uid, this.latitude, this.longitude)
        return res    
    
    def _get_ddm_coords(self, cr, uid, ids, field_name, arg, context):
        res={}
        for i in ids:
            this=self.browse(cr, uid, i)
            res[i]=self.pool.get('gps_base.base').ddm_format(cr, uid, this.latitude, this.longitude)
        return res    

    def _get_dms_coords(self, cr, uid, ids, field_name, arg, context):
        res={}
        for i in ids:
            this=self.browse(cr, uid, i)
            res[i]=self.pool.get('gps_base.base').dms_format(cr, uid, this.latitude, this.longitude)
        return res    







    def create(self, cr, uid, vals, context=None):
    
        user_coords_format  = self.pool.get('gps_base.base')._get_user_coords_format(cr, uid)
        user_coords_format  = vals.get('format_aux', user_coords_format)
        method_to_use       = "self.pool.get('gps_base.base')." + user_coords_format + '_validate'

        latitude_aux    = vals['latitude_aux']
        longitude_aux   = vals['longitude_aux']
        
        #validation of the user input
        val_res=eval(method_to_use)(cr, uid, latitude_aux, longitude_aux)


        #if coordinates are ok
        #we convert the coordinates to dd format so that they can be saved
        if val_res:
            #no need to convert if coords are already in dd format
            if user_coords_format == 'dd':
                vals['latitude'], vals['longitude'] = val_res
            else:
                method_to_use="self.pool.get('gps_base.base')." + 'convert_' + user_coords_format + '_dd'

                #raise osv.except_osv(_('Warning!'),_(method_to_use))

                vals['latitude'], vals['longitude'] = eval(method_to_use)(cr, uid, latitude_aux, longitude_aux)


            vals['latitude_aux']  = vals['latitude']
            vals['longitude_aux'] = vals['longitude']
            vals['format_aux']    = 'dd'
        

        #raise osv.except_osv(_('Warning!'),_(vals) + '\n' + _(val_res))
        
        try:
            aux=super(gps_base_coords, self).create(cr, uid, vals, context=context)
        except:
            raise osv.except_osv(_('Error!'), _('Check if you entered the coordinates in the right format (%s)') % (user_coords_format))
        
        return aux


    def write(self, cr, uid, ids, vals, context=None):
    
        if not isinstance(ids,(list,tuple)):
            ids=[ids]
    
        #how to do the validation of the user input
        user_coords_format=self.pool.get('gps_base.base')._get_user_coords_format(cr, uid)
        if 'format_aux' in vals:
            user_coords_format=vals.get('format_aux', user_coords_format)
        method_to_use="self.pool.get('gps_base.base')." + user_coords_format + '_validate'

        for this in self.browse(cr, uid, ids):

            latitude_aux=this.latitude_aux
            if 'latitude_aux' in vals:
                latitude_aux=vals['latitude_aux']
                
            longitude_aux=this.longitude_aux
            if 'longitude_aux' in vals:
                longitude_aux=vals['longitude_aux']
        
            #validation of the user input
            val_res=eval(method_to_use)(cr, uid, latitude_aux, longitude_aux)

            #if coordinates are ok
            #we convert the coordinates to dd format so that they can be saved
            if val_res:
                #no need to convert if coords are already in dd format
                if user_coords_format == 'dd':
                    vals['latitude'], vals['longitude'] = val_res
                else:
                    method_to_use="self.pool.get('gps_base.base')." + 'convert_' + user_coords_format + '_dd'
                    vals['latitude'], vals['longitude'] = eval(method_to_use)(cr, uid, latitude_aux, longitude_aux)


                vals['latitude_aux']  = vals['latitude']
                vals['longitude_aux'] = vals['longitude']
                vals['format_aux']    = 'dd'
        
            #raise osv.except_osv(_('Warning!'),_(vals) + '\n' + _(val_res))
        
        return super(gps_base_coords, self).write(cr, uid, ids, vals, context=context)


    _columns = {
        'country_id'  : fields.many2one('res.country', 'Country'),
        
        #***********************************************************
        # fields for entering data
        #***********************************************************
        'latitude_aux'  : fields.char('Latitude (N)',size=15, required=True),
        'longitude_aux' : fields.char('Longitude (W)',size=15, required=True),
        'format_aux'    : fields.selection(
                                            (
                                                ('dd','Decimal degrees: N 40.446°, W 79.982°'), 
                                                ('ddm',"Degrees decimal minutes: N 40° 26.767′, W 79° 58.933′"),
                                                ('dms',"Degrees minutes seconds: N 40° 26′ 46″, W 79° 58′ 56''"),
                                            ), 
                                            'Coordinate format', 
                                            help='This is the format against wich coordinates will be validated',
                                            ),
        
        
        #coordinates are always saved in the decimal degrees format (N 40.446°, W 79.982°)
        'latitude'  : fields.float('Latitude',digits=(9,6), readonly=True, help='Decimal degrees format'),
        'longitude' : fields.float('Longitude',digits=(9,6), readonly=True, help='Decimal degrees format'),

        #coordinates in the format the user has chosen
        'user_coords'  : fields.function(_get_user_coords, type='char', method=True, string='Coords'),

        #***********************************************************
        # functional fields to show coordinates in all three formats
        #***********************************************************
        'dd_coords' : fields.function(_get_dd_coords,  type='char', method=True, string='Decimal degrees format'),
        'ddm_coords': fields.function(_get_ddm_coords, type='char', method=True, string='Degrees decimal minutes format'),
        'dms_coords': fields.function(_get_dms_coords, type='char', method=True, string='Degrees minutes seconds format'),
    }

    _defaults = {
        'format_aux': lambda self, cr, uid, c: self.pool.get('gps_base.base')._get_user_coords_format(cr, uid) or 'dd',
    }




