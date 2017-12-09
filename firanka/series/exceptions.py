# coding=UTF-8
from __future__ import print_function, absolute_import, division
import six
import logging


class FirankaError(Exception):
    pass


class NotInDomainError(FirankaError, ValueError):
    """
    Requested index is beyond this domain
    """
