# coding=UTF-8
from __future__ import print_function, absolute_import, division

import functools
import logging

logger = logging.getLogger(__name__)

from .base import Series
from ..intervals import REAL_SET


class SeriesBundle(Series):
    """
    Bundles a bunch of series together, returning a list from their outputs
    """

    def __init__(self, *series):
        domain = functools.reduce(lambda x, y: x.intersection(y),
                                  (p.domain for p in series),
                                  REAL_SET)

        super(SeriesBundle, self).__init__(domain)

        self.series = series

    def _get_for(self, item):
        return [s._get_for(item) for s in self.series]
