# coding=utf-8
from bs4 import BeautifulSoup
from calendars.ashare_calendar import AshareCalendar
from collections import namedtuple
from notice import conf
from util.date import date_format
import urllib
import zlib

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

    def analyze_noon_notices(self, url):
        text = self.fetch_url(url)
        if text is None:
            return None




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