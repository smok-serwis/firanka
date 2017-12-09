# coding=UTF-8
from __future__ import print_function, absolute_import, division

import unittest

from firanka.series import DiscreteSeries
from firanka.timeproviders import TimeProvidedSeries, BijectionMapping


class TestTimeproviders(unittest.TestCase):
    def test_base(self):
        map = BijectionMapping(
            lambda hhmm: hhmm[0] * 60 + hhmm[1],
            lambda t: (t // 60, t % 60)
        )

        ser = DiscreteSeries([(0, 17), (60, 20), (120, 18)])
        ts = TimeProvidedSeries(ser, map)

        self.assertEqual(ts[(2, 0)], 18)
