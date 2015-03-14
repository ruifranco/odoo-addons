#! -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Multibase.pt (<http://www.multibase.pt>)
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


#from openerp import sys
from openerp import addons
from openerp.tools import config
from openerp.osv import osv, orm
from openerp import models, fields, api, _


import os
import shutil
import errno
import zipfile
import base64

class ir_module_module(orm.Model):
    _inherit='ir.module.module'

    @api.one
    def button_create_readme_file(self):

        if isinstance(self,(list,tuple)):
            self=self[0]

        readme_txt="""[ NAME ]\n%s\n\n
[ SUMMARY ]\n%s\n\n
[ AUTHOR ]\n%s\n\n
[ VERSION ]\n%s\n\n
[ WEBSITE ]\n%s\n\n
[ CATEGORY ]\n%s\n\n
[ LICENSE ]\n%s\n\n
[ DESCRIPTION ]\n%s\n\n
[ MENUS ]\n%s\n\n
[ VIEWS ]\n%s\n\n
[ REPORTS ]\n%s""" % (self.name, self.shortdesc, self.author, self.latest_version or '', self.website, (self.category_id and self.category_id.name),
                      self.license, self.description, self.menus_by_module, self.views_by_module, self.reports_by_module)


        readme_txt=readme_txt.strip(' \t')

        module_path=self.get_module_path(self.name)
        if module_path:
            try:
                f=open(module_path +'/README.md',"w")
                f.write(readme_txt.encode('utf-8'))
                f.close()
            except:
                raise osv.except_osv(_('Error!'),_('Unable to write file at ' + readme_path))
        else:
            raise osv.except_osv(_('Error!'),_("Unable to find '%s' folder " % self.name))

        return True

    #https://docs.python.org/2/library/zipfile.html#zipfile-objects
    def zipdir(self, path, zip):
        for root, dirs, files in os.walk(path):
            for file in files:
                aux=os.path.join(root, file)
                if aux!=zip.filename:
                    zip.write(aux, os.path.relpath(aux, path))
                    #zip.write(aux)
        return True


    def get_separator(self, path):
        separator=''
        if path:
            if path.find('/')>=0:
                separator='/'
            else:
                separator='\\'
        return separator


    def get_module_path(self, module):
        module_path=False
        addons_path=config['addons_path'].split(',')

        for addons_folder in addons_path:
            separator=self.get_separator(addons_folder)
            break

        for addons_folder in addons_path:
            readme_path=separator.join([addons_folder, module])
            if os.path.isdir(readme_path):
                module_path=readme_path
                break
        return module_path
        

    def button_pack_module(self, cr, uid, ids, context):
        depends=self.get_associated_modules(cr, uid, ids, [])

        this=self.browse(cr, uid, ids)
        if isinstance(this,(tuple,list)):
            this=this[0]

        # ******************************************
        # create temp folder
        # ******************************************

        module_folder=self.get_module_path(this.name)
        
        separator=self.get_separator(module_folder)
        temp_folder=separator.join([module_folder, 'repository_manager_dependencies'])

        new_folder=False

        #delete previous existing folder        
        if os.path.isdir(temp_folder):
            shutil.rmtree(temp_folder)
        
        try:
            os.makedirs(temp_folder)
            new_folder=True
        except:
            raise osv.except_osv(_('Error!'),_('The destination folder could not be created'))

        if new_folder:
            # ******************************************
            # copy files
            # ******************************************
            for d in depends:
                module_path=self.get_module_path(d)
                if module_path:
                    module_name=module_path.split(separator)
                    if module_name:
                        module_name=module_name[-1]
                        self.copyfolder(module_path, separator.join([temp_folder, module_name]))
                        
            
            # ******************************************
            # create a zip file
            # ******************************************
            
            zip_file_name=this.name + '.zip'
            zip_file_path=separator.join([module_folder, zip_file_name])
            if os.path.isfile(zip_file_path):
                os.remove(zip_file_path)
            zipf = zipfile.ZipFile(zip_file_path, 'w')
            self.zipdir(module_folder, zipf)
            zipf.close()


            #delete the temp folder
            shutil.rmtree(temp_folder)


            # ******************************************
            # present file to the user
            # ******************************************
            #self.create_attachment(cr, uid, zip_file_name, zip_file_path)
            
            raise osv.except_osv(_('Error!'),_('A ZIP file has been created:\n%s') % zip_file_path)

        else:
            raise osv.except_osv(_('Error!'),_('Could not create folder %s') % new_folder)
        
        return True


    def create_attachment(self, cr, uid, zip_file_name, zip_file_path):
        if zip_file_name and zip_file_path:

            #create an attachment
            """
            zip_b64=zip_file_path+'.b64'
            with open(zip_file_path, 'rb') as fin, open(zip_b64, 'w') as fout:
                base64.encode(fin, fout)
            zip_aux=open(zip_b64, 'rb')
            zip_encoded=zip_aux.read()
            zip_aux.close()
            """

            #delete the zip file                                                      
            #os.remove(zip_file_path)
            #os.rename(zip_b64, zip_file_path)
            
            """            
            attachment_obj=self.pool.get('ir.attachment')

            attachment_ids=attachment_obj.search(cr, uid, [('name','=',zip_file_name)])
            if attachment_ids:
                attachment_obj.unlink(cr, uid, attachment_ids)

            zip_attachment=attachment_obj.create(cr,uid,{
                                              'name'        : zip_file_name,
                                              'db_datas'    : base64.encode(zip_encoded),
                                              'description' : this.name + '\n' + _('module dump by Repository Manager'),
                                              'datas_fname' : zip_file_name,
                                              })
                                             
                                                                 
            obj_model = self.pool.get('ir.model.data')
            model_data_ids = obj_model.search(cr,uid,[('model','=','ir.ui.view'),('name','=','view_attachment_form')])
            resource_id = obj_model.read(cr, uid, model_data_ids, fields=['res_id'])[0]['res_id']
            return {
                        'name'      :_("Repository Manager"),
                        'view_mode' : 'form',
                        'view_id'   : False,
                        'views'     : [(resource_id,'form')],
                        'view_type' : 'form',
                        'res_id'    : zip_attachment,
                        'res_model' : 'ir.attachment',
                        'type'      : 'ir.actions.act_window',
                        'target'    : 'new',
                    }
            """
        return True



    def copyfolder(self, src, dest):
        try:
            shutil.copytree(src, dest)
        except OSError as e:
            # If the error was caused because the source wasn't a directory
            if e.errno == errno.ENOTDIR:
                shutil.copy(src, dest)
            else:
                raise osv.except_osv(_('Error!'),_(e))
        return True


    def get_associated_modules(self, cr, uid, module_id, depends=[]):
        if module_id:
            aux=self.browse(cr, uid, module_id)
            for a in aux.dependencies_id:
                if a.name not in depends:
                    depends.append(a.name)
                    aux2=self.search(cr, uid, [('name','=',a.name)])
                    if aux2:
                        if isinstance(aux2,(tuple,list)):
                            aux2=aux2[0]

                        self.get_associated_modules(cr, uid, aux2, depends)
        return depends