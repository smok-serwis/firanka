__all__ = ['FirankaError', 'NotInDomainError', 'DomainError']


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

    def __init__(self, index, domain, *args, **kwargs):
        super().__init__(u'NotInDomainError: %s not in %s' % (index, domain), index, domain,
                         *args, **kwargs)
        self.index = index
        self.domain = domain
