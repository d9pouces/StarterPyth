import copy
import logging
from optparse import OptionParser
import os.path
import imp
import sys

import pkg_resources
from six import u

import starterpyth.log
import starterpyth.utils
from starterpyth.translation import ugettext as _

__author__ = 'd9pouces'


INTERACTIVE = True
DEFAULT_EXTENSIONS = ['starterpyth.plugins.base:BasePlugin', 'starterpyth.plugins.starter_django:DjangoPlugin',
                      'starterpyth.plugins.cli:CliPlugin', 'starterpyth.plugins.starter_cython:CythonPlugin',
                      ]


def load_module(modulename):
    parents = modulename.split(u('.'))
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

    @staticmethod
    def get_template(context, modname, filename):
        """
        Render a single template.
        :param context: dict
        :param modname: str
        :param filename: str
        :return:
        """
        from jinja2 import Environment, PackageLoader
        from jinja2.loaders import ChoiceLoader
        dirname, filename = filename.rsplit(u('/'), 1)
        loader = ChoiceLoader([PackageLoader(u('starterpyth'), u('templates')), PackageLoader(modname, dirname)])
        env = Environment(loader=loader)
        template = env.get_template(filename)
        return template.render(**context)

    def get_excluded_files(self, context):
        return []

    def write_files(self, context, filters):
        """
        Write template or raw files to the new project
        :param context: dict context (dict) to be used by jinja2
        :param filters: list extra filters for jinja2
        :return:
        """
        from jinja2 import Environment, PackageLoader, Template
        from jinja2.loaders import ChoiceLoader
        local_context = copy.copy(context)
        local_context.update(self.get_local_context(local_context))
        excludes = self.get_excluded_files(local_context)
        modname, dirname = self.get_resources()
        if modname is None or dirname is None:
            return
        loader = ChoiceLoader([PackageLoader('starterpyth', 'templates'), PackageLoader(modname, dirname)])
        env = Environment(loader=loader)
        env.filters.update(filters)
        project_root = os.path.join(context['project_root'], context['project_name'])
        if not os.path.isdir(project_root):
            msg = _('Directory %(f)s created.') % {'f': project_root}
            logging.info(msg)
            os.makedirs(project_root)
        # noinspection PyTypeChecker
        prefix_len = len(dirname) + 1

        def get_path(root_, name):
            """return relative source path (to template dir) and destination path"""
            src_path_ = (root_ + '/' + name)[prefix_len:]
            dst_path_ = src_path_
            if os.sep != '/':
                dst_path_ = dst_path_.replace('/', os.sep)
            if dst_path_.find('{') > -1:
                dst_path_ = Template(dst_path_).render(**local_context)
            if dst_path_[-4:] == '_tpl':
                dst_path_ = dst_path_[:-4]
            return src_path_, os.path.join(project_root, dst_path_)
        for root, dirnames, filenames in starterpyth.utils.walk(modname, dirname):
            for dirname in dirnames:
                src_path, dst_path = get_path(root, dirname)
                if src_path in excludes:
                    continue
                if not os.path.isdir(dst_path):
                    msg = _('Directory %(f)s created.') % {'f': dst_path}
                    logging.info(msg)
                    os.makedirs(dst_path)
            for filename in filenames:
                if filename[-4:] == '_inc':
                    continue
                src_path, dst_path = get_path(root, filename)
                if src_path in excludes:
                    continue
                if not os.path.isdir(os.path.dirname(dst_path)):
                    continue
                if filename[-4:] == '_tpl':
                    template = env.get_template(src_path)
                    f_out = open(dst_path, 'ab')
                    f_out.write(template.render(**local_context).encode('utf-8'))
                    f_out.close()
                    msg = _('Template %(f)s written.') % {'f': dst_path}
                    logging.info(msg)
                else:
                    f_out = open(dst_path, 'wb')
                    f_in = pkg_resources.resource_stream(modname, root + '/' + filename)
                    data = f_in.read(10240)
                    while data:
                        f_out.write(data)
                        data = f_in.read(10240)
                    f_in.close()
                    f_out.close()
                    msg = _('File %(f)s written.') % {'f': dst_path}
                    logging.info(msg)

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
