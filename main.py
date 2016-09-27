# coding=utf-8
import notice.conf as nconf
from calendars.ashare_calendar import AshareCalendar
import tushare as ts
from bs4 import BeautifulSoup
import re

from data.file_portal import (
    FileReader,
    FileWriter,
    DataframeFileFetcher
)
from data.stocks import (
    AShareStocksWriter,
    AShareStocks
)
from notice.analyze import NoticeAnalyzer

def test_calendar():
    ac = AshareCalendar()
    print ac.open_days

def test_stocks_reader():
    pass

def test_stocks_adj():
    pass

def test_daily_trade():
    pass

def test_stocks_file_interface():
    #sw = AShareStocksWriter()
    #sw.write()
    sr = AShareStocks()
    print sr.get_ticker_by_name('全新好')
    print sr.get_name_by_ticker('000001')
    for name in sr.get_all_tickers_name():
        print name

def test_notice_analyzer():
    noon_url_reader = FileReader(file_path=nconf.NOTICE_RAW_URL_NOON_DATA_PATH,
                                 file_fetcher=DataframeFileFetcher())
    noon_df = noon_url_reader.read()
    noon_date = noon_df['date'].tolist()
    noon_url = noon_df['url'].tolist()
    noon_pairs = zip(noon_date, noon_url)

    mourning_url_reader = FileReader(file_path=nconf.NOTICE_RAW_URL_MOURNING_DATA_PATH,
                                 file_fetcher=DataframeFileFetcher())
    mourning_df = mourning_url_reader.read()
    mourning_date = mourning_df['date'].tolist()
    mourning_url = mourning_df['url'].tolist()
    mourning_pairs = zip(mourning_date, mourning_url)

    na = NoticeAnalyzer(mourning_pairs, noon_pairs)
    na.analyze()
    na.read_noon_notice()

if __name__ == '__main__':
    test_notice_analyzer()