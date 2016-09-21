from config import globals as gs
from .data_portal import (
    DataWriter,
    DataReader,
    write_array_to_csv,
    read_csv_to_array
)

class NaturalCalWriter(DataWriter):

    def __init__(self, _write=write_array_to_csv):
        super(NaturalCalWriter, self).__init__(_write)

    @property
    def file_path(self):
        return gs.NATURAL_CALENDAR_PATH

    def set_data(self):
        # Not finished yet
        pass

class NaturalCalReader(DataReader):

    def __init__(self, _read=read_csv_to_array):
        super(NaturalCalReader, self).__init__(_read)

    @property
    def file_path(self):
        return gs.NATURAL_CALENDAR_PATH

class AShareTradingCalWriter(DataWriter):

    def __init__(self, _write=write_array_to_csv):
        super(AShareTradingCalWriter, self).__init__(_write)

    @property
    def file_path(self):
        return gs.A_SHARE_TRADING_CALENDAR_PATH

    def set_data(self):
        # Not finished yet
        pass

class AShareTradingCalReader(DataReader):

    def __init__(self, _read=read_csv_to_array):
        super(AShareTradingCalReader, self).__init__(_read)

    @property
    def file_path(self):
        return gs.A_SHARE_TRADING_CALENDAR_PATH