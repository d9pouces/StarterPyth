"""

Generates a documentation index for your API by scanning all submodules of your
project and creates a basic `module.rst` file for each of them. Also generates
an global index referencing all these submodules.

Example::

    $ python setup.py gen_doc_api --overwrite
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
import logging
from setuptools import find_packages
from starterpyth.core import load_module

__author__ = 'd9pouces'
import codecs
from distutils.core import Command
import os
import shutil

try:
    from jinja2 import Environment, PackageLoader
except ImportError:
    Environment, PackageLoader = None, None
from starterpyth.translation import gettext as _


class GenDocApi(Command):
    """Generate simple API index for Sphinx documentation """
    description = 'Generate simple API index for Sphinx documentation'

    user_options = [('api-dir=', 'a', "documentation root"),
                    ('overwrite', 'o', "overwrite existing files"),
                    ('pre-rm', 'p', "remove existing files"), ]

    def __init__(self, *args, **kwargs):
        Command.__init__(self, *args, **kwargs)
        self.api_dir = os.path.join('doc', 'source', 'api')
        self.overwrite = 0
        self.pre_rm = 0

    def initialize_options(self):
        self.api_dir = os.path.join('doc', 'source', 'api')
        self.overwrite = 0
        self.pre_rm = 0

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
        for module_name in src_module_names:
            module = load_module(module_name)
            logging.warning('Processing %s.' % module_name)
            module_names.append(module_name)
            module_root = os.path.dirname(module.__file__)
            for filename in os.listdir(module_root):
                basename, sep, ext = filename.rpartition('.')
                if ext not in ('pyx', 'py', 'so') or filename == '__init__.py':
                    continue
                submodule_name = '%s.%s' % (module_name, basename)
                try:
                    load_module(submodule_name)
                    module_names.append(submodule_name)
                except ImportError:
                    msg = 'Unable to import %s.' % submodule_name
                    logging.warning(msg)
        template = env.get_template('index.rst_tpl')
        write_template(template, os.path.join(self.api_dir, 'index.rst'),
                       {'module_paths': [mod_name.replace('.', '/') for mod_name in module_names]})
        template = env.get_template('module.rst_tpl')
        for mod_name in module_names:
            path_components = mod_name.split('.')
            path_components[-1] += '.rst'
            write_template(template, os.path.join(self.api_dir, *path_components), {'module_name': mod_name})


if __name__ == '__main__':
    import doctest

    doctest.testmod()
