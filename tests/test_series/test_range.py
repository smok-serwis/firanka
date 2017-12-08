# coding=UTF-8
from __future__ import print_function, absolute_import, division
import unittest
from firanka.series import Range


class TestRange(unittest.TestCase):
    def do_intersect(self, a, b, val):
        if type(val) == bool:
            if bool(Range(a).intersection(b)) != val:
                self.fail('%s ^ %s != %s' % (Range(a), Range(b), val))
            if bool(Range(b).intersection(a)) != val:
                self.fail('%s ^ %s != %s' % (Range(b), Range(a), val))
        else:
            self.assertEqual(Range(a).intersection(b), Range(val))
            self.assertEqual(Range(b).intersection(a), Range(val))

    def test_isempty(self):
        def tf(r, p):
            s = Range(r)
            self.assertEqual(s, r)
            self.assertEqual(s.is_empty(), not p)

        tf(Range(-1,-1,False,False), False)
        tf(Range(-1,-1,False,True), True)
        self.assertEqual(Range(0,0,False,False), Range(2,2,False,False))

    def test_intersection(self):
        self.do_intersect(Range(-10, -1, True, True), '<2;3>', False)
        self.do_intersect(Range(-10, -1, True, False), '(-1;3>', False)
        self.do_intersect('<-10;-1)', '<-1;1>', False)
        self.do_intersect(Range(-10, -1, True, False), '(-1;3>', False)
        self.do_intersect('<-10;2)', '<1;5>', '<1;2)')

    def test_str_and_repr_and_bool(self):
        p = Range(-1,1,True,True)
        self.assertEqual(eval(repr(p)),p)
        self.assertEqual(str(Range(-1, 1, True, True)), '<-1;1>')

    def test_constructor(self):
        self.assertRaises(ValueError, lambda: Range('#2;3>'))
        self.assertRaises(ValueError, lambda: Range('(2;3!'))
        self.assertRaises(ValueError, lambda: Range('<-inf;3)'))
        self.assertEqual(Range(1,2,True,False), Range('<1;2)'))

    def test_contains(self):
        self.assertFalse(-1 in Range('<-10;-1)'))
        self.assertTrue(-10 in Range('<-10;-1)'))
        self.assertFalse(-10 in Range('(-10;-1>'))
        self.assertTrue(-1 in Range('(-10;-1>'))
        self.assertTrue(-5 in Range('(-10;-1>'))
        self.assertFalse(-20 in Range('(-10;-1>'))
        self.assertFalse(1 in Range('(-10;-1>'))

        self.assertTrue(Range('<-5;5>') in Range('<-10;10>'))