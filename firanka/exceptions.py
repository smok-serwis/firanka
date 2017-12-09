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


class DomainError(FirankaError):
    """Has something to do with the domain :)"""


class NotInDomainError(DomainError, ValueError):
    """
    Requested index is beyond this domain
    """
