# coding=utf-8
from bs4 import BeautifulSoup
from calendars.ashare_calendar import AshareCalendar
from collections import namedtuple
from notice import conf
from util.date import date_format
import urllib
import zlib
from config import globals as gs
import pandas as pd
import numpy as np
from data.stocks import (
    AShareStocks,
    TICKER_FIELD,
    NAME_FIELD
)
from data.file_portal import (
    FileWriter,
    DataframeFileSaver,
    FileReader,
    DataframeFileFetcher
)

class NoticeAnalyzer(object):

    def __init__(self, mourning_url_list, noon_url_list):
        # url_list: [(date, url), ...]
        self.mourning_urls = mourning_url_list
        self.noon_urls = noon_url_list
        self.ashare_stocks = AShareStocks()

    def fetch_url(self, url):
        urlobj =urllib.urlopen(url)
        bytes = urlobj.read()
        text = bytes.decode('gbk')
        #print text
        return text

    def find_ticker_from_text(self, text):
        names = self.ashare_stocks.get_all_tickers_name()
        for name in names:
            if name in text:
                sid = self.ashare_stocks.get_ticker_by_name(name)
                return sid, name
        return None, None


    def analyze_noon_content(self, soup):
        # Returns [{'title': '', 'content': ''}, ...]
        tags = soup.select('.atc-content p')
        # Ignore useless tag
        tags = [tag for tag in tags if tag.get('id') is None or 'yuanchuang-tuiguang' in tag.get('id')]

        # <strong> means a title.
        titles_index = []
        for i in range(0, len(tags)):
            if tags[i].strong is not None:
                titles_index.append(i)

        result = []
        for i in range(0, len(titles_index)-1):
            content_begin = titles_index[i] + 1
            content_end = titles_index[i+1] - 1
            title = tags[titles_index[i]].get_text()
            content = ''
            for j in range(content_begin, content_end+1):
                if tags[j].get_text() is not None:
                    content += tags[j].get_text()
            if content is not None and content != '':
                result.append({'title': title.strip(),
                               'content': content.strip()})
        return result

    def analyze_noon_notices(self, url):
        # should return [(sid, name, title, text), ...]
        text = self.fetch_url(url)
        if text is None:
            return None

        soup = BeautifulSoup(text, 'lxml')
        title_content = self.analyze_noon_content(soup)
        result = []
        for item in title_content:
            sid, name = self.find_ticker_from_text(item['title'])
            if sid is not None and name is not None:
                result.append((sid, name, item['title'], item['content']))
        return result

    def analyze_mourning_notice(self, url):
        pass

    def analyze(self):
        print self.noon_urls
        data_list = []
        for raw_data in self.noon_urls:
            date = raw_data[0]
            url = raw_data[1]
            tuple_list = self.analyze_noon_notices(url)
            for item_tuple in tuple_list:
                data_item = [date, item_tuple[0], item_tuple[1], item_tuple[2], item_tuple[3]]
                data_list.append(data_item)

        dtypes = np.dtype([('date', 'string'),
                           ('sid', 'string'),
                           ('name', 'string'),
                           ('title', 'string'),
                           ('content', 'string')])
        df = pd.DataFrame(data=data_list,
                          columns=['date', 'sid', 'name', 'title', 'content'],
                          dtype='string')
        print df

        notice_writer = FileWriter(file_path=conf.NOTICE_NOON_DATA_PATH,
                                   file_saver=DataframeFileSaver())
        notice_writer.write(df)

    def read_noon_notice(self):
        notice_reader = FileReader(file_path=conf.NOTICE_NOON_DATA_PATH,
                                   file_fetcher=DataframeFileFetcher())
        print notice_reader.read()