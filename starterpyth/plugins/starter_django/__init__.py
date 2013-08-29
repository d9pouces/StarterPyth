import random
import logging
__author__ = 'd9pouces'

from starterpyth.core import Plugin
from starterpyth.fields import BooleanInput
from starterpyth.translation import ugettext as _


class DjangoPlugin(Plugin):

    def __init__(self):
        self.selected = True
        self.use_tastypie = False
        super(DjangoPlugin, self).__init__()

    def is_selected(self):
        return self.selected

    def update_global_context(self, context, filters):
        self.selected = BooleanInput(_('Create a Django website'), default=True).input()
        if not self.selected:
            return
        if 3.0 <= context['pyversion'] <= 3.2:
            logging.warning(_('WARNING: django-tastypie is not compatible with Python 3.0 -> 3.2'))
        self.use_tastypie = BooleanInput(_('Create sample REST API with Tastypie'), default=True).input()
        self.use_tastypie_swagger = False
        if self.use_tastypie:
            self.use_tastypie_swagger = BooleanInput(_('Create API doc with Tastypie Swagger'), default=True).input()
        script = '%(module_name)s-manage = %(module_name)s.djangoproject.manage:main' % \
                 {'module_name': context['module_name']}
        context['entry_points'].setdefault('console_scripts', []).append(script)
        context['install_requires'].append('django')
        if self.use_tastypie:
            context['install_requires'].append('django-tastypie')
            context['install_requires'].append('python-mimeparse')
            context['install_requires'].append('python-dateutil')
        if self.use_tastypie_swagger:
            context['install_requires'].append('django-tastypie-swagger')

    def get_local_context(self, context):
        return {
            'use_tastypie': self.use_tastypie,
            'use_tastypie_swagger': self.use_tastypie_swagger,
        }

    def get_resources(self):
        return 'starterpyth.plugins.starter_django', 'templates'

    def __get_random_string(self, length=50, allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                                           'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
        return ''.join([random.choice(allowed_chars) for i in range(length)])
