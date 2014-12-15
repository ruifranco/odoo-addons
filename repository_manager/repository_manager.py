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

import os
from openerp import sys
from openerp import addons
from openerp.tools import config
from openerp.osv import osv, orm
from openerp import models, fields, api, _


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

        folder_found=False
        addons_path=config['addons_path'].split(',')
        for addons_folder in addons_path:
            readme_path=addons_folder + '\\' + self.name
            
            if os.path.isdir(readme_path):
                folder_found=True
                try:
                    f=open(readme_path +'/README.md',"w")
                    f.write(readme_txt.encode('utf-8'))
                    f.close()
                except:
                    raise osv.except_osv(_('Error!'),_('Unable to write file at ' + readme_path))
                break

        if not folder_found:
            raise osv.except_osv(_('Error!'),_("Unable to find '%s' folder " % self.name))
        

        return True