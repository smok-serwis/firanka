"""
A module describing our function's domains.

These domains are subset of the real number set.
"""
import logging
import operator
import functools
import typing as tp
import enum
from abc import abstractmethod, ABCMeta

logger = logging.getLogger(__name__)

__all__ = ['Closing', 'Domain', 'SingleIntervalDomain', 'EmptyDomain', 'PatchworkDomain']


class Closing(enum.Enum):
    CLOSED = 0       # a < or > closing
    OPEN = 1        # a ( or ) closing

    def __or__(self, other):
        if self.value == Closing.CLOSED or other.value == Closing.CLOSED:
            return Closing.CLOSED
        else:
            return Closing.OPEN

    def __and__(self, other):
        if self.value == Closing.OPEN or other.value == Closing.OPEN:
            return Closing.OPEN
        else:
            return Closing.CLOSED


class Domain(metaclass=ABCMeta):
    """
    A base class for the domains
    """
    @abstractmethod
    def __contains__(self, item: float) -> bool:
        ...

    @abstractmethod
    def __add__(self, other: 'Domain') -> 'Domain':
        ...

    @abstractmethod
    def __eq__(self, other: 'Domain') -> 'Domain':
        ...

    @abstractmethod
    def __hash__(self) -> int:
        ...

    @abstractmethod
    def __mul__(self, other: 'Domain') -> 'Domain':
        ...

    def __lt__(self, other: 'Domain') -> bool:
        return self.starts_at() < other.starts_at()

    def __le__(self, other: 'Domain') -> bool:
        return self.starts_at() <= other.starts_at()

    def __gt__(self, other: 'Domain') -> bool:
        return self.starts_at() > other.starts_at()

    def __ge__(self, other: 'Domain') -> bool:
        return self.starts_at() >= other.starts_at()

    @abstractmethod
    def starts_at(self) -> float:
        """
        :return: lowest real number that this domain includes (or not)
        """


class RealSetDomain(Domain):
    """
    A domain that envelops the entire real number set
    """
    def starts_at(self) -> float:
        return float('-inf')

    def __add__(self, other):
        return RealSetDomain()

    def __eq__(self, other):
        return isinstance(other, RealSetDomain)

    def __hash__(self):
        return 0

    def __mul__(self, other):
        return other

    def __contains__(self, item: float) -> bool:
        return True


class SingleIntervalDomain(Domain):
    """
    A domain consisting of a single interval of the real number set
    """
    def __init__(self, left_limit: float, left_close: Closing, right_limit: float,
                 right_close: Closing):
        self.left_limit = left_limit
        self.left_close = left_close
        self.right_limit = right_limit
        self.right_close = right_close

    def __mul__(self, other: 'Domain') -> 'Domain':
        if not isinstance(other, SingleIntervalDomain):
            raise NotImplementedError('not yet implemented')

        if self.left_limit > other.left_limit:
            return other * self

        assert self.left_limit <= other.left_limit

        if ((self.right_limit < other.left_limit) or (other.right_limit < other.left_limit)) or (
                self.right_limit == other.left_limit and not (self.left_close and other.left_close)):
            return EmptyDomain()

        # Set up range left_limit
        if self.left_limit == other.left_limit:
            left_limit = self.left_limit
            left_close = self.left_close and other.left_close
        else:
            left_limit = other.left_limit
            left_close = Closing.CLOSED if other.left_limit in self else Closing.CLOSED

        # Set up range end
        if self.right_limit == other.right_limit:
            right_limit = self.right_limit
            right_close = self.right_close and other.right_close
        else:
            p, q = (self, other) if self.right_limit < other.right_limit else (other, self)
            right_limit = p.right_limit
            right_close = p.right_close and (Closing.CLOSED if (right_limit in q) else Closing.OPEN)

        return SingleIntervalDomain(left_limit, left_close, right_limit, right_close)

    def starts_at(self) -> float:
        return self.left_limit

    def __contains__(self, item: float):
        if not self.left_limit <= item <= self.right_limit:
            return False

        if item == self.left_limit:
            if self.left_close == Closing.CLOSED:
                return True
            else:
                return False

        if item == self.right_limit:
            if self.right_close == Closing.CLOSED:
                return True
            else:
                return False

        return True

    def __add__(self, other: Domain):
        if isinstance(other, EmptyDomain):
            return self

        if isinstance(other, PointyDomain):
            return PatchworkDomain([self, other])

        if isinstance(other, PatchworkDomain):
            return PatchworkDomain(other.domains + [self])

        if not isinstance(other, SingleIntervalDomain):
            # let's hope that this other domain supports adding us
            return other + self

        # this means that we are adding a SingleIntervalDomain to a SingleIntervalDomain

        # make it so that self starts at less value then
        if self.left_limit > self.right_limit:
            self, other = other, self

        # possible situations are such
        #
        #       <self>   ... <other>

        if self.right_limit < other.left_limit:
            return PatchworkDomain([self, other])
        elif self.right_limit == other.left_limit:
            if self.right_close == Closing.CLOSED or other.left_close == Closing.CLOSED:
                return SingleIntervalDomain(self.left_limit, self.left_close, other.right_limit, other.right_close)
            else:
                return PatchworkDomain([self, other])

        #   <self>
        #      <other>

        if self.right_limit > other.left_limit:
            #   <  s e  l  f >
            #       <other>
            if other.right_limit < self.right_limit:
                return self

            #   < s e l f >
            #       <other>
            elif other.right_limit == self.right_limit:
                return SingleIntervalDomain(self.left_limit, self.left_close,
                                            self.right_limit, self.right_limit or other.right_limit)
            #   <self>
            #       <other>
            else:
                return SingleIntervalDomain(self.left_limit, self.left_close, other.right_limit,
                                            other.right_close)

    def __eq__(self, other: 'SingleIntervalDomain') -> bool:
        if not isinstance(other, SingleIntervalDomain):
            return False
        else:
            return self.left_limit == other.left_limit and self.left_close == other.left_close and \
                    other.right_limit == self.right_limit and self.right_close == other.right_close

    def __hash__(self) -> int:
        return hash(self.left_limit) ^ hash(self.left_close) ^ hash(self.right_close) ^ \
               hash(self.right_limit)

    def __str__(self) -> str:
        return '%s%s;%s%s' % ('<' if self.left_close == Closing.CLOSED else '(',
                              self.left_limit,
                              self.right_limit,
                              '>' if self.right_close == Closing.CLOSED else ')')


class EmptyDomain(Domain):
    def __contains__(self, item: float) -> bool:
        return False

    def __add__(self, other: 'Domain') -> 'Domain':
        return other

    def __eq__(self, other: 'Domain') -> 'Domain':
        if isinstance(other, EmptyDomain):
            return True
        return False

    def __hash__(self) -> int:
        return 0

    def __mul__(self, other):
        return EmptyDomain()

    def starts_at(self) -> float:
        return 0.0


class PointyDomain(Domain):
    """
    A domain that consists of single points

    :param points: an iterable of points to consider to lie within this domain
    """
    def __init__(self, points: tp.Iterable[float]):
        self.points = list(points)
        self.points.sort()
        if not self.points:
            raise ValueError('Cannot instantiate an empty PointyDomain, use EmptyDomain instead')

    def __contains__(self, item: float) -> bool:
        return item in self.points

    def starts_at(self) -> float:
        return self.points[0]

    def __add__(self, other: 'Domain') -> 'Domain':
        if isinstance(other, PointyDomain):
            return PointyDomain(set(self.points).union(set(other.points)))
        else:
            return PatchworkDomain(other.domains + [self])

    def __mul__(self, other):
        points = []
        for point in self.points:
            if point in other:
                points.append(point)
        return PointyDomain(points)

    def __hash__(self) -> int:
        return functools.reduce(operator.xor, map(hash, self.points))

    def __eq__(self, other: 'Domain') -> bool:
        if not isinstance(other, PointyDomain):
            return False
        else:
            return self.points == other.points


class PatchworkDomain(Domain):
    """
    A domain pieced together from other domains
    """
    def __init__(self, domains: tp.Iterable[Domain]):
        self.domains = []
        for domain in domains:
            if isinstance(domain, PatchworkDomain):
                self.domains.extend(domain.domains)
            else:
                self.domains.append(domain)
        self.domains.sort()

    def __contains__(self, item: float):
        for domain in self.domains:
            if item in domain:
                return True

        return False

    def __eq__(self, other: 'Domain') -> bool:
        if not isinstance(other, PatchworkDomain):
            return False
        else:
            return self.domains == other.domains

    def __hash__(self) -> int:
        return functools.reduce(operator.xor, map(hash, self.domains))

    def __mul__(self, other):
        if isinstance(other, EmptyDomain):
            return EmptyDomain()
        raise NotImplementedError()

    def __add__(self, other):
        if isinstance(other, EmptyDomain):
            return self
        raise NotImplementedError()

    def starts_at(self) -> float:
        return functools.reduce(lambda a, b:  min(a, b), (a.starts_at() for a in self.domains))
