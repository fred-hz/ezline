"""
Base factor for Filters, Factors and Classifiers
"""

from abc import ABCMeta, abstractmethod
from six import with_metaclass

class Term(with_metaclass(ABCMeta, object)):

    @abstractmethod
    def _compute(self, inputs, time, assets, mask):
        raise NotImplementedError()