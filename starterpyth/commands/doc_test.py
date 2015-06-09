import os
from setuptools import find_packages
from starterpyth.log import display
from starterpyth.log import GREEN, YELLOW
from starterpyth.core import load_module

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
            display('Processing %s.' % module_name, color=YELLOW)
            doctest.testmod(module)
            module_root = os.path.dirname(module.__file__)
            for filename in os.listdir(module_root):
                basename, sep, ext = filename.rpartition('.')
                if ext != 'py' or filename == '__init__.py':
                    continue
                submodule_name = '%s.%s' % (module_name, basename)
                try:
                    module = load_module(submodule_name)
                    display('Processing %s.' % submodule_name, color=GREEN)
                    doctest.testmod(module)
                except ImportError:
                    display('Unable to import %s.' % submodule_name, color=YELLOW)
