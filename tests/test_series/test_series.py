# coding=UTF-8
from __future__ import print_function, absolute_import, division
import six
import unittest
from firanka.series import DataSeries


class TestSeries(unittest.TestCase):
    def test_ds(self):

        ds = DataSeries()
        self.assertAlmostEqual(ds.length(), 0.0)
