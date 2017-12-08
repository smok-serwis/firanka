# coding=UTF-8
from __future__ import print_function, absolute_import, division
import six
import unittest
from firanka.series import Range



class TestRange(unittest.TestCase):

    def do_intersect(self, a, b, val):
        self.assertEqual(bool(Range(a).intersection(b)), val)
        self.assertEqual(bool(Range(b).intersection(a)), val)

    def test_intersection(self):
        self.do_intersect(Range(-10, -1, True, True), '<2;3>', False)
        self.do_intersect(Range(-10, -1, True, False), '(-1;3>', False)
        self.do_intersect('<-10;-1)', '<-1;1>', False)

    def test_str(self):
        self.assertEqual(str(Range(-1, 1, True, True)), '<-1;1>')

    def test_constructor(self):
        self.assertRaises(ValueError, lambda: Range('#2;3>'))
        self.assertRaises(ValueError, lambda: Range('(2;3!'))

    def test_contains(self):
        self.assertFalse(-1 in Range('<-10;-1)'))
        self.assertTrue(-10 in Range('<-10;-1)'))
        self.assertFalse(-10 in Range('(-10;-1>'))
        self.assertTrue(-1 in Range('(-10;-1>'))
        self.assertTrue(-5 in Range('(-10;-1>'))
        self.assertFalse(-20 in Range('(-10;-1>'))
        self.assertFalse(1 in Range('(-10;-1>'))
