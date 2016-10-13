import tushare as ts
from config import globals as gs
from .file_portal import (
    FileReader,
    FileWriter,
    DataframeFileSaver,
    DataframeFileFetcher
)
from collections import namedtuple
from data.stocks import AShareStocks

FETCH_FIELDS = ['ticker',
                'tradeDate',
                'actPreClosePrice',
                'openPrice',
                'highestPrice',
                'lowestPrice',
                'closePrice',
                'turnoverVol',
                'turnoverValue',
                'dealAmount',
                'turnoverRate',
                'negMarketValue',
                'marketValue',
                'isOpen',
                'PE',
                'PE1',
                'PB']

TICKER_FIELD = 'ticker'
TRADE_DATE_FIELD = 'trade_date'
PRE_CLOSE_PRICE_FIELD = 'pre_close_price'
OPEN_PRICE_FIELD = 'open_price'
HIGHEST_PRICE_FIELD = 'highest_price'
LOWEST_PRICE_FIELD = 'lowest_price'
TURNOVER_VOL_FIELD = 'turnover_vol'
TURNOVER_VALUE_FIELD = 'turnover_value'
DEAL_AMOUNT_FIELD = 'deal_amount'
TURNOVER_RATE_FIELD = 'turnover_rate'
NEG_MARKET_VALUE_FIELD = 'neg_market_value'
MARKET_VALUE_FIELD = 'market_value'
IS_OPEN_FIELD = 'is_open'
PE_FIELD = 'PE'
SUPPOSED_PE_FIELD = 'supposed_PE'
SUPPOSED_PB_FIELD = 'supposed_PB'

DailyTradeTupe = namedtuple('DailyTradeTupe', [TICKER_FIELD,
                                               TRADE_DATE_FIELD,
                                               PRE_CLOSE_PRICE_FIELD,
                                               OPEN_PRICE_FIELD,
                                               HIGHEST_PRICE_FIELD,
                                               LOWEST_PRICE_FIELD,
                                               TURNOVER_VOL_FIELD,
                                               TURNOVER_VALUE_FIELD,
                                               DEAL_AMOUNT_FIELD,
                                               TURNOVER_RATE_FIELD,
                                               NEG_MARKET_VALUE_FIELD,
                                               MARKET_VALUE_FIELD,
                                               IS_OPEN_FIELD,
                                               PE_FIELD,
                                               SUPPOSED_PE_FIELD,
                                               SUPPOSED_PB_FIELD])

class AShareDailyTradeWriter():
    def __init__(self):
        self.file_writer = FileWriter(gs.A_SHARE_DAILY_TRADE_PATH,
                                      DataframeFileSaver())
        self.ashare_stocks = AShareStocks()

    def load_Internet_data(self):
        mt = ts.Market()
        data = None
        for sid in self.ashare_stocks.get_all_sids():
            df = mt.MktEqud(ticker=sid, field=','.join(FETCH_FIELDS))
            if df is not None and not df.empty:
                df[FETCH_FIELDS[0]] = df[FETCH_FIELDS[0]].astype('string')
                df[FETCH_FIELDS[0]] = sid
            if data is None or data.empty:
                if df is not None and not df.empty:
                    data = df
            elif df is not None and not df.empty:
                data = data.append(df, ignore_index=True)
            print 'sid: ' + str(sid) + ' completed, size ' + str(len(data))

        data.rename(columns={FETCH_FIELDS[0]: TICKER_FIELD,
                             FETCH_FIELDS[1]: TRADE_DATE_FIELD,
                             FETCH_FIELDS[2]: PRE_CLOSE_PRICE_FIELD,
                             FETCH_FIELDS[3]: OPEN_PRICE_FIELD,
                             FETCH_FIELDS[4]: HIGHEST_PRICE_FIELD,
                             FETCH_FIELDS[5]: LOWEST_PRICE_FIELD,
                             FETCH_FIELDS[6]: TURNOVER_VOL_FIELD,
                             FETCH_FIELDS[7]: TURNOVER_VALUE_FIELD,
                             FETCH_FIELDS[8]: DEAL_AMOUNT_FIELD,
                             FETCH_FIELDS[9]: TURNOVER_RATE_FIELD,
                             FETCH_FIELDS[10]: NEG_MARKET_VALUE_FIELD,
                             FETCH_FIELDS[11]: MARKET_VALUE_FIELD,
                             FETCH_FIELDS[12]: IS_OPEN_FIELD,
                             FETCH_FIELDS[13]: PE_FIELD,
                             FETCH_FIELDS[14]: SUPPOSED_PE_FIELD,
                             FETCH_FIELDS[15]: SUPPOSED_PB_FIELD},
                    inplace=True)
        return data

    def write(self):
        self.file_writer.write(self.load_Internet_data())

class AshareDailyTrade():
    def __init__(self):
        self.file_reader = FileReader(gs.A_SHARE_DAILY_TRADE_PATH,
                                      DataframeFileFetcher())
        self.data = self.read()

    def read(self):
        return self.file_reader.read()

    def get_trade_info(self, ticker, date, columns=None):
        '''
        :param ticker:
        :param date:
        :param columns: Should be an array
        :return:
        '''
        if columns is None:
            result = self.data[(self.data[TICKER_FIELD] == ticker) and
                               (self.data[TRADE_DATE_FIELD] == date)]
        else:
            result = self.data[(self.data[TICKER_FIELD] == ticker) and
                               (self.data[TRADE_DATE_FIELD] == date)][columns]
        if result is None or result.empty:
            return None
        else:
            return result[0]