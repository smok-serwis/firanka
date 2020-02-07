import functools
import logging

from sortedcontainers import SortedSet, SortedList

logger = logging.getLogger(__name__)

from .base import Series, DiscreteSeries
from ..intervals import REAL_SET


class SeriesBundle(Series):
    """
    Bundles a bunch of series together, returning a list from their outputs
    """

    def __init__(self, *series):
        domain = functools.reduce(lambda x, y: x.intersection(y),
                                  (p.domain for p in series),
                                  REAL_SET)

        super().__init__(domain)

        self.series = series

    def _get_for(self, item):
        return [s._get_for(item) for s in self.series]


class DiscreteSeriesBundle(SeriesBundle):
    def __init__(self, *series):
        """
        :raise TypeError: if not all series are discrete
        """
        super().__init__(*series)

        if any((not isinstance(s, DiscreteSeries)) for s in series):
            raise TypeError('All series must be discrete')

    def compose(self):
        """
        Return a DiscreteSet from multiple bunded series.
        This does not lose accuracy.

        If you use any fancy classes based from DiscreteSeries,
        their functionality WILL BE LOST.
        """
        keys = SortedSet()

        for s in self.series:
            for k, v in s.data:
                keys.add(k)

        data = SortedList()
        for k in keys:
            v = self._get_for(k)
            if len(data) > 0 and data[-1][1] == v:
                continue
            else:
                data.add((k, v))

        return DiscreteSeries([(k, self._get_for(k)) for k in keys], self.domain)
