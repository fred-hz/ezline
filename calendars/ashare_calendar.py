from abc import ABCMeta, abstractproperty
import pandas as pd
from config import globals as gs
from .trading_calendar import TradingCalendar
from data.calendar import AShareTradingCalReader
from pandas import DataFrame

class AshareCalendar(TradingCalendar):

    def load_open_days(self):
        acr = AShareTradingCalReader()
        opens = acr.read()
        return opens
