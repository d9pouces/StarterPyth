# -*- coding: utf-8 -*-
"""Evaluate the quality of your code
---------------------------------

Define a basic pylint call.

Usage:

.. code-block:: bash

  pip install pylint
  python setup.py lint

"""
from starterpyth.log import RED
from starterpyth.log import display

__author__ = 'Matthieu Gallet'

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
            display(_('package pylint is required.'), color=RED)
            return 1
        pylint.lint.Run((self.distribution.get_name(), ), exit=False)