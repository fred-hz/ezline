from abc import ABCMeta, abstractproperty
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
from data.calendar import NaturalCalReader


class TradingCalendar(with_metaclass(ABCMeta)):
    def __init__(self, begin=gs.DATE_BEGIN_DEFAULT, end=gs.DATE_END_DEFAULT):

        _index_is_open = [1 if date in self.open_days else 0 for date in self.all_days]

        self.schedule = DataFrame(
            index=Index(data=self.all_days, name=gs.DATE_FIELD),
            columns=[gs.MARKET_OPEN_FIELD],
            data={
                gs.MARKET_OPEN_FIELD: _index_is_open
            }
        )

    @property
    def all_days(self):
        ncr = NaturalCalReader()
        _all_days = ncr.read()
        '''_all_days = DataFrame(
            columns=[gs.DATE_FIELD],
            data=all_days_list
        )
        all_days = pd.read_csv(
            filepath_or_buffer=gs.NATURAL_CALENDAR,
            names=[DATE_FIELD]
        )'''
        return _all_days

    @abstractproperty
    def open_days(self):
        """
        A List of open days
        :return:
        """
        return None

    def is_open(self, dt):
        return self.schedule.ix[dt, gs.MARKET_OPEN_FIELD]

    def next_open(self, dt):
        t1 = self.schedule.ix[dt:,:].ix[1:,:]
        t2 = t1[t1[gs.MARKET_OPEN_FIELD] == 1].index.get_values()[0]
        return t2