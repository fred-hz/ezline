from config import globals as gs
from .file_portal import (
    FileReader,
    FileWriter,
    DataframeFileSaver,
    DataframeFileFetcher,
)
from pandas import Series
import tushare as ts

FETCH_FIELDS = ['ticker',
                'secShortName',
                'exchangeCD',
                'listStatusCD',
                'listDate']

INDEX_FIELD = 'index'
TICKER_FIELD = 'ticker'
NAME_FIELD = 'name'
EXCHANGE_FIELD = 'exchange'
STATUS_FIELD = 'status'
LIST_DATE_FIELD = 'list_date'

class AShareStocksWriter():
    def __init__(self):
        self.file_writer = FileWriter(gs.A_SHARE_STOCKS_PATH,
                                      DataframeFileSaver())

    def load_Internet_data(self):
        mt = ts.Master()
        df = mt.SecID(assetClass='E', field=','.join(FETCH_FIELDS))
        df.rename(columns={FETCH_FIELDS[0]: TICKER_FIELD,
                           FETCH_FIELDS[1]: NAME_FIELD,
                           FETCH_FIELDS[2]: EXCHANGE_FIELD,
                           FETCH_FIELDS[3]: STATUS_FIELD,
                           FETCH_FIELDS[4]: LIST_DATE_FIELD},
                  inplace=True)
        df = df[df[EXCHANGE_FIELD].isin([gs.SHANGHAI_EXCHANGE, gs.SHENZHEN_EXCHANGE])]
        df.index = Series(range(1,len(df)+1))
        return df

    def write(self):
        self.file_writer.write(self.load_Internet_data())

class AShareStocks():
    def __init__(self):
        self.file_reader = FileReader(gs.A_SHARE_STOCKS_PATH,
                                      DataframeFileFetcher())
        self.data = self.read()

    def read(self):
        return self.file_reader.read()

    def get_info_by_columns(self, ticker=None, name=None, exchange=None, status=None, list_date=None, fields=None):
        pass

    def get_ticker_by_name(self, name):
        ticker_list =  self.data[self.data[NAME_FIELD] == name][TICKER_FIELD].tolist()
        if ticker_list is not None:
            return ticker_list[0]
        else:
            return None

    def get_name_by_ticker(self, ticker):
        name_list = self.data[self.data[TICKER_FIELD] == ticker][NAME_FIELD].tolist()
        if name_list is not None:
            return name_list[0]
        else:
            return None

    def get_all_tickers_name(self):
        return self.data[NAME_FIELD].tolist()

    def get_data(self):
        return self.data

'''
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


    list = []
    for index, row in data.iterrows():
        if len(str(row['ticker'])) < 6:
            if row['ticker'] not in list:
                print row['ticker']
                list.append(row['ticker'])
            data[index, 'ticker'] = format_tickerID(row['ticker'])
            #data[index]['ticker'] = format_tickerID(row['ticker'])
            #print data[index]['ticker']

    asw = AShareDailyTradeWriter()
    asw.data = data
    asw.write()'''
