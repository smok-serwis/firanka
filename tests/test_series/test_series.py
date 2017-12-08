# coding=UTF-8
from __future__ import print_function, absolute_import, division
import six
import unittest
from firanka.series import DiscreteSeries, FunctionBasedSeries, Range


class TestDiscreteSeries(unittest.TestCase):


    def test_base(self):

        s = DiscreteSeries([[0,0], [1,1], [2,2]])

        self.assertEqual(s[0], 0)
        self.assertEqual(s[0.5], 0)
        self.assertEqual(s[1], 1)

        self.assertRaises(ValueError, lambda: s[-1])
        self.assertRaises(ValueError, lambda: s[2.5])


        s = DiscreteSeries([[0,0], [1,1], [2,2]], domain=Range(0,3,True,True))
        self.assertEqual(s[0], 0)
        self.assertEqual(s[0.5], 0)
        self.assertEqual(s[1], 1)

        self.assertRaises(ValueError, lambda: s[-1])
        self.assertEqual(s[2.5], 2)


    def test_slice(self):
        series = DiscreteSeries([[0, 0], [1, 1], [2, 2]])

        sp = series[0.5:1.5]

        self.assertEqual(sp[0.5], 0)
        self.assertEqual(sp[1.5], 1)
        self.assertRaises(ValueError, lambda: sp[0])
        self.assertRaises(ValueError, lambda: sp[2])
        self.assertEqual(sp.domain.start, 0.5)
        self.assertEqual(sp.domain.stop, 1.5)

    def test_eval(self):
        sa = DiscreteSeries([[0, 0], [1, 1], [2, 2]])
        sb = DiscreteSeries([[0, 1], [1, 2], [2, 3]])

        sc = sa.apply(sb, lambda a, b: a+b)
        sd = sc.compute()
        self.assertEqual(sc.eval_points([0,1,2]), [1,3,5])
        self.assertEqual(sd.eval_points([0,1,2]), sd.eval_points([0,1,2]))

        self.assertEqual(sd.data, [(0,1),(1,3),(2,5)])

    def test_eval2(self):
        sa = DiscreteSeries([[0, 0], [1, 1], [2, 2]])
        sb = FunctionBasedSeries(lambda x: x, '<0;2)')

        sc = sa.apply(sb, lambda a, b: a+b)
        sd = sc.compute()
        self.assertEqual(sc.eval_points([0,1,2]), [0,2,4])
        self.assertEqual(sd.eval_points([0,1,2]), sd.eval_points([0,1,2]))

        self.assertEqual(sd.data, [(0,0),(1,2),(2,4)])


class TestFunctionBasedSeries(unittest.TestCase):
    def test_slice(self):
        series = FunctionBasedSeries(lambda x: x, '<0;2>')

        sp = series[0.5:1.5]

        self.assertEqual(sp[0.5], 0.5)
        self.assertEqual(sp[1.5], 1.5)
        self.assertRaises(ValueError, lambda: sp[0])
        self.assertRaises(ValueError, lambda: sp[2])
        self.assertEqual(sp.domain.start, 0.5)
        self.assertEqual(sp.domain.stop, 1.5)
