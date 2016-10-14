from abc import ABCMeta, abstractmethod
from data.persistence.file_portal import (
    FileReader,
    FileWriter,
)
import pandas as pd


class DataFetch(object):
    __metaclass__ = ABCMeta

    def __init__(self, data_reader):
        """
        DataFetch is the intermediate class to fetch data from persistence and provide
        it to the data interface, which transfers data with a convenient call
        :param data_reader:
        """
        self.data_reader = data_reader
        self.data = None

    def read(self):
        self.data = self.data_reader.read()

