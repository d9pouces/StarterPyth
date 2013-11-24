from six import u
from starterpyth.fields import BooleanInput

__author__ = 'd9pouces'

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
        context['doc_urls']['cython'] = (u('http://docs.cython.org/'), u('externals/cython_0.19.inv'))
#        context['ext_modules'].append('Extension("sample_cython", ["sample_cython.pyx"])')
#        context['extra_imports'].append(('distutils.extension', 'Extension', None))
#        context['extra_imports'].append(('Cython.Distutils', 'build_ext', 'cython_build_ext'))
        cython_setup = self.get_template(context, u('starterpyth.plugins.starter_cython'),
                                         u('extra_templates/setup.py_tpl'))
        context['extra_setup'].append(cython_setup)

    def get_resources(self):
        return 'starterpyth.plugins.starter_cython', 'templates'
