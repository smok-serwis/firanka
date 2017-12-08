# coding=UTF-8
from __future__ import print_function, absolute_import, division
import six
import logging
import re
from satella.coding import for_argument

logger = logging.getLogger(__name__)


class Range(object):
    """
    Range of real numbers
    """
    def __init__(self, *args):
        if len(args) == 1:
            rs, = args
            assert rs.startswith('<') or rs.startswith('(')
            assert rs.endswith('>') or rs.endswith(')')

            lend_inclusive = rs[0] == '<'
            rend_inclusive = rs[-1] == '>'

            rs = rs[1:-1]
            start, stop = map(float, rs.split(';'))
        elif isinstance(args[0], Range):
            start = args[0].range
            stop = args[0].stop
            lend_inclusive = args[0].lend_inclusive
            rend_inclusive = args[0].rend_inclusive
        else:
            start, stop, lend_inclusive, rend_inclusive = args

        self.start = start
        self.stop = stop
        self.lend_inclusive = lend_inclusive
        self.rend_inclusive = rend_inclusive

    def __contains__(self, x):
        if x == self.start:
            return self.lend_inclusive

        if x == self.stop:
            return self.rend_inclusive

        return self.start < x < self.stop

    def is_empty(self):
        return (self.start == self.stop) and (not self.lend_inclusive) and (
        not self.rend_inclusive)

    def __len__(self):
        return self.stop - self.start

    def __repr__(self):
        return str(self)
        return 'Range(%s, %s, %s, %s)' % (repr(self.start), repr(self.stop), repr(self.lend_inclusive), repr(self.rend_inclusive))

    def __bool__(self):
        """True if not empty"""
        return not self.is_empty()

    def __str__(self):
        return '%s%s;%s%s' % (
            '<' if self.lend_inclusive else '(',
            self.start,
            self.stop,
            '>' if self.rend_inclusive else ')',
        )

    def intersection(self, y):
        if not isinstance(y, Range): y = Range(y)

        x = self

        # Check for intersection being impossible
        if (x.stop < y.start) or (x.start > y.stop) or \
            (x.stop == y.start and not x.rend_inclusive and not y.lend_inclusive) or \
            (x.start == x.stop and not x.lend_inclusive and not y.rend_inclusive):
            return EMPTY_RANGE

        # Check for range extension
        if (x.start == y.stop) and (x.lend_inclusive or y.lend_inclusive):
            return Range(y.start, x.stop, y.lend_inclusive, x.rend_inclusive)

        if (x.start == y.stop) and (x.lend_inclusive or y.lend_inclusive):
            return Range(y.start, x.stop, y.lend_inclusive, x.rend_inclusive)


        if x.start == y.start:
            start = x.start
            lend_inclusive = x.lend_inclusive or y.lend_inclusive
        else:
            p = x if x.start > y.start else y
            start = p.start
            lend_inclusive = p.lend_inclusive

        if x.stop == y.stop:
            stop = x.stop
            rend_inclusive = x.rend_inclusive or y.rend_inclusive
        else:
            p = x if x.stop < y.stop else y
            stop = p.stop
            rend_inclusive = p.rend_inclusive

        return Range(start, stop, lend_inclusive, rend_inclusive)

    def __eq__(self, other):
        if not isinstance(other, Range): other = Range(other)
        return self.start == other.start and self.stop == other.stop and self.lend_inclusive == other.lend_inclusive and self.rend_inclusive == other.rend_inclusive

    def __hash__(self):
        return hash(self.start) ^ hash(self.stop)


EMPTY_RANGE = Range(0, 0, False, False)