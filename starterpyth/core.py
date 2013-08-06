import copy
import logging
import logging.config
from optparse import OptionParser
import os.path
import imp
import sys

from jinja2 import Environment, PackageLoader, Template
import pkg_resources

import starterpyth.log
import starterpyth.utils
from starterpyth.translation import ugettext as _

__author__ = 'flanker'


INTERACTIVE = True
DEFAULT_EXTENSIONS = ['starterpyth.plugins.base:BasePlugin', 'starterpyth.plugins.starter_django:DjangoPlugin',
                      'starterpyth.plugins.cli:CliPlugin', 'starterpyth.plugins.starter_cython:CythonPlugin',
                      ]


def load_module(modulename):
    parents = modulename.split('.')
    path = sys.path
    module = None
    for module_name in parents:
        (file_, pathname, description) = imp.find_module(module_name, path)
        module = imp.load_module(module_name, file_, pathname, description)
        path = [os.path.dirname(module.__file__)]
    return module


class Plugin(object):

    def update_global_context(self, context, filters):
        pass

    def get_template(self, context, modname, filename):
        dirname, filename = filename.rsplit('/', 1)
        env = Environment(loader=PackageLoader(modname, dirname))
        template = env.get_template(filename)
        return template.render(**context)

    def write_files(self, context, filters):
        local_context = copy.copy(context)
        local_context.update(self.get_local_context(local_context))
        modname, dirname = self.get_resources()
        if modname is None or dirname is None:
            return
        env = Environment(loader=PackageLoader(modname, dirname))
        env.filters.update(filters)
        project_root = os.path.join(context['project_root'], context['project_name'])
        if not os.path.isdir(project_root):
            logging.info(_('Directory %(f)s created.') % {'f': project_root})
            os.makedirs(project_root)
        # noinspection PyTypeChecker
        prefix_len = len(dirname) + 1

        def get_path(root, name):
            """return relative source path (to template dir) and destination path"""
            src_path = (root + '/' + name)[prefix_len:]
            dst_path = src_path
            if os.sep != '/':
                dst_path = dst_path.replace('/', os.sep)
            if dst_path.find('{') > -1:
                dst_path = Template(dst_path).render(**context)
            if dst_path[-4:] == '_tpl':
                dst_path = dst_path[:-4]
            return src_path, os.path.join(project_root, dst_path)

        for root, dirnames, filenames in starterpyth.utils.walk(modname, dirname):
            for dirname in dirnames:
                src_path, dst_path = get_path(root, dirname)
                if not os.path.isdir(dst_path):
                    logging.info(_('Directory %(f)s created.') % {'f': dst_path})
                    os.makedirs(dst_path)
            for filename in filenames:
                if filename[-4:] == '_inc':
                    continue
                src_path, dst_path = get_path(root, filename)
                if filename[-4:] == '_tpl':
                    template = env.get_template(src_path)
                    with open(dst_path, 'ab') as f_out:
                        f_out.write(template.render(**context).encode('utf-8'))
                    logging.info(_('Template %(f)s written.') % {'f': dst_path})
                else:
                    with open(dst_path, 'wb') as f_out:
                        with pkg_resources.resource_stream(modname, root + '/' + filename) as f_in:
                            data = f_in.read(10240)
                            while data:
                                f_out.write(data)
                                data = f_in.read(10240)
                    logging.info(_('File %(f)s written.') % {'f': dst_path})

    def get_resources(self):
        return None, None

    # noinspection PyUnusedLocal
    def get_local_context(self, context):
        return {}

    def is_selected(self):
        return True


def main():
    global INTERACTIVE
    parser = OptionParser(usage=_('%(bin)s [-extension my.extension.module:class]') % {'bin': sys.argv[0]})
    parser.add_option('--extension', '-e', action='append', dest='extensions', default=[],
                      help=_('extra extension module'))
    parser.add_option('-v', '--verbose', action='store_true', help='print more messages', default=False)
    parser.add_option('--nointeractive', '-n', action='store_true', dest='nointeractive', default=False,
                      help=_('no interactive mode'))
    parser.add_option('--target', '-t', action='store', dest='target', default='.',
                      help=_('base folder for the new project'))
    options, args = parser.parse_args(sys.argv[1:])
    if options.nointeractive:
        INTERACTIVE = False
    log_config = starterpyth.log.CONSOLE
    if options.verbose:
        log_config['root']['level'] = 'DEBUG'
    else:
        log_config['root']['level'] = 'WARNING'
    logging.config.dictConfig(log_config)
    extensions = DEFAULT_EXTENSIONS + options.extensions
    context = {'project_root': options.target, 'entry_points': {}, 'install_requires': [], 'setup_requires': [],
               'tests_requires': [], 'doc_urls': {}, 'ext_modules': [], 'extra_setup': [], 'classifiers': [], }
    filters = {}

    classes = []
    for extension in extensions:
        module_name, class_name = extension.split(':', 1)
        module = load_module(module_name)
        cls = getattr(module, class_name)()
        classes.append(cls)
    for cls in classes:
        cls.update_global_context(context, filters)
    for cls in classes:
        if cls.is_selected():
            cls.write_files(context, filters)


if __name__ == '__main__':
    import doctest
    doctest.testmod()