from data.stocks import (
    AShareDailyTradeReader
)
import time

A_SHARE_DAILY_TRADE_COLUMNS = frozenset([
    'secID', 'ticker', 'exchangeCD', 'tradeDate', 'preClosePrice',
    'actPreClosePrice', 'openPrice', 'highestPrice', 'lowestPrice',
    'closePrice', 'turnoverVol', 'turnoverValue', 'dealAmount',
    'turnoverRate', 'accumAdjFactor', 'negMarketValue', 'marketValue',
    'PE', 'PE1', 'PB', 'isOpen'
])



class AShareDailyTrade(object):
    def __init__(self):
        self._initialize()

    def _initialize(self):
        time.clock()
        print 'Starting loading daily_trade'
        asdtr = AShareDailyTradeReader()
        self.trade_data = asdtr.read()
        print 'Loading time: ' + str(time.clock())

    def get_spot_value(self, sid, dt, column):
        if column not in A_SHARE_DAILY_TRADE_COLUMNS:
            return None
        print self.trade_data

        print self.trade_data[
            str(self.trade_data['ticker']) == sid]

        print self.trade_data[
            self.trade_data.tradeDate == dt]

        result = self.trade_data[
            (self.trade_data.ticker == sid) &
            (self.trade_data.tradeDate == dt)
        ]['closePrice']
        print result
        result.describe()
        return result