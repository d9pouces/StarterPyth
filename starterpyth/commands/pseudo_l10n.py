#coding=utf-8
import logging
from setuptools import find_packages
from starterpyth.core import load_module
from starterpyth.utils import my_unicode

__author__ = 'flanker'

from distutils.core import Command
import polib
import os
import subprocess

from starterpyth.translation import gettext as _

def translate_string(src_str):
    """
    Transform a ASCII string into a larger string with non-ASCII characters.

    >>> translate_string(my_unicode('ab')) == my_unicode('[!!!—æß—!!!]')
    True

    """
    dst_str = src_str
    return my_unicode('[ƒ——!{0}!—–]').format(dst_str)


class PseudoL10N(Command):
    """Compile message files for i18n"""
    description = '''Compile message files for i18n'''
    user_options = [
        ('langage=', 'l', "target language (default: xx_XX)"),
        ('dest=', 'd', "output dir"),
    ]

    def initialize_options(self):
        self.language = 'xx_XX'
        self.dest = None

    def finalize_options(self):
        pass

    def run(self):
        module_names = find_packages()
        dst_rel_path = 'locale' if self.dest is None else self.dest
        # group by top-level packages and compute their directories:
        top_levels_modules = {}
        for module_name in module_names:
            top_level = module_name.partition('.')[0]
            if top_level not in top_levels_modules:
                locale_dir = os.path.join(os.path.dirname(load_module(top_level).__file__), dst_rel_path)
                top_levels_modules[top_level] = locale_dir

        for module_name, locale_dir in top_levels_modules.items():
            po_filename = os.path.join(locale_dir, self.language, 'LC_MESSAGES', '%s.po' % module_name)
            if not os.path.isfile(po_filename):
                logging.warning(_('Missing file: %(filename)s. Please run the makemessages -l xx_XX command first.')
                                % {'filename': po_filename})
                continue
            po_content = polib.pofile(po_filename)
            for entry in po_content:
                entry.msgstr = translate_string(entry.msgid)
            logging.info(_('Processed file: %(filename)s.') % {'filename': po_filename})
            po_content.save(po_filename)
