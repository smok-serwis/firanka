# coding=UTF-8
from __future__ import print_function, absolute_import, division

__all__ = [
    'FirankaError',
    'NotInDomainError',
    'DomainError',
]


class FirankaError(Exception):
    """
    Base class for firanka's exceptions
    """


class DomainError(FirankaError, ValueError):
    """Has something to do with the domain :)"""


class NotInDomainError(DomainError):
    """
    Requested index is beyond this domain
    """

    def __init__(self, index, domain):
        super(NotInDomainError, self).__init__(u'NotInDomainError: %s not in %s' % (index, domain))
        self.index = index
        self.domain = domain
