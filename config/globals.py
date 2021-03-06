# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd

SHANGHAI_EXCHANGE = 'XSHG'
SHENZHEN_EXCHANGE = 'XSHE'

PATH_PREFIX = os.path.abspath(os.path.dirname(sys.argv[0]))
DATA_PREFIX = 'D:/ezline/data/basic'

NATURAL_CALENDAR_PATH = DATA_PREFIX + '/natural_cal.csv'
A_SHARE_TRADING_CALENDAR_PATH = DATA_PREFIX + '/ashare_trading_cal.csv'
A_SHARE_STOCKS_PATH = DATA_PREFIX + '/ashare_stocks.csv'
A_SHARE_DAILY_TRADE_PATH = DATA_PREFIX + '/daily_trade.csv'
A_SHARE_STOCKS_ADJUST_PATH = DATA_PREFIX + '/stocks_adj.csv'

DATE_BEGIN_DEFAULT = '2000-01-01'
DATE_END_DEFAULT = '2016-12-31'