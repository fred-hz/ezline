from config import globals as gs
from .data_portal import (
    DataWriter,
    DataReader,
    write_array_to_csv,
    write_dataframe_to_csv,
    read_csv_to_array,
    read_csv_to_dataframe
)

class AShareStocksWriter(DataWriter):
    def __init__(self, _write=write_array_to_csv):
        super(AShareStocksWriter, self).__init__(_write)

    @property
    def file_path(self):
        return gs.A_SHARE_STOCKS_PATH

    def set_data(self):
        # Not finished yet
        pass

class AShareStockReader(DataReader):
    def __init__(self, _read=read_csv_to_array):
        super(AShareStockReader, self).__init__(_read)

    @property
    def file_path(self):
        return gs.A_SHARE_STOCKS_PATH

class AShareDailyTradeWriter(DataWriter):
    def __init__(self, _write=write_dataframe_to_csv):
        super(AShareDailyTradeWriter, self).__init__(_write)

    @property
    def file_path(self):
        return gs.A_SHARE_DAILY_TRADE_PATH

    def set_data(self):
        # Not finished yet
        pass


class AShareDailyTradeReader(DataReader):
    def __init__(self, _read=read_csv_to_dataframe):
        super(AShareDailyTradeReader, self).__init__(_read)

    @property
    def file_path(self):
        return gs.A_SHARE_DAILY_TRADE_PATH

def format_tickerID(ticker):
    result = str(ticker)
    while(len(result) < 6):
        result = '0' + result
    return result

def justify_tickers():
    print 'Starting reading'
    asr = AShareDailyTradeReader()
    data = asr.read()

    del asr

    #print data['tradeDate']
    print 'Starting converting'
    #mask = (data['ticker']/100000==0)
    #print mask

    list = []
    ticker_row = data['ticker']
    for index in ticker_row.index:
        value = ticker_row[index]
        if len(str(value))<6:
            if value not in list:
                print index, value
                list.append(value)
            ticker_row[index] = format_tickerID(value)

    data['ticker'] = ticker_row


    '''list = []
    for index, row in data.iterrows():
        if len(str(row['ticker'])) < 6:
            if row['ticker'] not in list:
                print row['ticker']
                list.append(row['ticker'])
            data[index, 'ticker'] = format_tickerID(row['ticker'])
            #data[index]['ticker'] = format_tickerID(row['ticker'])
            #print data[index]['ticker']'''

    print 'Starting writing'
    asw = AShareDailyTradeWriter()
    asw.data = data
    asw.write()
