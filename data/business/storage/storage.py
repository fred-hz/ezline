from abc import ABCMeta, abstractmethod
from data.persistence.file_portal import (
    FileReader,
    FileWriter,
)
import pandas as pd


class DataStorage(object):
    __metaclass__ = ABCMeta

    def __init__(self, data_writer, fields_map):
        """
        DataStorage is the intermediate class to fetch data and store it into persistence
        :param data_writer: data.persistence.file_portal.FileWriter
        :param fields_map: dict class which maps fetched fields to storage fields
        """
        self.data_writer = data_writer
        self.fields_map = fields_map
        self.data = None

    @abstractmethod
    def load_data(self):
        """
        Load data into self.data which can then be renamed and stored.
        self.data should be a pandas.dataframe
        :return:
        """
        pass

    @abstractmethod
    def write(self):
        """
        Store self.data into persistence with data_writer
        :return:
        """
        pass


class DataframeStorage(DataStorage):

    def __init__(self, data_writer, fields_map):
        super(DataframeStorage, self).__init__(data_writer, fields_map)

    @abstractmethod
    def load_data(self):
        pass

    def _rename(self):
        assert isinstance(self.fields_map, dict)
        self.data.rename(columns=self.fields_map,
                         inplace=True)

    def write(self):
        if self.data is None or not isinstance(self.data, pd.DataFrame):
            raise ValueError(
                "data of class {self_class} should be pd.DataFrame, but be {error_class} instead".format(
                    self_class=type(self),
                    error_class=type(self.data)
                ))

        self._rename()
        self.data_writer.write(self.data)

