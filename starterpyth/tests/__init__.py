"""
Package gathering all unitary tests for {{ module_name }}.
Module names must start with `test_` to be taken into account.

You should consider to install :mod:`Distribute` to run all tests with::

    $ python setup.py test

"""
__author__ = 'd9pouces'
__all__ = []  # 'load_tests']

# import os.path
import unittest


# def load_tests(loader=None, standard_tests=None, pattern=None):
#     """Automatically discover test cases in files whose
#     name starts with `test_`. Follows the `load_tests` Protocol.
#
#     Kwargs:
#         * `loader` (:class:`unittest.TestLoader`):
#         * `standard_tests` (:class:`unittest.TestSuite`):
#         * `pattern` (:py:class:`str`):
#
#     Return:
#         * :class:`unittest.TestSuite` `standard_tests` augmented with
#             all tests defined in this package.
#     """
#     if loader is None:
#         loader = unittest.TestLoader()
#     if pattern is None:
#         pattern = 'test_*.py'
#     if standard_tests is None:
#         standard_tests = unittest.TestSuite()
#     package_tests = loader.discover(os.path.dirname(__file__), pattern=pattern)
#     standard_tests.addTests(package_tests)
#     return standard_tests


if __name__ == '__main__':
    unittest.main()
