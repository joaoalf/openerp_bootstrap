import datetime
import os
import shutil
from paste.script import templates
from paste.script.templates import var


class NewModule(templates.Template):

    egg_plugins = ['openerp_newmodule']
    summary = 'Template for creating a basic openerp package skeleton'
    required_templates = []
    _template_dir = 'templates/newmodule'
    use_cheetah = True

    vars = [
        var('module_name', 'Module name (like "Project Issue")',
            default='My Module'),
        var('description', 'One-line description of the module'),
        var('version', 'Version', default='1.0'),
        var('author', 'Author name'),
        var('author_email', 'Author email'),
        var('category', 'Category'),
        var('website', 'Website'),
        var('license', 'License', default="AGPLv3"),
        var('depends', 'Dependencies [space-separated module names]',
            default=''),
        var('is_web', 'Is web addon? [yes/no]', default='no'),
        var('has_demo', 'Has demo data? [yes/no]', default='no'),
        var('has_report', 'Has reports? [yes/no]', default='yes'),
        var('has_wizard', 'Has wizards? [yes/no]', default='yes'),
        var('has_workflow', 'Has workflows? [yes/no]', default='no'),
    ]

    def pre(self, command, output_dir, vars):
        """
        Called before template is applied.
        """
        # import pdb;pdb.set_trace()
        depends = vars['depends'].split(' ')
        vars['is_web'] = vars['is_web'] == 'yes' and True or False
        vars['has_demo'] = vars['has_report'] == 'yes' and True or False
        vars['has_report'] = vars['has_report'] == 'yes' and True or False
        vars['has_wizard'] = vars['has_wizard'] == 'yes' and True or False
        vars['has_workflow'] = vars['has_workflow'] == 'yes' and True or False
        if vars['is_web'] and not 'web' in depends:
            depends.append('web')
        vars['depends'] = [x for x in depends if x]

        if vars['license'] in ('AGPL-3', 'AGPLv3', 'GPL-3', 'GPLv3'):
            if vars['license'] in ('AGPL-3', 'AGPLv3'):
                license = 'GNU Affero General Public License'
            else:
                license = 'GNU General Public License'

            vars['copyright'] = """##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) {0} {1} (<{2}>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the {3} as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    {3} for more details.
#
#    You should have received a copy of the {3}
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################""".format(
    datetime.date.today().year,
    vars['author'],
    vars['website'],
    license)
        else:
            license = ''

    def post(self, command, output_dir, vars):
        for i in ('has_report', 'has_wizard', 'has_workflow'):
            if not vars[i]:
                shutil.rmtree(os.path.join(output_dir,
                                           i.replace('has_', '')))
