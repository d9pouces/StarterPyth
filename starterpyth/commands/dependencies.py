from six import u

from starterpyth.log import YELLOW, GREEN
from starterpyth.log import display

__author__ = 'd9pouces'

import abc
from distutils.core import Command
import imp
import json
import os.path
import re
import subprocess


def find_dependencies(module_name):
    p = subprocess.Popen(['sfood', '--follow', module_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    found_dependencies = set()
    missing_dependencies = set()
    warning_re = re.compile(r'^WARNING\s*:\s*Line [0-9]+:.*')
    missing_re = re.compile(r'^WARNING\s*:  \s*(.*)$')
    for line in u(stderr).splitlines():
        if warning_re.match(line):
            continue
        missing_match = missing_re.match(line)
        if missing_match:
            missing_dependencies.add(missing_match.group(1))
    python_root = os.path.dirname(abc.__file__)

    def get_module_root(base_modulename):
        (file_, pathname, description) = imp.find_module(base_modulename)
        base_module = imp.load_module(base_modulename, file_, pathname, description)
        return os.path.abspath(os.path.dirname(os.path.dirname(base_module.__file__)))
    module_root = get_module_root(module_name)

    def add_dependence(python_root_, module_root_, found_dependencies_, dirname, filename):
        if dirname is None or filename is None:
            return
        if dirname.find(python_root_) == 0 or dirname.find(module_root_) == 0:
            return
        name = filename.partition(os.path.sep)[0]
        basename, ext = os.path.splitext(name)
        if ext.find('.py') == 0:
            found_dependencies_.add(basename)
        else:
            found_dependencies_.add(name)

    for line in u(stdout).splitlines():
        (src, dst) = json.loads(line.replace("(", "[").replace(")", "]").replace("'", '"').replace('None', 'null'))
        add_dependence(python_root, module_root, found_dependencies, *src)
        add_dependence(python_root, module_root, found_dependencies, *dst)
    return found_dependencies, missing_dependencies


class Dependencies(Command):
    description = 'Display a list of found dependencies'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        install_requires = set(self.distribution.install_requires)
        module_name = self.distribution.get_name()
        msg = 'Looking for dependencies of %(module_name)s...' % {'module_name': module_name}
        display(msg, color=GREEN)
        found_dependencies, missing_dependencies = find_dependencies(module_name)
        if found_dependencies:
            display('Found dependencies: ' + ', '.join(found_dependencies), color=GREEN)
            marked_dependencies = filter(lambda x: x not in install_requires, found_dependencies)
            if marked_dependencies:
                display('You should add the following dependencies to your stdeb.cfg and setup.py.:', color=YELLOW)
                display(', '.join(marked_dependencies), color=YELLOW)
            else:
                display('All of them are correctly set in your setup.py.', color=GREEN)
        else:
            display('No dependencies', color=GREEN)
        if len(missing_dependencies) > 0:
            display('Missing dependencies: ' + ', '.join(missing_dependencies), color=YELLOW)
            display('They may be false positive dependencies.', color=GREEN)
