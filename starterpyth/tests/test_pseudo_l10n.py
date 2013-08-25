#coding=utf-8
from starterpyth.utils import py3k_unicode

__author__ = 'd9pouces'

import unittest
from starterpyth.commands.pseudo_l10n import translate_string


class TranslationTest(unittest.TestCase):
    """Test cases for :mod:`starterpyth.commands.pseudo_l10n`."""

    def test_1(self):
        """Test the sample_function with two arguments."""
        self.assertEqual(translate_string(py3k_unicode('ab')), py3k_unicode('[ƒ——!ab!—–]'))

if __name__ == '__main__':
    unittest.main()
