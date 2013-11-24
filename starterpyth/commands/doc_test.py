import os
from setuptools import find_packages
from starterpyth.core import load_module
from starterpyth.log import green, yellow

__author__ = 'd9pouces'
from distutils.core import Command
import doctest


class DocTest(Command):
    description = 'Run examples provided in docstrings'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        module_names = find_packages()
        for module_name in module_names:
            module = load_module(module_name)
            print(green('Processing %s.' % module_name))
            doctest.testmod(module)
            module_root = os.path.dirname(module.__file__)
            for filename in os.listdir(module_root):
                basename, sep, ext = filename.rpartition('.')
                if ext != 'py' or filename == '__init__.py':
                    continue
                submodule_name = '%s.%s' % (module_name, basename)
                try:
                    module = load_module(submodule_name)
                    print(green('Processing %s.' % submodule_name))
                    doctest.testmod(module)
                except ImportError:
                    print(yellow('Unable to import %s.' % submodule_name))
