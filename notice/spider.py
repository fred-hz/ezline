# coding=utf-8
from bs4 import BeautifulSoup
from calendars.ashare_calendar import AshareCalendar
from collections import namedtuple
from notice import conf
from util.date import date_format
import urllib
import zlib
from notice.data_portal import (
    create_notice_raw_writer,
    create_notice_url_writer
)
from data.data_portal import (
    write_dictlist_to_csv,
    SingleFileWriter
)

class Spider(object):

    def __init__(self):
        pass

    def _check_contain_text(self, tag, texts):
        # Not sure...
        if texts is None:
            return True
        for text in texts:
            if text not in tag.string:
                return False
        return True

    def fetch_url(self, url):
        urlobj =urllib.urlopen(url)
        bytes = urlobj.read()
        text = bytes.decode('gbk')
        #print text
        return text

    def get_attr(self, url, css_attr_list):
        '''
        :param html:
        :param css_attr_list: find attributes for each css. It's a list and
        for every css there's a list of attributes to fetch.
        e.g. [{'css': '', 'attr': ['',''], 'contain_text': ['','']}, ...]
        :return: [{'css': '', attr1: '', attr2: ''}, ...] where attr1 and attr2 are list
        '''
        soup = BeautifulSoup(urllib.urlopen(url).read(), 'lxml')
        result = []
        for css_attr in css_attr_list:
            result_dict_piece = {}
            css = css_attr['css']
            result_dict_piece['css'] = css

            attr_list = css_attr['attr']
            tag_list = soup.select(css)
            for attr in attr_list:
                attr_result = []
                for tag in tag_list:
                    # Needed to be checked
                    if self._check_contain_text(tag, css_attr['contain_text']):
                        attr_result.append(tag.attrs[attr])
                result_dict_piece[attr] = attr_result
            result.append(result_dict_piece)

        return result

    def get_text(self, url, css_list):
        """
        :param url:
        :param css_list: ['', '', ...]
        :return: [{'css': '', 'text': ['','',...]}, ...]
        """
        soup = BeautifulSoup(self.fetch_url(url), 'lxml')
        print soup.get_text()
        result = []
        for css in css_list:
            result_dict_piece = {}
            result_dict_piece['css'] = css

            tag_list = soup.select(css)
            text_result = []
            for tag in tag_list:
                # Needed to be checked
                if tag.string is not None:
                    text_result.append(tag.string)
            result_dict_piece['text'] = text_result

            result.append(result_dict_piece)
        return result



class NoticeCrawler(object):

    def __init__(self):
        self.spider = Spider()
        self.start_date = conf.NOTICE_START_DATE
        self.end_date = conf.NOTICE_END_DATE

        self.url_file_writer = create_notice_url_writer()

    def generate_url_list(self):
        ashare_cal = AshareCalendar()
        opens_list = ashare_cal.get_all_opens(self.start_date, self.end_date)
        return [{'date': date,
                 'url': conf.THS_JIEPAN_URL + '/' + date_format(date, '%Y%m%d') + '/'}
                for date in opens_list]

    def crawl_noon_url(self):
        crawl_url_list = self.generate_url_list()
        result = []
        for pair in crawl_url_list:
            url = pair['url']
            date = pair['date']
            url_list = self.spider.get_attr(url, [{
                'css': '.list-con .arc-title a',
                'attr': ['href'],
                'contain_text': [u'午间重要公告']
            }])
            try:
                result.append({
                    'date': date,
                    'url': url_list[0]['href'][0]})
            except:
                continue

            print result
        self.noon_notice_urls = result
        return result

    def crawl_mourning_url(self):
        crawl_url_list = self.generate_url_list()
        result = []
        for pair in crawl_url_list:
            url = pair['url']
            date = pair['date']
            url_list = self.spider.get_attr(url, [{
                'css': '.list-con .arc-title a',
                'attr': ['href'],
                'contain_text': [u'早盘必读']
            }])
            try:
                result.append({
                    'date': date,
                    'url': url_list[0]['href'][0]})
            except:
                continue

            print result
        self.mourning_notice_urls = result
        return result

    def write_noon_url(self):
        self.url_file_writer.write(self.noon_notice_urls, conf.NOTICE_RAW_URL_NOON_DATA_PATH)

    def write_mourning_url(self):
        self.url_file_writer.write(self.mourning_notice_urls, conf.NOTICE_RAW_URL_MOURNING_DATA_PATH)

if __name__ == '__main__':
    '''nc = NoticeCrawler()
    nc.crawl_mourning_url()
    nc.write_mourning_url()'''

    spider = Spider()
    result = spider.get_text('http://stock.10jqka.com.cn/20151230/c586757777.shtml', ['.atc-content p'])
    result[0]['text'][0] = result[0]['text'][0].encode('GBK')
    print result
    sfw = SingleFileWriter(_write=write_dictlist_to_csv)
    sfw.write(result, conf.NOTICE_COTENT_DATA_PATH)