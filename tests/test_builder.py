# coding=UTF-8
from __future__ import print_function, absolute_import, division

import unittest

from firanka.builders import DiscreteSeriesBuilder
from firanka.series import DiscreteSeries


class TestBuilder(unittest.TestCase):
    def test_t1(self):
        ser = DiscreteSeries([(0, 1), (1, 2)])

        kb = DiscreteSeriesBuilder(ser)

        kb.put(3, 4)
        kb.put(-1, 5)
        kb.put(0, 2)
        kb.put(-1, 6)

        s2 = kb.as_series()

        self.assertTrue(s2.domain, '<-1;3>')
        self.assertEqual(s2.data, [(-1, 6), (0, 2), (1, 2), (3, 4)])

    def test_exnihilo(self):
        kb = DiscreteSeriesBuilder()

        kb.put(0, 0)
        kb.put(1, 1)

        s = kb.as_series()

        self.assertEqual(s[0], 0)
        self.assertEqual(s[1], 1)
        self.assertEqual(s.domain, '<0;1>')
