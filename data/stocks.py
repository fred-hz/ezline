from config import globals as gs
from .data_portal import (
    DataWriter,
    DataReader,
    write_array_to_csv,
    read_csv_to_array
)

class AShareStocksWriter(DataWriter):

    def __init__(self, _write=write_array_to_csv):
        super(AShareStocksWriter, self).__init__(_write)

    @property
    def file_path(self):
        return gs.A_Share_STOCKS_PATH

    @property
    def data(self):
        # Not finished yet
        pass

class AShareStockReader(DataReader):

    def __init__(self, _read=read_csv_to_array):
        super(AShareStockReader, self).__init__(_read)

    @property
    def file_path(self):
        return gs.A_Share_STOCKS_PATH
