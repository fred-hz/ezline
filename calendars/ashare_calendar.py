from abc import ABCMeta, abstractproperty
import pandas as pd
from config import globals as gs
from .trading_calendar import TradingCalendar
from data.calendar import AShareTradingCalReader
from pandas import DataFrame

class AshareCalendar(TradingCalendar):

    @property
    def open_days(self):
        acr = AShareTradingCalReader()
        opens = acr.read()
        '''opens = DataFrame(
            columns=[gs.MARKET_OPEN_FIELD],
            data=open_list
        )
        opens = pd.read_csv(
            filepath_or_buffer=gs.A_SHARE_TRADING_CALENDAR,
            names=['date']
        )'''
        return opens