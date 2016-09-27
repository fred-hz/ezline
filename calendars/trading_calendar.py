from abc import ABCMeta, abstractproperty, abstractmethod
import numpy as np
import pandas as pd
from six import with_metaclass
from config import globals as gs
from pandas import (
    DataFrame,
    Index,
    date_range,
    DatetimeIndex,
    DateOffset
)
from data.file_portal import (
    FileReader,
    ListFileFetcher
)

def create_natural_cal_reader():
    ncr = FileReader(file_path=gs.NATURAL_CALENDAR_PATH,
                     file_fetcher=ListFileFetcher())
    return ncr

class TradingCalendar(with_metaclass(ABCMeta)):
    def __init__(self, begin=gs.DATE_BEGIN_DEFAULT, end=gs.DATE_END_DEFAULT):

        self.all_days = self.load_all_days()
        self.open_days = self.load_open_days()

        _index_is_open = [1 if date in self.open_days else 0 for date in self.all_days]

        self.schedule = DataFrame(
            index=Index(data=self.all_days, name=gs.DATE_FIELD),
            columns=[gs.MARKET_OPEN_FIELD],
            data={
                gs.MARKET_OPEN_FIELD: _index_is_open
            }
        )

    def load_all_days(self):
        return create_natural_cal_reader().read()

    @abstractmethod
    def load_open_days(self):
        raise NotImplementedError

    def is_open(self, dt):
        return self.schedule.ix[dt, gs.MARKET_OPEN_FIELD]

    def next_open(self, dt):
        t1 = self.schedule.ix[dt:,:].ix[1:,:]
        t2 = t1[t1[gs.MARKET_OPEN_FIELD] == 1].index.get_values()[0]
        return t2

    def get_all_opens(self, start_dt, end_dt):
        result = []
        if self.is_open(start_dt):
            result.append(start_dt)
        next_open = self.next_open(start_dt)
        while next_open <= end_dt:
            result.append(next_open)
            next_open = self.next_open(next_open)
        return result
