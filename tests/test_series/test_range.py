# coding=UTF-8
from __future__ import print_function, absolute_import, division
import six
import unittest
from firanka.series import Range


class TestRange(unittest.TestCase):
    def test_intersection(self):
        self.assertFalse(Range(-10, -1, True, True).intersection('<2;3>'))
        self.assertFalse(Range(-10, -1, True, False).intersection('(-1;3>'))
        self.assertFalse(Range('<-10;-1)').intersection('<-1;1>'))

    def test_str(self):
        self.assertEqual(str(Range(-1, 1, True, True)), '<-1;1>')

    def test_contains(self):
        self.assertFalse(-1 in Range('<-10;-1)'))
        self.assertTrue(-10 in Range('<-10;-1)'))
        self.assertFalse(-10 in Range('(-10;-1>'))
        self.assertTrue(-1 in Range('(-10;-1>'))
        self.assertTrue(-5 in Range('(-10;-1>'))
        self.assertFalse(-20 in Range('(-10;-1>'))
        self.assertFalse(1 in Range('(-10;-1>'))
