import codecs
import datetime
from distutils.core import Command
import os
import subprocess
from six import u
from starterpyth.log import red, green, yellow

try:
    from jinja2 import Environment, PackageLoader
except ImportError:
    Environment, PackageLoader = None, None
from setuptools import find_packages
from starterpyth.core import load_module

from starterpyth.translation import gettext as _


class MakeMessages(Command):
    """Generate message files for i18n"""
    description = '''Generate message files for i18n'''
    user_options = [
        ('language=', 'l', "target language (default: fr_FR)"),
        ('dest=', 'd', "output dir, relative to the top-level package folder (default: locale)"),
    ]

    def __init__(self, dist=None):
        super(MakeMessages, self).__init__(dist=dist)
        self.language = 'fr_FR'
        self.dest = None

    def initialize_options(self):
        self.language = 'fr_FR'
        self.dest = None

    def finalize_options(self):
        pass

    def run(self):
        if Environment is None:
            print(red(_('package jinja2 is required.')))
            return 1
        module_names = find_packages()
        dst_rel_path = 'locale' if self.dest is None else self.dest
        # group by top-level packages and compute their directories:
        all_modules = {}
        top_levels_modules = {}
        for module_name in module_names:
            top_module = module_name.partition('.')[0]
            all_modules.setdefault(top_module, []).append(module_name)
            if top_module not in top_levels_modules:
                top_levels_modules[top_module] = os.path.dirname(load_module(top_module).__file__)
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
            pot_filename = os.path.join(dst_abs_path, '%s.pot' % tl_name)
            po_filename = os.path.join(dst_abs_path, self.language, 'LC_MESSAGES', '%s.po' % tl_name)
            if not os.path.isdir(os.path.dirname(po_filename)):
                os.makedirs(os.path.dirname(po_filename))
            for filename in (pot_filename, po_filename):
                if not os.path.isfile(filename):
                    context['package'] = tl_name
                    po_fd = codecs.open(filename, 'w', encoding='utf-8')
                    po_fd.write(template.render(context))
                    po_fd.close()
        for tl_name, module_names in all_modules.items():
            dst_abs_path = os.path.join(top_levels_modules[tl_name], dst_rel_path)
            root_path = os.path.dirname(top_levels_modules[tl_name])
            print(root_path)
            pot_filename = os.path.join(dst_abs_path, '%s.pot' % tl_name)
            po_filename = os.path.join(dst_abs_path, self.language, 'LC_MESSAGES', '%s.po' % tl_name)
            # build the list of files to examine, for each top-level module
            filenames = []
            for module_name in module_names:
                init_filename = load_module(module_name).__file__
                local_root = os.path.dirname(init_filename)
                for filename in os.listdir(local_root):
                    filename = os.path.join(local_root, filename)
                    basename, sepa, ext = filename.rpartition('.')
                    if ext not in ('py', 'pyx', 'c'):
                        continue
                    try:
                        po_fd = codecs.open(filename, 'r', encoding='utf-8')
                        po_fd.read()
                        po_fd.close()
                        filenames.append(os.path.relpath(filename, root_path))
                        msg = _('%(filename)s added.') % {'filename': filename}
                        print(green(msg))
                    except UnicodeDecodeError:
                        msg = _('Encoding of %(filename)s is not UTF-8.') % {'filename': filename}
                        print(green(msg))
            cmd = ['xgettext', '--language=Python', '--keyword=_', u('--output=%s') % pot_filename,
                   '--from-code=UTF-8', '--add-comments=Translators', ] + filenames
            subprocess.check_call(cmd, stdout=subprocess.PIPE)
            if os.path.isfile(po_filename):
                cmd = ['msgmerge', '--update', '--backup=off', po_filename, pot_filename, ]
            else:
                cmd = ['msginit', '--no-translator', '-l', self.language, u('--input=%s') % pot_filename,
                       u('--output=%s') % po_filename, ]
            subprocess.check_call(cmd, stderr=subprocess.PIPE)
            msg = _('Please translate strings in %(filename)s') % {'filename': po_filename}
            print(yellow(msg))
            msg = _('Then run setup.py compilemessages -l %(lang)s') % {'lang': self.language}
            print(yellow(msg))
