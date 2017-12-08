# coding=UTF-8
from __future__ import print_function, absolute_import, division
import six
import logging

logger = logging.getLogger(__name__)


class DataSeries(object):
    """
    Finite mapping from x: REAL => object
    """

    def __init__(self, data=None):
        self.data = data or []

    def length(self):
        """
        Return timespan
        :return: float
        """
        try:
            return self.data[-1] - self.data[0]
        except IndexError:
            return 0.0


