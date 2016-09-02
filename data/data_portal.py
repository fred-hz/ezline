from abc import ABCMeta, abstractproperty
from six import with_metaclass
import numpy as np
import pandas as pd
import codecs

def write_dataframe_to_csv(data, file_path):
    data.to_csv(file_path)

def write_array_to_csv(data, file_path):
    file_write_obj = codecs.open(file_path, 'w')
    for line in data:
        file_write_obj.write(line)
        file_write_obj.write('\n')

class DataWriter(with_metaclass(ABCMeta)):

    def __init__(self, _write):
        self._write = _write

    @abstractproperty
    def file_path(self):
        raise NotImplementedError()

    @abstractproperty
    def data(self):
        raise NotImplementedError()

    def write(self):
        self._write(self.data, self.file_path)
        return self.data

def read_csv_to_dataframe(file_path):
    return pd.read_csv(file_path)

def read_csv_to_array(file_path):
    file_read_obj = codecs.open(file_path, 'r')
    return file_read_obj.read().split('\n')

class DataReader(with_metaclass(ABCMeta)):

    def __init__(self, _read):
        self._read = _read
        self.data = None

    @abstractproperty
    def file_path(self):
        raise NotImplementedError()

    def read(self):
        self.data = self._read(self.file_path)
        return self.data