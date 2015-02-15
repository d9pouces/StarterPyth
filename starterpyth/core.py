# coding=utf-8
import getpass
from optparse import OptionParser
import os.path
import imp
import sys
import re

from six import u
from starterpyth.models import PackageModel, DjangoModel, CliModel, DjangofloorModel

from starterpyth.translation import ugettext as _
from starterpyth.cliforms import BaseForm, RegexpInput, BooleanInput, CharInput, ChoiceInput, PathInput


__author__ = 'd9pouces'

licenses = [('CeCILL-A', _('CeCILL-A')), ('CeCILL-B', _('CeCILL-B')), ('BSD-2-clauses', _('BSD 2 clauses')),
            ('Apache-2', _('Apache 2')), ('CeCILL-C', _('CeCILL-C')), ('GPL-2', _('GPL v.2')), ('GPL-3', _('GPL v.3')),
            ('LGPL-2', _('LGPL v.2')), ('LGPL-', _('LGPL v.3')), ('MIT', _('MIT'))]


available_models = [(PackageModel, PackageModel.name), (DjangoModel, DjangoModel.name), (CliModel, CliModel.name),
                    (DjangofloorModel, DjangofloorModel.name), ]


class BaseInfoForm(BaseForm):
    @staticmethod
    def __use_py2(**kwargs):
        return kwargs['use_py26'] or kwargs['use_py27']

    @staticmethod
    def __use_py3(**kwargs):
        for k, v in kwargs.items():
            if k.startswith('use_py3') and v:
                return True
        return False

    @staticmethod
    def __overwrite(**kwargs):
        return os.path.exists(kwargs['project_root'])

    project_name = RegexpInput(re.compile(r'[a-zA-Z_\-]\w*'), label=_('Project name'), initial='Project')
    module_name = RegexpInput(re.compile(r'[a-z][\-_a-z0-9]*'), label=_('Python module name'),
                              initial=lambda project_name: project_name.lower())
    root = PathInput(label=_('Destination directory'), initial='.')
    project_root = CharInput(initial=lambda **kwargs: os.path.join(kwargs['root'], kwargs['project_name']), show=False)
    overwrite = BooleanInput(initial=not __overwrite.__func__, show=__overwrite.__func__,
                             label=_('Overwrite destination'))
    author = CharInput(label=_('Author name'), initial=getpass.getuser())
    company = CharInput(label=_('Company'), initial=_('19pouces.net'))
    email = CharInput(label=_('E-mail'), initial=lambda **kwargs: _('%(author)s@%(company)s') % kwargs)
    use_py26 = BooleanInput(initial=False, label=_('Use Python 2.6'))
    use_py27 = BooleanInput(initial=lambda **kwargs: kwargs['use_py26'], label=_('Use Python 2.7'))
    use_py30 = BooleanInput(initial=False, label=_('Use Python 3.0'))
    use_py31 = BooleanInput(initial=lambda **kwargs: kwargs['use_py30'], label=_('Use Python 3.1'))
    use_py32 = BooleanInput(initial=lambda **kwargs: kwargs['use_py31'], label=_('Use Python 3.2'))
    use_py33 = BooleanInput(initial=True, label=_('Use Python 3.3'))
    use_py34 = BooleanInput(initial=True, label=_('Use Python 3.4'))
    use_py35 = BooleanInput(initial=True, label=_('Use Python 3.5'))
    use_py2 = BooleanInput(initial=__use_py2.__func__, show=False)
    use_py3 = BooleanInput(initial=__use_py3.__func__, show=False)
    use_six = BooleanInput(initial=False, label=_('Use six for Python 3 compatibility'),
                           show=lambda **kwargs: kwargs['use_py2'] and kwargs['use_py3'])
    use_2to3 = BooleanInput(initial=False, label=_('Use 2to3 for Python 3 compatibility'),
                            show=lambda **kwargs: kwargs['use_py2'] and kwargs['use_py3'] and not kwargs['use_six'])
    license = ChoiceInput(licenses, label=_('License'), initial='CeCILL-B')
    version = CharInput(label=_('Version'), initial='0.1')
    model = ChoiceInput(available_models, label=_('Code template'))
    use_i18n = BooleanInput(initial=True, label=_('Use translated strings'))


def load_module(modulename):
    parents = modulename.split(u('.'))
    path = sys.path
    module = None
    for module_name in parents:
        (file_, pathname, description) = imp.find_module(module_name, path)
        module = imp.load_module(module_name, file_, pathname, description)
        path = [os.path.dirname(module.__file__)]
    return module


def main():
    parser = OptionParser(usage=_('%(bin)s [-extension my.extension.module:class]') % {'bin': sys.argv[0]})
    parser.add_option('--extension', '-e', action='append', dest='extensions', default=[],
                      help=_('extra extension module'))
    parser.add_option('-v', '--verbose', action='store_true', help='print more messages', default=False)
    parser.add_option('--nointeractive', '-n', action='store_false', dest='nointeractive', default=True,
                      help=_('no interactive mode'))
    options, args = parser.parse_args(sys.argv[1:])
    base_form = BaseInfoForm(initial={'model': CliModel, 'overwrite': True, 'use_py26': True, 'use_six': False})
    base_context = base_form.read(interactive=options.nointeractive)
    model = base_context['model'](base_context=base_context)
    model.run(interactive=options.nointeractive)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
