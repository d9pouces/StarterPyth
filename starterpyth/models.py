#coding=utf-8
import random
from starterpyth.cliforms import BaseForm
from starterpyth.model import Model
from starterpyth.translation import ugettext as _

__author__ = 'flanker'


class PackageModel(Model):
    name = _('Python package')
    template_roots = [('starterpyth', 'templates/common'), ('starterpyth', 'templates/package')]


class DjangoModel(Model):
    name = _('Django-based website')
    template_roots = [('starterpyth', 'templates/common'), ('starterpyth', 'templates/django')]

    class ExtraForm(BaseForm):
        pass

    def get_extracontext(self):
        requires = ['django', 'south', 'gunicorn', 'django-bootstrap3', 'django-pipeline', 'django-grappelli',
                    'django-debug-toolbar', ]
        self.global_context['entry_points'].setdefault('console_scripts', [])
        module_name = self.global_context['module_name']
        scripts = ['%s-manage = %s.core.scripts:main' % (module_name, module_name),
                   '%s-gunicorn = %s.core.scripts:gunicorn' % (module_name, module_name)]
        self.global_context['entry_points']['console_scripts'] += scripts
        self.global_context['install_requires'] += requires
        self.global_context['setup_requires'] += requires
        self.global_context['secret_key'] = self.__get_random_string()
        return {}

    @staticmethod
    def __get_random_string(length=50, allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                                     'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
        return ''.join([random.choice(allowed_chars) for i in range(length)])


if __name__ == '__main__':
    import doctest

    doctest.testmod()