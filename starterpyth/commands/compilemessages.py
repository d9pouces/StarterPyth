from setuptools import find_packages
from starterpyth.core import load_module
from starterpyth.log import green

__author__ = 'd9pouces'

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
    ]

    def __init__(self, dist=None):
        super(CompileMessages, self).__init__(dist=dist)
        self.language = 'fr_FR'
        self.dest = None

    def initialize_options(self):
        self.language = 'fr_FR'
        self.dest = None

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
            mo_file = os.path.join(locale_dir, self.language, 'LC_MESSAGES', '%s.mo' % module_name)
            po_file = os.path.join(locale_dir, self.language, 'LC_MESSAGES', '%s.po' % module_name)
            if not os.path.isdir(os.path.dirname(mo_file)):
                os.makedirs(os.path.dirname(mo_file))
            if os.path.isfile(po_file):
                cmd = 'msgfmt --output-file %s %s' % (mo_file, po_file)
                print(green(_('Processing file %(filename)s.') % {'filename': po_file}))
                subprocess.check_call(cmd, shell=True, stderr=subprocess.PIPE)
