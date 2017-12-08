# coding=UTF-8
from __future__ import print_function, absolute_import, division
import six
import unittest
from firanka.series import DataSeries


class TestSeries(unittest.TestCase):
    def test_ds(self):

        ds = DataSeries()
        self.assertAlmostEqual(ds.length(), 0.0)

        ds = DataSeries([[0,1], [10,2]])
        self.assertAlmostEqual(ds.length(), 10.0)
