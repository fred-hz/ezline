from collections import namedtuple

import tushare as ts

from config import globals as gs
from data.persistence.file_portal import (
    FileReader,
    FileWriter,
    DataframeFileSaver,
    DataframeFileFetcher
)
from data.stocks import AShareStocks

# adjFactor and AccumAdjFactor should not be used
FETCH_FIELDS = ['ticker',
                'exDivDate',
                'perCashDiv',
                'perShareDivRatio',
                'perShareTransRatio',
                'allotmentRatio',
                'allotmentPrice',
                'adjFactor',
                'accumAdjFactor']

TICKER_FIELD = 'ticker'
DIV_DATE_FIELD = 'div_date'
PER_CASH_FIELD = 'per_cash'
PER_SHARE_DIV_FIELD = 'per_share_div_ratio'
PER_SHARE_TRANS_FIELD = 'per_share_trans_ratio'
ALLOTMENT_RATIO_FIELD = 'allotment_ratio'
ALLOTMENT_PRICE_FIELD = 'allotment_price'
ADJ_FACTOR_FIELD = 'adj_factor'
ACCUM_ADJ_FACTOR_FIELD = 'accum_adj_factor'

Adj_tuple = namedtuple('Adj_tuple', [TICKER_FIELD,
                                     DIV_DATE_FIELD,
                                     PER_CASH_FIELD,
                                     PER_SHARE_DIV_FIELD,
                                     PER_SHARE_TRANS_FIELD,
                                     ALLOTMENT_RATIO_FIELD,
                                     ALLOTMENT_PRICE_FIELD])

class AShareStocksAdjWriter(object):
    def __init__(self):
        self.file_writer = FileWriter(gs.A_SHARE_STOCKS_ADJUST_PATH,
                                      DataframeFileSaver())
        self.ashare_stocks = AShareStocks()

    def load_Internet_data(self):
        mt = ts.Market()
        data = None
        for sid in self.ashare_stocks.get_all_sids():
            df = mt.MktAdjf(ticker=sid, field=','.join(FETCH_FIELDS))
            if df is not None and not df.empty:
                df[FETCH_FIELDS[0]] = df[FETCH_FIELDS[0]].astype('string')
                # df.astype('string')
                df[FETCH_FIELDS[0]] = sid
            if data is None or data.empty:
                if df is not None and not df.empty:
                    data = df
            elif df is not None and not df.empty:
                data = data.append(df, ignore_index=True)

        data.rename(columns={FETCH_FIELDS[0]: TICKER_FIELD,
                             FETCH_FIELDS[1]: DIV_DATE_FIELD,
                             FETCH_FIELDS[2]: PER_CASH_FIELD,
                             FETCH_FIELDS[3]: PER_SHARE_DIV_FIELD,
                             FETCH_FIELDS[4]: PER_SHARE_TRANS_FIELD,
                             FETCH_FIELDS[5]: ALLOTMENT_RATIO_FIELD,
                             FETCH_FIELDS[6]: ALLOTMENT_PRICE_FIELD,
                             FETCH_FIELDS[7]: ADJ_FACTOR_FIELD,
                             FETCH_FIELDS[8]: ACCUM_ADJ_FACTOR_FIELD},
                    inplace=True)
        return data

    def write(self):
        self.file_writer.write(self.load_Internet_data())


class AShareStocksAdj(object):
    def __init__(self):
        self.file_reader = FileReader(gs.A_SHARE_STOCKS_ADJUST_PATH,
                                      DataframeFileFetcher())
        self.data = self.read()

    def read(self):
        return self.file_reader.read()

    def get_adjs_by_ticker(self, ticker):
        # Should return [Adj_tuple]
        result = []
        adjs = self.data[self.data[TICKER_FIELD] == ticker]
        for index, row in adjs.iterrows():
            result.append(Adj_tuple(ticker=row[TICKER_FIELD],
                                    div_date=row[DIV_DATE_FIELD],
                                    per_cash=row[PER_CASH_FIELD],
                                    per_share_div_ratio=row[PER_SHARE_DIV_FIELD],
                                    per_share_trans_ratio=row[PER_SHARE_TRANS_FIELD],
                                    allotment_ratio=row[ALLOTMENT_RATIO_FIELD],
                                    allotment_price=row[ALLOTMENT_PRICE_FIELD]))
        return result
