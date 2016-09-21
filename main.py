from calendars.ashare_calendar import AshareCalendar
from data.stocks import AShareStockReader
from data.stocks_adjust import AShareStockAdjWriter, AShareStockAdjReader
from util.date import date_format
from config import globals as gs
import tushare as ts
import pandas as pd
import codecs
from data.calendar import (
    NaturalCalReader,
    NaturalCalWriter,
    AShareTradingCalReader,
    AShareTradingCalWriter
)
from market.daily_trade import AShareDailyTrade
from data.stocks import justify_tickers

def test_calendar():
    ncr = NaturalCalReader()
    print ncr.read()
    acr = AShareTradingCalReader()
    print acr.read()

    asc = AshareCalendar()
    print asc.open_days
    print asc.all_days
    print asc.is_open('2013-03-04')
    print asc.next_open('2013-03-04')

def test_stocks_reader():
    asr = AShareStockReader()
    print asr.read()
    asar = AShareStockAdjReader()
    print asar.read()

def test_stocks_adj():
    asaw = AShareStockAdjWriter()
    print asaw.write()

def test_daily_trade():
    asdt = AShareDailyTrade()
    asdt.get_spot_value('300372', '2014-02-10', 'closePrice')

if __name__ == '__main__':
    justify_tickers()