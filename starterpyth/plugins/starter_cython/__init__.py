from starterpyth.fields import BooleanInput

__author__ = 'flanker'

from starterpyth.core import Plugin
from starterpyth.translation import ugettext as _


class CythonPlugin(Plugin):

    def __init__(self):
        self.selected = True
        super(CythonPlugin, self).__init__()

    def is_selected(self):
        return self.selected

    def update_global_context(self, context, filters):
        self.selected = BooleanInput(_('Create a Cython application'), default=True).input()
        if not self.selected:
            return
        context['doc_urls']['cython'] = ('http://docs.cython.org/', 'externals/cython_0.19.inv')
#        context['ext_modules'].append('Extension("sample_cython", ["sample_cython.pyx"])')
#        context['extra_imports'].append(('distutils.extension', 'Extension', None))
#        context['extra_imports'].append(('Cython.Distutils', 'build_ext', 'cython_build_ext'))
        cython_setup = self.get_template(context, 'starterpyth.plugins.starter_cython', 'extra_templates/setup.py_tpl')
        context['extra_setup'].append(cython_setup)

    def get_resources(self):
        return 'starterpyth.plugins.starter_cython', 'templates'
