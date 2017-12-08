# coding=UTF-8
from __future__ import print_function, absolute_import, division
import six
import logging

logger = logging.getLogger(__name__)

from .exceptions import OutOfRangeError, EmptyDomainError



class DataSeries(object):
    """
    Finite mapping from x: REAL => object
    """

    def __init__(self, data, domain_end=None):
        self.data = data

        if domain_end is None:
            try:
                self.domain_end = data[-1][0]
            except IndexError:
                self.domain_end = None
        else:
            self.domain_end = domain_end

    @property
    def domain(self):
        try:
            start = self.data[0][0]
            stop = self.domain_end
            assert start <= stop
            return start, stop
        except IndexError:
            return EmptyDomainError

    def __contains__(self, index):
        start, stop = self.domain
        return start <= index <= stop

    def length(self):
        """
        Return timespan
        :return: float
        """
        try:
            start, stop = self.domain

            return stop-start
        except IndexError:
            return 0.0
        except TypeError:
            return 0.0 # domain_end is None

    def __getitem__(self, index):
        if index not in self:
            raise OutOfRangeError('index not within domain', index)

        for k, v in self.data:
            if k <= index:
                return v
