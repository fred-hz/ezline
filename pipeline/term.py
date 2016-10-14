"""
Base factor for Filters, Factors and Classifiers
"""

from abc import ABCMeta, abstractmethod
from six import with_metaclass


class Term(with_metaclass(ABCMeta, object)):
    window_length = None
    missing_value = None

    def __init__(self,
                 window_length=window_length,
                 missing_value=missing_value):
        self.window_length = window_length
        self.missing_value = missing_value

    @abstractmethod
    def _compute(self, inputs, time, assets, mask):
        """
        Logical computing function for Filter, Factors and Classifiers.
        Function compute() is reserved for Custom Terms.
        Every day @inputs, @time, @assets and @mask will be different
        :param inputs: Arrays
        :param time: Supposed to be date or time
        :param assets: Supposed to be asset ids
        :param mask: Filters which mask useless data
        :return:
        """
        raise NotImplementedError()