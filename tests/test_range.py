# coding=UTF-8
from __future__ import print_function, absolute_import, division

import unittest

from firanka.ranges import Range


class TestRange(unittest.TestCase):
    def do_intersect(self, a, b, val):
        if type(val) == bool:
            p = Range(a).intersection(b)
            if p.is_empty() != val:
                self.fail(
                    '%s ^ %s [=> %s] != %s' % (Range(a), Range(b), p, val))
            p = Range(b).intersection(a)
            if p.is_empty() != val:
                self.fail(
                    '%s ^ %s [=> %s] != %s' % (Range(b), Range(a), p, val))
        else:
            self.assertEqual(Range(a).intersection(b), Range(val))
            self.assertEqual(Range(b).intersection(a), Range(val))

    def test_slicing(self):
        self.assertTrue(Range('<-5;5>')[0:] == Range('<0;5>'))

    def test_isempty(self):
        self.assertTrue(Range(-1, -1, False, False).is_empty())
        self.assertFalse(Range(-1, -1, False, True).is_empty())
        self.assertEqual(Range(0, 0, False, False), Range(2, 2, False, False))

    def test_intersection(self):
        self.do_intersect('<-10;1>', '<2;3>', True)
        self.do_intersect('<10;1)', '(-1;3>', True)
        self.do_intersect('<-10;-1)', '<-1;1>', True)
        self.do_intersect('<-10;-1)', '(-1;3>', True)
        self.do_intersect('<-10;2)', '<1;5>', '<1;2)')
        self.do_intersect('<-5;5>', '(-5;5)', '(-5;5)')

    def test_str_and_repr_and_bool(self):
        p = Range(-1, 1, True, True)
        self.assertEqual(eval(repr(p)), p)
        self.assertEqual(str(Range(-1, 1)), '<-1;1>')

    def test_constructor(self):
        self.assertRaises(ValueError, lambda: Range('#2;3>'))
        self.assertRaises(ValueError, lambda: Range('(2;3!'))
        self.assertRaises(ValueError, lambda: Range('<-inf;3)'))
        self.assertEqual(Range(1, 2, True, False), Range('<1;2)'))
        self.assertEqual(Range(1, 2, True, False), '<1;2)')

    def test_contains(self):
        self.assertFalse(-1 in Range('<-10;-1)'))
        self.assertTrue(-10 in Range('<-10;-1)'))
        self.assertFalse(-10 in Range('(-10;-1>'))
        self.assertTrue(-1 in Range('(-10;-1>'))
        self.assertTrue(-5 in Range('(-10;-1>'))
        self.assertFalse(-20 in Range('(-10;-1>'))
        self.assertFalse(1 in Range('(-10;-1>'))

        self.assertTrue(Range('<-5;5>') in Range('<-10;10>'))
        self.assertTrue('(-1;6)' in Range(-10.0, 10.0, True, False))
        self.assertTrue('<0.5;1.5>' in Range('<0;2>'))
