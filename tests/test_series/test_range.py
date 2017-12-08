# coding=UTF-8
from __future__ import print_function, absolute_import, division
import six
import unittest
from firanka.series.range import Range

class TestRange(unittest.TestCase):
    def test_intersection(self):

        self.assertFalse(Range(-10, -1, True, True).intersection('<2;3>'))
        self.assertFalse(Range(-10, -1, True, False).intersection('(-1;3>'))
        self.assertFalse(Range('<-10;-1)').intersection('<-1;1>'))


    def test_str(self):
        self.assertEqual(str(Range(-1, 1, True, True)), '<-1;1>')