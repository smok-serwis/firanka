import logging
import typing as tp
from firanka.domain import *
from unittest import TestCase
logger = logging.getLogger(__name__)


class TestDomain(TestCase):
    def test_single_interval_domain(self):
        sid = SingleIntervalDomain(-1, Closing.OPEN, 1, Closing.CLOSED)
        self.assertEqual(str(sid), '(-1;1>')
        self.assertNotIn(-1, sid)
        self.assertIn(0, sid)
        self.assertIn(1, sid)
        sid2 = SingleIntervalDomain(0.5, Closing.OPEN, 2, Closing.CLOSED)
        self.assertEqual(sid + sid2, SingleIntervalDomain(-1, Closing.OPEN, 2, Closing.CLOSED))
        self.assertEqual(str(sid * sid2), '<0.5;1>')

        sid3 = SingleIntervalDomain(5, Closing.CLOSED, 10, Closing.OPEN)
        self.assertIsInstance(sid * sid3, EmptyDomain)
        self.assertIsInstance(sid + sid3, PatchworkDomain)
