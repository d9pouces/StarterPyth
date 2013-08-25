"""
Define a basic pylint call.
"""
__author__ = 'd9pouces'

from distutils.core import Command
import pylint.lint


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
        pylint.lint.Run((self.distribution.get_name(), ), exit=False)

