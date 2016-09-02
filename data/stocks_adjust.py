import tushare as ts
from config import globals as gs
from .data_portal import (
    DataWriter,
    DataReader,
    write_dataframe_to_csv,
    read_csv_to_dataframe
)
from .calendar import AShareTradingCalReader
from .stocks import AShareStockReader
from datautil.ez_tushare import MktAdjf
from util.date import date_format

class AShareStockAdjWriter(DataWriter):

    def __init__(self, _write=write_dataframe_to_csv):
        super(AShareStockAdjWriter, self).__init__(_write)

    @property
    def file_path(self):
        return gs.STOCKS_ADJUST_PATH

    @property
    def data(self):
        asr = AShareStockReader()
        data = None
        stocks_list = asr.read()
        for stock in stocks_list:
            begin_date = date_format(gs.DATE_BEGIN_DEFAULT, '%Y%m%d')
            end_date = date_format(gs.DATE_END_DEFAULT, '%Y%m%d')
            new_data = MktAdjf(ticker=stock, beginDate=begin_date, endDate=end_date)
            if new_data is None or new_data.empty:
                continue
            if data is None:
                data = new_data
            else:
                data = data.append(new_data, ignore_index=True)
        return data

class AShareStockAdjReader(DataReader):

    def __init__(self, _read=read_csv_to_dataframe):
        super(AShareStockAdjReader, self).__init__(_read)

    @property
    def file_path(self):
        return gs.STOCKS_ADJUST_PATH