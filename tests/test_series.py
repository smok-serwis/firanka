# coding=UTF-8
from __future__ import print_function, absolute_import, division

import math
import unittest

from firanka.exceptions import NotInDomainError, DomainError
from firanka.intervals import Interval
from firanka.series import DiscreteSeries, FunctionSeries, ModuloSeries, \
    LinearInterpolationSeries, Series

NOOP = lambda x: x

HUGE_IDENTITY = FunctionSeries(NOOP, '(-inf;inf)')


class TestBase(unittest.TestCase):
    def test_abstract(self):
        self.assertRaises(NotImplementedError, lambda: Series('<-1;1>')[0])


class TestDiscreteSeries(unittest.TestCase):
    def test_redundancy_skip(self):
        a = DiscreteSeries([(0, 0), (1, 0), (2, 0)], '<0;5>')
        b = DiscreteSeries([(0, 0), (1, 0)], '<0;5>')

        a.join(b, lambda i, x, y: x + y)

    def test_uncov(self):
        self.assertRaises(DomainError,
                          lambda: DiscreteSeries([[0, 0], [1, 1], [2, 2]],
                                                 '<-5;2>'))

    def test_base(self):
        s = DiscreteSeries([[0, 0], [1, 1], [2, 2]])

        self.assertEqual(s[0], 0)
        self.assertEqual(s[0.5], 0)
        self.assertEqual(s[1], 1)

        self.assertRaises(NotInDomainError, lambda: s[-1])
        self.assertRaises(NotInDomainError, lambda: s[2.5])

        s = DiscreteSeries([[0, 0], [1, 1], [2, 2]],
                           domain=Interval(0, 3, True, True))
        self.assertEqual(s[0], 0)
        self.assertEqual(s[0.5], 0)
        self.assertEqual(s[1], 1)

        self.assertRaises(NotInDomainError, lambda: s[-1])
        self.assertEqual(s[2.5], 2)

    def test_translation(self):
        s = DiscreteSeries([[0, 0], [1, 1], [2, 2]]).translate(3)

        self.assertEqual(s[3], 0)
        self.assertEqual(s[3.5], 0)
        self.assertEqual(s[4], 1)

    def test_slice_outdomain(self):
        series = DiscreteSeries([[0, 0], [1, 1], [2, 2]])

        self.assertRaises(NotInDomainError, lambda: series[-1:2])

    def test_translate(self):
        sp = DiscreteSeries([[0, 0], [1, 1], [2, 2]]).translate(1)
        self.assertEqual(sp[1.5], 0)
        self.assertEqual(sp[2.5], 1)

    def test_slice(self):
        series = DiscreteSeries([[0, 0], [1, 1], [2, 2]])

        sp = series[0.5:1.5]

        self.assertEqual(sp[0.5], 0)
        self.assertEqual(sp[1.5], 1)
        self.assertRaises(NotInDomainError, lambda: sp[0])
        self.assertRaises(NotInDomainError, lambda: sp[2])
        self.assertEqual(sp.domain.start, 0.5)
        self.assertEqual(sp.domain.stop, 1.5)

    def test_eval(self):
        sa = DiscreteSeries([[0, 0], [1, 1], [2, 2]])
        sb = DiscreteSeries([[0, 1], [1, 2], [2, 3]])

        sc = sa.join_discrete(sb, lambda i, a, b: a + b)
        self.assertIsInstance(sc, DiscreteSeries)
        self.assertEqual(sc.eval_points([0, 1, 2]), [1, 3, 5])
        self.assertEqual(sc.data, [(0, 1), (1, 3), (2, 5)])

    def test_eval2(self):
        sa = DiscreteSeries([[0, 0], [1, 1], [2, 2]])
        sb = FunctionSeries(NOOP, '<0;2>')

        sc = sa.join_discrete(sb, lambda i, a, b: a + b)
        self.assertEqual(sc.eval_points([0, 1, 2]), [0, 2, 4])

        self.assertIsInstance(sc, DiscreteSeries)
        self.assertEqual(sc.data, [(0, 0), (1, 2), (2, 4)])

    def test_eval2i(self):
        sa = DiscreteSeries([[0, 0], [1, 1], [2, 2]])
        sc = sa.join_discrete(HUGE_IDENTITY, lambda i, a, b: i)
        self.assertEqual(sc.eval_points([0, 1, 2]), [0, 1, 2])
        self.assertIsInstance(sc, DiscreteSeries)
        self.assertEqual(sc.data, [(0, 0), (1, 1), (2, 2)])

    def test_apply(self):
        sb = DiscreteSeries([[0, 0], [1, 1], [2, 2]]).apply(
            lambda k, v: k)
        self.assertEquals(sb.data, [(0, 0), (1, 1), (2, 2)])

    def test_eval3(self):
        sa = FunctionSeries(lambda x: x ** 2, '<-10;10)')
        sb = FunctionSeries(NOOP, '<0;2)')

        sc = sa.join(sb, lambda i, a, b: a * b)

        PTS = [0, 1, 1.9]
        EPTS = [x * x ** 2 for x in PTS]

        self.assertEqual(sc.eval_points(PTS), EPTS)
        self.assertTrue(Interval('<0;2)') in sc.domain)

    def test_discretize(self):
        # note the invalid data for covering this domain
        self.assertRaises(DomainError, lambda: FunctionSeries(lambda x: x ** 2,
                                                             '<-10;10)').discretize(
            [0, 1, 2, 3, 4, 5], '(-1;6)'))

        self.assertRaises(NotInDomainError, lambda: FunctionSeries(lambda x: x ** 2,
                                                                   '<-10;10)').discretize(
            [-100, 0, 1, 2, 3, 4, 5], '(-1;6)'))

        PTS = [-1, 0, 1, 2, 3, 4, 5]
        sa = FunctionSeries(lambda x: x ** 2, '<-10;10)').discretize(PTS,
                                                                     '(-1;6)')

        self.assertIsInstance(sa, DiscreteSeries)
        self.assertEqual(sa.data, [(i, i ** 2) for i in PTS])

        sa = FunctionSeries(lambda x: x ** 2, '<-10;10)').discretize(PTS)
        self.assertIsInstance(sa, DiscreteSeries)
        self.assertEqual(sa.data, [(i, i ** 2) for i in PTS])

        empty = FunctionSeries(lambda x: x ** 2, '<-10;10)').discretize([])
        self.assertTrue(empty.domain.is_empty())


class TestFunctionSeries(unittest.TestCase):
    def test_slice(self):
        series = FunctionSeries(NOOP, '<0;2>')
        sp = series[0.5:1.5]

        self.assertEqual(sp[0.5], 0.5)
        self.assertEqual(sp[1.5], 1.5)
        self.assertRaises(NotInDomainError, lambda: sp[0])
        self.assertRaises(NotInDomainError, lambda: sp[2])
        self.assertEqual(sp.domain.start, 0.5)
        self.assertEqual(sp.domain.stop, 1.5)

    def test_apply(self):
        PTS = [-1, -2, -3, 1, 2, 3]
        series = FunctionSeries(NOOP, '<-5;5>').apply(lambda k, x: k)

        self.assertEqual(series.eval_points(PTS), [x for x in PTS])

    def test_apply_wild(self):
        def dzika(k, x, a=5, *args, **kwargs):
            return k

        PTS = [-1, -2, -3, 1, 2, 3]
        series = FunctionSeries(NOOP, '<-5;5>').apply(dzika)

        self.assertEqual(series.eval_points(PTS), [x for x in PTS])

    def test_domain_sensitivity(self):
        logs = FunctionSeries(math.log, '(0;5>')
        dirs = DiscreteSeries([(0, 1), (1, 2), (3, 4)], '<0;5>')

        self.assertRaises(ValueError,
                          lambda: dirs.join_discrete(logs, lambda i, x, y: x + y))


class TestModuloSeries(unittest.TestCase):
    def test_exceptions(self):
        self.assertRaises(ValueError, lambda: ModuloSeries(
            FunctionSeries(NOOP, '(-inf; 0>')))
        self.assertRaises(ValueError, lambda: ModuloSeries(
            FunctionSeries(NOOP, '(-inf; inf)')))
        self.assertRaises(ValueError,
                          lambda: ModuloSeries(FunctionSeries(NOOP, '<0; 0>')))

    def test_base(self):
        series = ModuloSeries(
            DiscreteSeries([(0, 1), (1, 2), (2, 3)], '<0;3)'))

        self.assertEquals(series[3], 1)
        self.assertEquals(series[4], 2)
        self.assertEquals(series[5], 3)
        self.assertEquals(series[-1], 3)

    def test_advanced(self):
        series = ModuloSeries(DiscreteSeries([(-1, 1), (0, 2), (1, 3)], '<-1;2)'))

        self.assertEqual(series.period, 3.0)

        self.assertEqual(series.eval_points([-1, 0, 1]), [1, 2, 3])

        self.assertEqual(series.eval_points([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]),
                         [3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1])

    def test_comp_discrete(self):
        ser1 = ModuloSeries(FunctionSeries(lambda x: x ** 2, '<0;3)'))
        ser2 = FunctionSeries(NOOP, '<0;3)')

        ser3 = ser1.join(ser2, lambda i, x, y: x * y)


class TestLinearInterpolation(unittest.TestCase):
    def test_lin(self):
        series = LinearInterpolationSeries(
            DiscreteSeries([(0, 1), (1, 2), (2, 3)], '<0;3)'))

        self.assertEqual(series[0], 1)
        self.assertEqual(series[0.5], 1.5)
        self.assertEqual(series[1], 2)
        self.assertEqual(series[2.3], 3)

    def test_conf(self):
        self.assertRaises(TypeError, lambda: LinearInterpolationSeries(
            FunctionSeries(NOOP, '<0;3)')))
