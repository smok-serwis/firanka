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
    def __init__(self, series):

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

    def update_series(self):
        """:return: a new DiscreteSeries instance"""

        new_data = copy.copy(self.series.data)
        for k,v in self.new_data.items():
            new_data.add((k,v))

        return DiscreteSeries(new_data, self.domain)
