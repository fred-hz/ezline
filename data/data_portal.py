from abc import ABCMeta, abstractproperty, abstractmethod
from six import with_metaclass
import numpy as np
import pandas as pd
import codecs
import csv
import os

MULTI_FILES_READ_FIELDS = frozenset(['path_fix',
                                    'content'])

def write_dataframe_to_csv(data, file_path):
    data.to_csv(file_path)

def write_array_to_csv(data, file_path):
    file_write_obj = codecs.open(file_path, 'w')
    for line in data:
        file_write_obj.write(line)
        file_write_obj.write('\n')
    file_write_obj.close()

def write_dictlist_to_csv(data, file_path):
    """
    Need to ensure that the keys of dict are same
    :param data: A list of dicts
    :param file_path:
    :return:
    """
    writer = None
    csv_file = open(file_path, 'w')
    for row_dict in data:
        if writer is None:
            writer = csv.DictWriter(csv_file, fieldnames=row_dict.keys())
            writer.writeheader()
        writer.writerow(row_dict)
    csv_file.close()

class SingleFileWriter():

    def __init__(self, _write, data=None, file_path=None):
        self._write = _write
        self.data = data
        self.file_path = file_path

    def write(self):
        if self.data is not None and self.file_path is not None:
            self._write(self.data, self.file_path)
        else:
            raise Exception('Writing files without data or file_path')

class MultiFilesWriter():

    def __init__(self, _write, data=None, root_path=None, path_fix=None):
        # data and path_fix should be list
        self._write = _write
        self.data = data
        self.root_path = root_path
        self.path_fix = path_fix

    def write(self):
        if (self.data is not None) and (self.root_path is not None) and (self.path_fix is not None):
            for data_piece, path_fix_piece in zip(self.data, self.path_fix):
                self._write(data_piece, self.root_path + path_fix_piece)

class DataWriter(with_metaclass(ABCMeta)):

    def __init__(self, _write):
        self._write = _write
        self.data = None

    @abstractproperty
    def file_path(self):
        raise NotImplementedError()

    @abstractmethod
    def set_data(self, params=None):
        # Need to set self.data
        raise NotImplementedError()

    def write(self):
        if self.data is None:
            print 'Data is None. Writing aborted.'
            return
        self._write(self.data, self.file_path)
        return self.data

def read_csv_to_dataframe(file_path):
    return pd.read_csv(file_path)

def read_csv_to_array(file_path):
    file_read_obj = codecs.open(file_path, 'r')
    return file_read_obj.read().split('\n')

def read_csv_to_dictlist(file_path):
    csv_file = open(file_path, 'rb')
    reader = csv.DictReader(csv_file)
    return [row_dict for row_dict in reader]

class SingleFileReader():

    def __init__(self, _read, file_path=None):
        self._read = _read
        self.file_path = file_path

    def read(self):
        if self.file_path is not None:
            self.data = self._read(self.file_path)
            return self.data
        else:
            raise Exception('Reading file without file_path')

class MultiFilesReader():

    def __init__(self, _read, root_path=None, selected_files=None, selected_folders=None):
        """
        :param _read:
        :param root_path:
        :param selected_files: Variable selected_files should be a list containing target files.
        If it is empty then select all the files under the dir
        :param selected_folders: Variable selected_folders should be a list containing target folders.
        If it is empty then select all the folders
        """
        self._read = _read
        self.root_path = root_path
        self.selected_files = selected_files
        self.selected_folders = selected_folders

    def read_one_layer(self, path_fix):
        files = os.listdir(self.root_path + path_fix)

    def read(self):
        if self.root_path is None:
            raise Exception('Reading multi-files without root_path')

        if self.selected_files is None:
            files = [file for file in os.listdir(self.root_path)
                     if os.path.isfile(self.root_path + os.sep + file)]
        else:
            result = []
            for file_fix in self.selected_files:
                absolute_path = self.root_path + os.sep + file_fix
                if os.path.exists(absolute_path):
                    result.append({'path_fix': file_fix,
                                   'content': self._read(absolute_path)})


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