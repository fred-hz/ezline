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
        df[FETCH_FIELDS[0]] = df[FETCH_FIELDS[0]].astype('string')
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

    def get_all_sids(self):
        return self.data[TICKER_FIELD].tolist()

    def get_data(self):
        return self.data