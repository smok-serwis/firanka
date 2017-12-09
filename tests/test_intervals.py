# coding=UTF-8
from __future__ import print_function, absolute_import, division

import unittest

from firanka.intervals import Interval


class TestIntervals(unittest.TestCase):
    def do_intersect(self, a, b, val):
        if type(val) == bool:
            p = Interval(a).intersection(b)
            if p.is_empty() != val:
                self.fail(
                    '%s ^ %s [=> %s] != %s' % (Interval(a), Interval(b), p, val))
            p = Interval(b).intersection(a)
            if p.is_empty() != val:
                self.fail(
                    '%s ^ %s [=> %s] != %s' % (Interval(b), Interval(a), p, val))
        else:
            self.assertEqual(Interval(a).intersection(b), Interval(val))
            self.assertEqual(Interval(b).intersection(a), Interval(val))

    def test_slicing(self):
        self.assertTrue(Interval('<-5;5>')[0:] == Interval('<0;5>'))

    def test_isempty(self):
        self.assertTrue(Interval(-1, -1, False, False).is_empty())
        self.assertFalse(Interval(-1, -1, False, True).is_empty())
        self.assertEqual(Interval(0, 0, False, False), Interval(2, 2, False, False))

    def test_intersection(self):
        self.do_intersect('<-10;1>', '<2;3>', True)
        self.do_intersect('<10;1)', '(-1;3>', True)
        self.do_intersect('<-10;-1)', '<-1;1>', True)
        self.do_intersect('<-10;-1)', '(-1;3>', True)
        self.do_intersect('<-10;2)', '<1;5>', '<1;2)')
        self.do_intersect('<-5;5>', '(-5;5)', '(-5;5)')

    def test_str_and_repr_and_bool(self):
        p = Interval(-1, 1, True, True)
        self.assertEqual(eval(repr(p)), p)
        self.assertEqual(str(Interval(-1, 1)), '<-1;1>')

    def test_constructor(self):
        self.assertRaises(ValueError, lambda: Interval('#2;3>'))
        self.assertRaises(ValueError, lambda: Interval('(2;3!'))
        self.assertRaises(ValueError, lambda: Interval('<-inf;3)'))
        self.assertEqual(Interval(1, 2, True, False), Interval('<1;2)'))
        self.assertEqual(Interval(1, 2, True, False), '<1;2)')

        r = Interval(1, 2, True, False)
        self.assertEqual(r, Interval(r))

    def test_extend(self):
        i = Interval('(-1;1)')

        self.assertEqual(i.extend_to_point(-1), '<-1;1)')
        self.assertEqual(i.extend_to_point(1), '(-1;1>')
        self.assertEqual(i.extend_to_point(float('inf')), '(-1;inf)')
        self.assertEqual(i.extend_to_point(float('-inf')), '(-inf;1)')

    def test_contains(self):
        self.assertFalse(-1 in Interval('<-10;-1)'))
        self.assertTrue(-10 in Interval('<-10;-1)'))
        self.assertFalse(-10 in Interval('(-10;-1>'))
        self.assertTrue(-1 in Interval('(-10;-1>'))
        self.assertTrue(-5 in Interval('(-10;-1>'))
        self.assertFalse(-20 in Interval('(-10;-1>'))
        self.assertFalse(1 in Interval('(-10;-1>'))
        self.assertFalse('<-10;-1>' in Interval('(-10;-1)'))
        self.assertFalse('<-10;-1)' in Interval('(-10;-1>'))

        self.assertTrue(Interval('<-5;5>') in Interval('<-10;10>'))
        self.assertTrue('(-1;6)' in Interval(-10.0, 10.0, True, False))
        self.assertTrue('<0.5;1.5>' in Interval('<0;2>'))
