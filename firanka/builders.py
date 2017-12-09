# coding=UTF-8
from __future__ import print_function, absolute_import, division

import copy

from sortedcontainers import SortedList

from .series import DiscreteSeries

"""
Update knowledge of current discrete series
"""

__all__ = [
    'DiscreteSeriesBuilder',
]


class DiscreteSeriesBuilder(object):
    def __init__(self, series=None):

        if series is None:
            series = DiscreteSeries([])

        if not isinstance(series, DiscreteSeries):
            raise TypeError('discrete knowledge builder supports only discrete series')

        self.new_data = {}
        self.domain = series.domain
        self.series = series

    def put(self, index, value):
        self.domain = self.domain.extend_to_point(index)
        self.new_data[index] = value

    def as_series(self):
        """
        Update
        :return: a new DiscreteSeries instance
        """

        new_data = SortedList()
        cp_new_data = copy.copy(self.new_data)

        # Update - series.data is sorted, so no worries :)
        for k, v in self.series.data:
            if k in cp_new_data:
                v = cp_new_data.pop(k)
            new_data.append((k, v))

        # Add those that remained
        for k, v in cp_new_data.items():
            new_data.add((k, v))

        return DiscreteSeries(new_data, self.domain)
