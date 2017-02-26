# -*- coding=utf-8 -*-
"""Compile translated files
------------------------

Create .mo files from .po files, with the following tools: `xgettext`, `msgmerge`, `msginit` and `msgfmt`..

Usage:

.. code-block:: bash

  python setup.py compilemessages -l fr_FR

Do not forget to add these files to your version control system!
"""
from setuptools import find_packages
from starterpyth.log import display, GREEN
from starterpyth.core import load_module

__author__ = 'Matthieu Gallet'

from distutils.core import Command
import os
import subprocess

from starterpyth.translation import gettext as _


class CompileMessages(Command):
    """Compile message files for i18n"""
    description = '''Compile message files for i18n'''
    user_options = [
        ('language=', 'l', "target language (default: fr_FR)"),
        ('dest=', 'd', "output dir"),
        ('domain=', 'D', "i18n domain (default to the corresponding module name)"),
    ]

    def __init__(self, dist=None):
        Command.__init__(self, dist=dist)
        self.language = 'fr_FR'
        self.dest = None
        self.domain = None

    def initialize_options(self):
        self.language = 'fr_FR'
        self.dest = None
        self.domain = None

    def finalize_options(self):
        pass

    def run(self):
        module_names = find_packages()
        dst_rel_path = 'locale' if self.dest is None else self.dest
        # group by top-level packages and compute their directories:
        top_levels_modules = {}
        for module_name in module_names:
            tl, sep, bl = module_name.partition('.')
            if tl not in top_levels_modules:
                locale_dir = os.path.join(os.path.dirname(load_module(tl).__file__), dst_rel_path)
                top_levels_modules[tl] = locale_dir

        for module_name, locale_dir in top_levels_modules.items():
            domain = self.domain or module_name
            mo_file = os.path.join(locale_dir, self.language, 'LC_MESSAGES', '%s.mo' % domain)
            po_file = os.path.join(locale_dir, self.language, 'LC_MESSAGES', '%s.po' % domain)
            if not os.path.isdir(os.path.dirname(mo_file)):
                os.makedirs(os.path.dirname(mo_file))
            if os.path.isfile(po_file):
                cmd = 'msgfmt --output-file %s %s' % (mo_file, po_file)
                display(_('Processing file %(filename)s.') % {'filename': po_file}, color=GREEN)
                subprocess.check_call(cmd, shell=True, stderr=subprocess.PIPE)
