"""
Define a basic pylint call.
"""
from starterpyth.log import red

__author__ = 'd9pouces'

from distutils.core import Command
try:
    import pylint.lint
except ImportError:
    pylint = None
from starterpyth.translation import gettext as _


class Lint(Command):
    """Evaluate code quality through pylint"""
    # pylint: disable=R0904
    description = '''Evaluate code quality through pylint'''
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if pylint is None:
            print(red(_('package pylint is required.')))
            return 1
        pylint.lint.Run((self.distribution.get_name(), ), exit=False)