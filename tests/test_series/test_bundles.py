import unittest

from firanka.series import DiscreteSeries, FunctionSeries, SeriesBundle, DiscreteSeriesBundle
from .common import NOOP


class TestBundles(unittest.TestCase):
    def test_base(self):
        s = SeriesBundle(
            DiscreteSeries([(0, 1), (1, 1), (2, 1)], '<0;inf)'),
            DiscreteSeries([(0, 2), (1, 2), (2, 2), (3, 4)], '<0;inf)'),
        )

        self.assertEqual(s[0], [1, 2])
        self.assertEqual(s[3], [1, 4])

    def test_disc(self):
        self.assertRaises(TypeError, lambda: DiscreteSeriesBundle(
            DiscreteSeries([(0, 1), (1, 1), (2, 1)], '<0;inf)'),
            FunctionSeries(NOOP, '<0;inf)'),
        ))

        s = DiscreteSeriesBundle(
            DiscreteSeries([(0, 1), (1, 1), (2, 1)], '<0;inf)'),
            DiscreteSeries([(0, 2), (1.5, 2), (2, 2), (3, 4)], '<0;inf)'),
        )

        self.assertEqual(s[0], [1, 2])
        self.assertEqual(s[3], [1, 4])

    def test_compose(self):
        s = DiscreteSeriesBundle(
            DiscreteSeries([(0, 1), (1, 1), (2.5, 1)], '<0;inf)'),
            DiscreteSeries([(0, 2), (1.5, 2), (2, 2), (3, 4)], '<0;inf)'),
        )

        p = s.compose()

        self.assertEqual(p.data,
                         [(0, [1, 2]), (1, [1, 2]), (1.5, [1, 2]), (2, [1, 2]), (2.5, [1, 2]),
                          (3, [1, 4])])
