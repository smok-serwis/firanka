import logging
import typing as tp
import sympy
from abc import ABCMeta, abstractmethod
import collections
logger = logging.getLogger(__name__)


Variable = collections.namedtuple('Variable', ('name', ))


class BaseStructure(metaclass=ABCMeta):
    """
    Base class for structures of our time-series
    """
    @abstractmethod
    def get_variables(self) -> tp.List[Variable]:
        """
        Return a list of our backing variables
        :return:
        """
        ...

    @abstractmethod
    def get_expression(self) -> sympy.Expr:
        ...

