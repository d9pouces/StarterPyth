import codecs
import datetime
from distutils.core import Command
import logging
import os
import subprocess
from jinja2 import Environment, PackageLoader
from setuptools import find_packages
from starterpyth.core import load_module

from starterpyth.translation import gettext as _
from starterpyth.utils import my_unicode


class MakeMessages(Command):
    """Generate message files for i18n"""
    description = '''Generate message files for i18n'''
    user_options = [
        ('language=', 'l', "target language (default: fr_FR)"),
        ('dest=', 'd', "output dir, relative to the top-level package folder (default: locale)"),
    ]

    def initialize_options(self):
        self.language = 'fr_FR'
        self.dest = None

    def finalize_options(self):
        pass

    def run(self):
        module_names = find_packages()
        dst_rel_path = 'locale' if self.dest is None else self.dest
        # group by top-level packages and compute their directories:
        all_modules = {}
        top_levels_modules = {}
        for module_name in module_names:
            tl, sep, bl = module_name.partition('.')
            all_modules.setdefault(tl, []).append(module_name)
            if tl not in top_levels_modules:
                top_levels_modules[tl] = os.path.dirname(load_module(tl).__file__)
        env = Environment(loader=PackageLoader('starterpyth.commands.makemessages', 'templates'))
        template = env.get_template('lang.po')
        context = {
            'description': self.distribution.get_description(),
            'copyright': self.distribution.get_author(),
            'package': None,
            'author': self.distribution.get_author(),
            'version': self.distribution.get_version(),
            'email': self.distribution.get_author_email(),
            'year': datetime.datetime.now().year,
        }
        for tl_name in top_levels_modules.keys():
            dst_abs_path = os.path.join(top_levels_modules[tl_name], dst_rel_path)
            pot_file = os.path.join(dst_abs_path, '%s.pot' % tl_name)
            po_file = os.path.join(dst_abs_path, self.language, 'LC_MESSAGES', '%s.po' % tl_name)
            if not os.path.isdir(os.path.dirname(po_file)):
                os.makedirs(os.path.dirname(po_file))
            for filename in (pot_file, po_file):
                if not os.path.isfile(filename):
                    context['package'] = tl_name
                    with codecs.open(filename, 'w', encoding='utf-8') as fd:
                        fd.write(template.render(context))
        for tl_name, module_names in all_modules.items():
            dst_abs_path = os.path.join(top_levels_modules[tl_name], dst_rel_path)
            root_path = os.path.dirname(top_levels_modules[tl_name])
            print(root_path)
            pot_file = os.path.join(dst_abs_path, '%s.pot' % tl_name)
            po_file = os.path.join(dst_abs_path, self.language, 'LC_MESSAGES', '%s.po' % tl_name)
            # build the list of files to examine, for each top-level module
            filenames = []
            for module_name in module_names:
                init_filename = load_module(module_name).__file__
                local_root = os.path.dirname(init_filename)
                for filename in os.listdir(local_root):
                    filename = os.path.join(local_root, filename)
                    basename, sep, ext = filename.rpartition('.')
                    if ext not in ('py', 'pyx', 'c'):
                        continue
                    try:
                        with codecs.open(filename, 'r', encoding='utf-8') as fd:
                            fd.read()
                        filenames.append(os.path.relpath(filename, root_path))
                        logging.info(_('%(filename)s added.') % {'filename': filename})
                    except UnicodeDecodeError:
                        logging.error(_('Encoding of %(filename)s is not UTF-8.') % {'filename': filename})
            cmd = ['xgettext', '--language=Python', '--keyword=_', my_unicode('--output=%s') % pot_file,
                   '--from-code=UTF-8', '--add-comments=Translators', ] + filenames
            subprocess.check_call(cmd, stdout=subprocess.PIPE)
            if os.path.isfile(po_file):
                cmd = ['msgmerge', '--update', '--backup=off', po_file, pot_file, ]
            else:
                cmd = ['msginit', '--no-translator', '-l', self.language, my_unicode('--input=%s') % pot_file,
                       my_unicode('--output=%s') % po_file, ]
            subprocess.check_call(cmd, stderr=subprocess.PIPE)
            logging.warning(_('Please translate strings in %(filename)s') % {'filename': po_file})