"""

Generates a documentation index for your API by scanning all submodules of your
project and creates a basic `module.rst` file for each of them. Also generates
an global index referencing all these submodules.

Example:

.. code-block: python

    python setup.py gen_doc_api --overwrite
    writing doc/source/api/index.rst
    writing doc/source/api/starterpyth.rst
    writing doc/source/api/starterpyth/command.rst
    writing doc/source/api/starterpyth/command/compilemessages.rst
    writing doc/source/api/starterpyth/command/dependencies.rst
    writing doc/source/api/starterpyth/command/dmg.rst
    writing doc/source/api/starterpyth/command/gen_doc.rst
    writing doc/source/api/starterpyth/command/gen_doc_api.rst
    writing doc/source/api/starterpyth/command/lint.rst
    writing doc/source/api/starterpyth/command/makemessages.rst
    writing doc/source/api/starterpyth/command/profiling.rst
    writing doc/source/api/starterpyth/command/shell.rst
    writing doc/source/api/starterpyth/command/test_doc.rst
    writing doc/source/api/starterpyth/constants.rst
    writing doc/source/api/starterpyth/generator.rst
    writing doc/source/api/starterpyth/plugins.rst
    writing doc/source/api/starterpyth/plugins/base.rst
    writing doc/source/api/starterpyth/plugins/cython_app.rst
    writing doc/source/api/starterpyth/plugins/django_start.rst
    writing doc/source/api/starterpyth/plugins/qt_skeleton.rst
    writing doc/source/api/starterpyth/plugins/shell.rst
    writing doc/source/api/starterpyth/utils.rst

"""
import codecs
import fnmatch
import logging
import os
import shutil
from setuptools import find_packages
from starterpyth.core import load_module

from distutils.core import Command

try:
    from jinja2 import Environment, PackageLoader
except ImportError:
    Environment, PackageLoader = None, None
from starterpyth.translation import gettext as _
__author__ = 'Matthieu Gallet'


class GenDocApi(Command):
    """Generate simple API index for Sphinx documentation """
    description = 'Generate simple API index for Sphinx documentation'

    user_options = [('api-dir=', 'a', 'documentation root'),
                    ('overwrite', 'o', 'overwrite existing files'),
                    ('modules-to-exclude=', 'm',
                     'exclude these modules (dotted paths separated by commas. * and ? are supported)'),
                    ('pre-rm', 'p', 'remove existing files'), ]

    def __init__(self, *args, **kwargs):
        Command.__init__(self, *args, **kwargs)

        self.api_dir = os.path.join('doc', 'source', 'api')
        self.overwrite = 0
        self.pre_rm = 0
        self.modules_to_exclude = ''

    def initialize_options(self):
        self.api_dir = os.path.join('doc', 'source', 'api')
        self.overwrite = 0
        self.pre_rm = 0
        self.modules_to_exclude = ''

    def finalize_options(self):
        pass

    def run(self):
        if Environment is None:
            logging.critical(_('package jinja2 is required.'))
            return 1
        env = Environment(loader=PackageLoader('starterpyth.commands', 'templates'))

        def write_template(template_, path, context):
            """
            Write a template file.

            :param template_: Jinja2 template
            :type template_: :class:`Template`
            :param path: destination path
            :type path: basestring
            :param context: context
            :type context: :class:`dict`
            """
            dirname = os.path.dirname(path)
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
            if not os.path.isfile(path) or self.overwrite:
                tpl_fd = codecs.open(path, 'w', encoding='utf-8')
                tpl_fd.write(template_.render(context))
                tpl_fd.close()
                logging.info('writing %s' % path)
        src_module_names = find_packages()
        if self.pre_rm and os.path.isdir(self.api_dir):
            logging.info('removing %s' % self.api_dir)
            shutil.rmtree(self.api_dir)
        module_names = []
        excluded_module_names = set([x.strip() for x in self.modules_to_exclude.split(',') if x.strip()])

        for module_name in src_module_names:
            module = load_module(module_name)
            logging.warning('Processing %s.' % module_name)
            if not any(fnmatch.fnmatch(module_name, x) for x in excluded_module_names):
                module_names.append(module_name)
            module_root = os.path.dirname(module.__file__)
            for filename in os.listdir(module_root):
                basename, sep, ext = filename.rpartition('.')
                if ext not in ('pyx', 'py', 'so') or filename == '__init__.py':
                    continue
                submodule_name = '%s.%s' % (module_name, basename)
                try:
                    load_module(submodule_name)
                    if not any(fnmatch.fnmatch(submodule_name, x) for x in excluded_module_names):
                        module_names.append(submodule_name)
                except ImportError as e:
                    msg = 'Unable to import %s [%s].' % (submodule_name, e)
                    logging.warning(msg)
        template = env.get_template('index.rst_tpl')
        all_module_names = [mod_name.replace('.', '/') for mod_name in module_names]
        all_module_names.sort()
        write_template(template, os.path.join(self.api_dir, 'index.rst'),
                       {'module_paths': all_module_names})
        template = env.get_template('module.rst_tpl')
        for mod_name in module_names:
            path_components = mod_name.split('.')
            path_components[-1] += '.rst'
            write_template(template, os.path.join(self.api_dir, *path_components), {'module_name': mod_name})


if __name__ == '__main__':
    import doctest

    doctest.testmod()
