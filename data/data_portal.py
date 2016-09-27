from abc import ABCMeta, abstractproperty, abstractmethod
from six import with_metaclass
import numpy as np
import pandas as pd
import codecs
import csv
import os


class DataWriter(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def write(self, data):
        pass


class DataReader(object):
    __metaclass__ =  ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def read(self):
        pass