from data.data_portal import (
    DataWriter,
    DataReader
)
from abc import ABCMeta, abstractproperty, abstractmethod
import pandas as pd
import codecs
import csv


class FileSaveInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def save(self, data, file_path):
        pass


class PlainTextFileSaver(FileSaveInterface):
    def __init__(self):
        pass

    def save(self, data, file_path):
        file_write_obj = open(file_path, 'w')
        file_write_obj.write(data)
        file_write_obj.close()


class DataframeFileSaver(FileSaveInterface):
    def __init__(self):
        pass

    def save(self, data, file_path, sep='|', index=False, encoding='utf8'):
        data.to_csv(file_path, sep=sep, index=index, encoding=encoding)


class ListFileSaver(FileSaveInterface):
    def __init__(self):
        pass

    def save(self, data, file_path):
        file_write_obj = codecs.open(file_path, 'w')
        for line in data:
            file_write_obj.write()
            file_write_obj.write()
        file_write_obj.close()


class DictlistFileSaver(FileSaveInterface):
    def __init__(self):
        pass

    def save(self, data, file_path):
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


class FileFetchInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def fetch(self, file_path):
        pass


class PlainTextFileFetcher(FileFetchInterface):
    def __init__(self):
        pass

    def fetch(self, file_path):
        pass


class DataframeFileFetcher(FileFetchInterface):
    def __init__(self):
        pass

    def fetch(self, file_path, sep='|', encoding='utf8', dtype='string'):
        return pd.read_csv(file_path, sep=sep, encoding=encoding, dtype=dtype)


class ListFileFetcher(FileFetchInterface):
    def __init__(self):
        pass

    def fetch(self, file_path):
        file_read_obj = codecs.open(file_path, 'r')
        return file_read_obj.read().split('\n')


class DictlistFileFetcher(FileFetchInterface):
    def __init__(self):
        pass

    def fetch(self, file_path):
        csv_file = open(file_path, 'rb')
        reader = csv.DictReader(csv_file)
        return [row_dict for row_dict in reader]



class FileWriter(DataWriter):
    def __init__(self, file_path, file_saver):
        self.file_path = file_path
        self.file_saver = file_saver
        super(FileWriter, self).__init__()

    def write(self, data):
        self.file_saver.save(data, self.file_path)

class FileReader(DataReader):
    def __init__(self, file_path, file_fetcher):
        self.file_path = file_path
        self.file_fetcher = file_fetcher
        super(FileReader, self).__init__()

    def read(self):
        return self.file_fetcher.fetch(self.file_path)