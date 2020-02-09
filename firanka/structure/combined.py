import logging
import typing as tp
from .base import BaseStructure
logger = logging.getLogger(__name__)

class CombinedStructure(BaseStructure):
    """
    A part that maps some of the domain into some structures. Essentially, a structure
    that patchworks the entire domain from some substructures
    """
