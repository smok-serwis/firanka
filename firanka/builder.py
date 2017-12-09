# coding=UTF-8
from __future__ import print_function, absolute_import, division
import six
import logging
import copy
from .series import Series, DiscreteSeries
from .ranges import Range

"""
Update knowledge of current discrete series
"""

__all__ = [
    'DiscreteKnowledgeBuilder',
]

class DiscreteKnowledgeBuilder(object):
    def __init__(self, series=None):

        if series is None:
            series = DiscreteSeries([], '(0;0)')

        if not isinstance(series, DiscreteSeries):
            raise TypeError('discrete knowledge builder supports only discrete series')

        self.new_data = {}
        self.domain = series.domain
        self.series = series

    def put(self, index, value):

        if index not in self.domain:
            if index <= self.domain.start:
                self.domain = Range(index, self.domain.stop, True, self.domain.right_inc)
            if index >= self.domain.stop:
                self.domain = Range(self.domain.start, index, self.domain.left_inc, True)

        self.new_data[index] = value

    def as_series(self):
        """
        Update
        :return: a new DiscreteSeries instance
        """

        new_data = []

        cp_new_data = copy.copy(self.new_data)

        # Update
        for k, v in self.series.data:
            if k in cp_new_data:
                v = cp_new_data.pop(k)
            new_data.append((k,v))

        # Add those that remained
        for k,v in cp_new_data.items():
            new_data.append((k,v))

        return DiscreteSeries(new_data, self.domain)
