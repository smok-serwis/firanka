# coding=UTF-8
from __future__ import print_function, absolute_import, division

from firanka.series import FunctionSeries

NOOP = lambda x: x
HUGE_IDENTITY = FunctionSeries(NOOP, '(-inf;inf)')
