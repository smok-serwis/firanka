# coding=UTF-8
from __future__ import print_function, absolute_import, division
import six
import unittest

from firanka.builder import DiscreteKnowledgeBuilder
from firanka.series import DiscreteSeries


class TestBuilder(unittest.TestCase):
    def test_t1(self):

        ser = DiscreteSeries([(0,1), (1,2)])

        kb = DiscreteKnowledgeBuilder(ser)

        kb.put(3, 4)
        kb.put(-1, 5)
        kb.put(-1, 6)

        s2 = kb.update_series()

        self.assertTrue(s2.domain, '<-1;3>')
        self.assertEqual(s2.data,[(-1,6), (0,1), (1,2), (3,4)])
