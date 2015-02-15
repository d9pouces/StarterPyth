# -*- coding: utf-8 -*-
import random
from starterpyth.cliforms import BaseForm, BooleanInput
from starterpyth.model import Model
from starterpyth.translation import ugettext as _

__author__ = 'flanker'


class PackageModel(Model):
    name = _('Python package')
    template_roots = [('starterpyth', 'templates/common'), ('starterpyth', 'templates/package')]


class CliModel(Model):
    name = _('Python binary')
    template_roots = [('starterpyth', 'templates/common'), ('starterpyth', 'templates/package'),
                      ('starterpyth', 'templates/cli')]

    def get_extracontext(self):
        self.global_context['entry_points'].setdefault('console_scripts', [])
        module_name = self.global_context['module_name']
        scripts = ['%s = %s.cli:main' % (module_name, module_name), ]
        self.global_context['entry_points']['console_scripts'] += scripts
        return {}


class DjangoModel(Model):
    name = _('Django-based website')
    template_roots = [('starterpyth', 'templates/common'), ('starterpyth', 'templates/django')]

    class ExtraForm(BaseForm):
        use_tastypie = BooleanInput(label=_('Use tastypie'), initial=True)

    def get_extracontext(self):
        requires = ['django', 'south', 'gunicorn', 'django-bootstrap3', 'django-pipeline', 'django-grappelli',
                    'django-debug-toolbar', ]
        if self.global_context['use_tastypie']:
            requires += ['django-tastypie', 'django-tastypie-swagger']
        self.global_context['entry_points'].setdefault('console_scripts', [])
        module_name = self.global_context['module_name']
        scripts = ['%s-manage = %s.core.scripts:main' % (module_name, module_name),
                   '%s-gunicorn = %s.core.scripts:gunicorn' % (module_name, module_name)]
        self.global_context['entry_points']['console_scripts'] += scripts
        self.global_context['install_requires'] += requires
        self.global_context['setup_requires'] += requires
        self.global_context['secret_key'] = self.__get_random_string()
        return {}

    def process_directory_or_file(self, src_path, dst_path, name, is_directory):
        if name == 'api.py' and not self.file_context['use_tastypie']:
            return False
        return super(DjangoModel, self).process_directory_or_file(src_path, dst_path, name, is_directory)

    @staticmethod
    def __get_random_string(length=50, allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                                     'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
        return ''.join([random.choice(allowed_chars) for i in range(length)])


class DjangofloorModel(Model):
    name = _('Djangofloor-based website')
    template_roots = [('starterpyth', 'templates/common'), ('starterpyth', 'templates/djangofloor')]

    class ExtraForm(BaseForm):
        use_djangorestframework = BooleanInput(label=_('Use Django REST framework'), initial=True)

    def get_extracontext(self):
        requires = ['djangofloor', ]
        self.global_context['entry_points'].setdefault('console_scripts', [])
        module_name = self.global_context['module_name']
        scripts = ['%s-manage = djangofloor.scripts:manage' % (module_name, ),
                   '%s-gunicorn = djangofloor.scripts:gunicorn' % (module_name, )]
        self.global_context['entry_points']['console_scripts'] += scripts
        if self.global_context['use_djangorestframework']:
            requires += ['djangorestframework', 'markdown', 'django-filter', 'pygments']
        self.global_context['install_requires'] += requires

        self.global_context['secret_key'] = self.__get_random_string()
        return {}

    def process_directory_or_file(self, src_path, dst_path, name, is_directory):
        if name == 'api.py' and not self.file_context['use_tastypie']:
            return False
        return super(DjangofloorModel, self).process_directory_or_file(src_path, dst_path, name, is_directory)

    @staticmethod
    def __get_random_string(length=50, allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                                     'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
        # noinspection PyUnusedLocal
        return ''.join([random.choice(allowed_chars) for i in range(length)])


if __name__ == '__main__':
    import doctest

    doctest.testmod()