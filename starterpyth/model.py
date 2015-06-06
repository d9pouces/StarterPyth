# -*- coding=utf-8 -*-
import datetime
import json
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
from jinja2 import ChoiceLoader
import pkg_resources
from six import u

from starterpyth.cliforms import BaseForm
from starterpyth.utils import binary_path, walk
from starterpyth.log import display, GREEN, CYAN, RED
from starterpyth.translation import ugettext as _


__author__ = 'flanker'


class Model(object):
    name = None
    template_includes = [('starterpyth', 'templates/includes')]
    include_suffix = '_inc'
    template_suffix = '_tpl'

    class ExtraForm(BaseForm):
        pass

    def __init__(self, base_context):
        """

        :param base_context: dictionnary with the following keys:
            string values
                * project_name: explicit name of the project ( [a-zA-Z_\-]\w* )
                * module_name: Python base module ( [a-z][\-_a-z0-9]* )
            some boolean values:
                * use_py2, use_py3: use Python 2 or Python 3
                * use_py26, use_py27, use_py30, use_py31, use_py32, use_py33, use_py34, use_py35
                * use_six, use_2to3: use six or 2to3 for Python 2&3 compatibility
        """
        self.global_context = base_context
        self.file_context = None

    @property
    def template_roots(self):
        result = []
        return result

    def run(self, interactive=True):
        project_root = self.global_context['project_root']
        if os.path.exists(project_root):
            if self.global_context['overwrite']:
                if os.path.isdir(project_root):
                    shutil.rmtree(project_root)
                else:
                    os.remove(project_root)
            else:
                display(_('Destination path already exists!'), color=RED, bold=True)
                return

        context = self.get_context()
        self.global_context.update(context)
        extra_form = self.get_extraform(interactive=interactive)
        self.global_context.update(extra_form)
        extra_context = self.get_extracontext()
        self.global_context.update(extra_context)
        filters = self.get_template_filters()

        self.set_virtualenvs()

        for modname, dirname in self.template_roots:
            display('dirname %s' % dirname, color=CYAN)
            env = self.get_environment(modname, dirname, filters)
            self.write_files(modname, dirname, env)

    def set_virtualenvs(self):
        virtualenv_path = None
        virtualenv_version = None
        for k in ('26', '27', '30', '31', '32', '33', '34', '35'):
            v = '%s.%s' % (k[0], k[1])
            if self.global_context['create_venv%s' % k]:
                if self.global_context['virtualenv_present']:
                    virtualenv_path = ('~/.virtualenvs/%s%s' % (self.global_context['module_name'], k))
                    python_path = binary_path('python%s' % v)
                    subprocess.check_call(['virtualenv', os.path.expanduser(virtualenv_path), '-p', python_path])
                    cmd_list = [os.path.join(os.path.expanduser(virtualenv_path), 'bin', 'python'), '--version']
                    p = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    content = p.communicate()
                    if content[0]:  # Python 3 prints version on stdout
                        # noinspection PyUnresolvedReferences
                        virtualenv_version = content[0].decode('utf-8').strip()
                    else:  # Python 2 prints version on stderr
                        # noinspection PyUnresolvedReferences
                        virtualenv_version = content[1].decode('utf-8').strip()
        self.global_context['virtualenv'] = (virtualenv_path, virtualenv_version)

    # noinspection PyMethodMayBeStatic
    def get_context(self):
        values = {'encoding': 'utf-8', 'entry_points': {}, 'cmdclass': {}, 'ext_modules': [],
                  'install_requires': [], 'setup_requires': [], 'classifiers': []}
        if self.global_context['use_six']:
            values['install_requires'] += ['six', 'setuptools>=1.0', ]
            values['setup_requires'] += ['six', 'setuptools>=1.0', ]
        license_fd = pkg_resources.resource_stream('starterpyth',
                                                   'data/licenses/%s.txt' % self.global_context['license'])
        values['license_content'] = license_fd.read().decode('utf-8')
        values['copyright'] = u('%d, %s') % (datetime.date.today().year, self.global_context['author'])
        self.global_context['used_python_versions'] = []
        for k in ('26', '27', '30', '31', '32', '33', '34', '35'):
            v = '%s.%s' % (k[0], k[1])
            if self.global_context['use_py%s' % k]:
                self.global_context['used_python_versions'].append(v)
        values['tox_used_python_versions'] = [('py' + x[0] + x[-1]) for x in self.global_context['used_python_versions']]
        return values

    # noinspection PyMethodMayBeStatic
    def get_extracontext(self):
        return {}

    def get_extraform(self, interactive=True):
        form = self.ExtraForm(extra_env=self.global_context)
        values = form.read(interactive=interactive)
        return values

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def process_directory_or_file(self, src_path, dst_path, name, is_directory):
        """
        :param src_path: source path, relative to python module
        :param dst_path: absolute destination path
        :param name: basename of the file or directory to be processed
        :return:
        """
        if name in ['.svn', '.git', '.hg', 'CVS'] or name[-len(self.include_suffix):] == self.include_suffix:
            return False
        return True

    # noinspection PyMethodMayBeStatic
    def get_environment(self, modname, dirname, filters):
        """
        Return a valid Jinja2 environment (with filters)
        :param modname:
        :param dirname:
        :param filters: dictionnary of extra filters for jinja2
        :return:
        """
        from jinja2 import Environment, PackageLoader
        loaders = [PackageLoader(modname, dirname)]
        for modname, dirname in self.template_includes:
            loaders.append(PackageLoader(modname, dirname))
        loader = ChoiceLoader(loaders)
        env = Environment(loader=loader)
        env.filters.update(filters)
        return env

    def write_files(self, modname, dirname, env):
        """
        Write all templated or raw files to the new project. All template are rendered twice.
        This behaviour allows to determine which functions must be imported at the beginning of Python files
        :param modname: module containing template files
        :param dirname: dirname containing template files in the module `modname`
        :param env: Jinja2 environment
        :return:
        """
        from jinja2 import Template
        project_root = self.global_context['project_root']
        # creation of the project directory if needed
        if not os.path.isdir(project_root):
            os.makedirs(project_root)
            display(_('Directory %(f)s created.') % {'f': project_root}, color=GREEN)
        # noinspection PyTypeChecker
        prefix_len = len(dirname) + 1

        def get_path(root_, name):
            """return relative source path (to template dir) and absolute destination path"""
            src_path_ = (root_ + '/' + name)[prefix_len:]
            dst_path_ = src_path_
            if os.sep != '/':
                dst_path_ = dst_path_.replace('/', os.sep)
            if dst_path_.find('{') > -1:  # the name of the file is templated
                dst_path_ = Template(dst_path_).render(**self.global_context)
            if dst_path_[-len(self.template_suffix):] == self.template_suffix:
                dst_path_ = dst_path_[:-len(self.template_suffix)]
            return src_path_, os.path.join(project_root, dst_path_)

        # walk through all files (raw and templates) in modname/dirname and write them to destination
        for root, dirnames, filenames in walk(modname, dirname):
            for dirname in dirnames:
                src_path, dst_path = get_path(root, dirname)
                if not self.process_directory_or_file(src_path, dst_path, dirname, True):
                    continue
                if not os.path.isdir(dst_path):
                    os.makedirs(dst_path)
                    display(_('Directory %(f)s created.') % {'f': dst_path}, color=GREEN)
            for filename in filenames:
                src_path, dst_path = get_path(root, filename)
                if not self.process_directory_or_file(src_path, dst_path, filename, False):
                    continue
                if not os.path.isdir(os.path.dirname(dst_path)):
                    continue
                if filename[-len(self.template_suffix):] == self.template_suffix:
                    self.file_context = {'render_pass': 1}
                    template = env.get_template(src_path)
                    f_out = open(dst_path, 'wb')
                    self.file_context.update(self.global_context)
                    template.render(**self.file_context)
                    self.file_context['render_pass'] = 2
                    template_content = template.render(**self.file_context).encode('utf-8')
                    f_out.write(template_content)
                    f_out.close()
                    display(_('Template %(f)s written.') % {'f': dst_path}, color=GREEN)
                else:
                    f_out = open(dst_path, 'wb')
                    f_in = pkg_resources.resource_stream(modname, root + '/' + filename)
                    data = f_in.read(10240)
                    while data:
                        f_out.write(data)
                        data = f_in.read(10240)
                    f_in.close()
                    f_out.close()
                    display(_('File %(f)s written.') % {'f': dst_path}, color=GREEN)

    def increment(self, key):
        self.file_context[key] = self.file_context.get(key, 0) + 1

    def text(self, value):
        return self.raw_text(value)

    def raw_text(self, value):
        if '\n' in value:
            prefix = '"""'
        elif "'" not in value:
            prefix = "'"
        elif '"' not in value:
            prefix = '"'
        else:
            value = value.replace("'", "\\'")
            prefix = "'"
        self.increment('counter_unicode_literals')
        return '%s%s%s' % (prefix, value, prefix)

    def docstring(self, value):
        self.increment('counter_unicode_literals')
        return '"""%s"""' % value

    def translate(self, value):
        if not self.global_context['use_i18n']:
            return self.text(value)
        self.increment('counter_i18n')
        return "_(%s)" % self.text(value)

    def binary(self, value):
        return 'b' + self.raw_text(value)

    def get_template_filters(self):
        return {'text': self.text, 'binary': self.binary, 'repr': lambda x: repr(x), 'translate': self.translate,
                'docstring': self.docstring, 'raw_text': self.raw_text}


if __name__ == '__main__':
    import doctest

    doctest.testmod()