
# coding=UTF-8
from __future__ import print_function, absolute_import, division
import six
import functools
import itertools

from .range import Range, REAL_SET, EMPTY_RANGE
from .exceptions import NotInDomainError


class Series(object):

    def __init__(self, domain):
        if not isinstance(domain, Range):
            domain = Range(domain)
        self.domain = domain

    def __getitem__(self, item):
        """
        Return a value for given index, or a subslice of this series
        :param item: a float, or a slice
        :return: Series instance or a value
        :raises NotInDomainError: index not in domain
        """
        if isinstance(item, slice):
            item = Range(item)
            if item not in self.domain:
                raise NotInDomainError('slicing beyond series domain')

            newdom = self.domain.intersection(item)
            return SlicedSeries(self, newdom)
        else:
            if item not in self.domain:
                raise NotInDomainError('item not in domain')

            return self._get_for(item)

    def _get_for(self, item):
        raise NotImplementedError

    def eval_points(self, points):
        """
        Return values for given points. A mass [] one could say
        :param points: iterable of indices
        :return: a list of values
        """
        return [self[p] for p in points]

    def apply(self, fun):
        """
        Return this series with a function applied to each value
        :param fun: callable/1 => 1
        :return: Series instance
        """
        return AppliedSeries(self, fun)

    def discretize(self, points, domain=None):
        """
        Return this as a DiscreteSeries, sampled at points
        :return: a DiscreteSeries instance
        """
        if len(points) == 0:
            return DiscreteSeries([])

        if domain is None:
            domain = Range(points[0], points[-1], True, True)

        if domain not in self.domain:
            raise NotInDomainError('points not inside this series!')

        data = [(i, self[i]) for i in points]
        return DiscreteSeries(data, domain)

    def join(self, series, fun):
        """
        Return a new series with values of fun(v1, v2)

        :param series: series to join against
        :param fun: callable/2 => value
        :return: new Series instance
        """
        return JoinedSeries(self, series, fun)

    def translate(self, x):
        """
        Translate the series by some distance
        :param x: a float
        :return: new Series instance
        """
        return TranslatedSeries(self, x)


class AppliedSeries(Series):
    def __init__(self, series, applyfun):
        super(AppliedSeries, self).__init__(series.domain)
        self.fun = applyfun
        self.series = series

    def _get_for(self, item):
        return self.fun(self._get_for(item))


class TranslatedSeries(Series):
    def __init__(self, series, x):
        super(TranslatedSeries, self).__init__(self.domain.translate(x))
        self.series = series
        self.x = x

    def _get_for(self, item):
        return self.series._get_for(item+self.x)


class SlicedSeries(Series):
    def __init__(self, parent, domain):
        super(SlicedSeries, self).__init__(domain)
        self.parent = parent

    def _get_for(self, item):
        return self.parent._get_for(item)


class DiscreteSeries(Series):

    def __init__(self, data, domain=None):
        if len(data) == 0:
            domain = EMPTY_RANGE
        elif domain is None:
            domain = Range(data[0][0], data[-1][0], True, True)

        self.data = data
        super(DiscreteSeries, self).__init__(domain)

    def apply(self, fun):
        return DiscreteSeries([(k, fun(v)) for k, v in self.data], self.domain)

    def _get_for(self, item):
        for k, v in reversed(self.data):
            if k <= item:
                return v

        raise RuntimeError('should never happen')

    def translate(self, x):
        return DiscreteSeries([(k+x, v) for k, v in self.data], self.domain.translate(x))

    def join_discrete(self, series, fun):
        new_domain = self.domain.intersection(series.domain)

        if isinstance(series, DiscreteSeries):
            a = self.data[::-1]
            b = series.data[::-1]

            ptr = self.domain.start
            c = [(ptr, fun(self._get_for(ptr), series._get_for(ptr)))]

            def appendif(lst, ptr, v):
                if len(lst) > 0:
                    if lst[-1][0] >= ptr:
                        return
                lst.append((ptr, v))

            while len(a) > 0 or len(b) > 0:
                if len(a) > 0 and len(b) > 0:
                    if a[-1] < b[-1]:
                        ptr, v1 = a.pop()
                        v2 = series._get_for(ptr)
                    elif a[-1] > b[-1]:
                        ptr, v1 = b.pop()
                        v2 = self._get_for(ptr)
                    else:
                        ptr, v1 = a.pop()
                        _, v2 = b.pop()

                    assert ptr >= c[-1][0]

                    appendif(c, ptr, fun(v1, v2))

                else:
                    if len(a) > 0:
                        rest = a
                        static_v = series._get_for(ptr)
                        op = lambda me, const: fun(me, const)
                    else:
                        rest = b
                        static_v = self._get_for(ptr)
                        op = lambda me, const: fun(const, me)

                    for ptr, v in rest:
                        appendif(c, ptr, op(v, static_v))

                    break
        else:
            if new_domain.start > self.data[0][0]:
                c = [(new_domain.start, fun(self._get_for(new_domain.start), series._get_for(new_domain.start)))]
            else:
                c = []

            for k, v in ((k, v) for k, v in self.data if new_domain.start <= k <= new_domain.stop):
                newv = fun(v, series._get_for(k))

                if len(c) > 0:
                    if c[-1][1] == newv:
                        continue

                c.append((k, newv))

            if c[-1][0] != new_domain.stop:
                c.append((new_domain.stop, fun(self._get_for(new_domain.stop), series._get_for(new_domain.stop))))

        return DiscreteSeries(c, new_domain)

    def compute(self):
        """Simplify self"""
        nd = [self.data[0]]
        for i in six.moves.range(1, len(self.data)):
             if self.data[i][1] != nd[-1][1]:
                 nd.append(self.data[i])
        return DiscreteSeries(nd, self.domain)


class FunctionBasedSeries(Series):
    """
    Series with values defined by a function
    """
    def __init__(self, fun, domain):
        super(FunctionBasedSeries, self).__init__(domain)
        self.fun = fun

    def _get_for(self, item):
        return self.fun(item)


class JoinedSeries(Series):
    """
    Series stemming from performing an operation on two series
    """
    def __init__(self, ser1, ser2, op):
        domain = ser1.domain.intersection(ser2.domain)
        super(JoinedSeries, self).__init__(domain)
        self.ser1 = ser1
        self.ser2 = ser2
        self.op = op

    def _get_for(self, item):
        return self.op(self.ser1._get_for(item), self.ser2._get_for(item))


class ModuloSeries(Series):

    def __init__(self, series):
        super(ModuloSeries, self).__init__(REAL_SET)

        self.series = series
        self.period = self.series.domain.length()

        if self.period == 0:
            raise ValueError('Modulo series cannot have a period of 0')

    def _get_for(self, item):
        if item < 0:
            item = -(item // self.period) * self.period + item
        elif item > self.period:
            item = item - (item // self.period) * self.period
        elif item == self.period:
            item = 0

        return self.series._get_for(self.series.domain.start + item)
