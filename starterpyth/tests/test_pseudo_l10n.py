#coding=utf-8
from starterpyth.utils import my_unicode

__author__ = 'flanker'

import unittest
from starterpyth.commands.pseudo_l10n import translate_string


class TranslationTest(unittest.TestCase):
    """Test cases for :mod:`starterpyth.commands.pseudo_l10n`."""

    def test_1(self):
        """Test the sample_function with two arguments."""
        self.assertEqual(translate_string(my_unicode('ab')), my_unicode('[ƒ——!ab!—–]'))

if __name__ == '__main__':
    unittest.main()