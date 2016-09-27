from abc import ABCMeta, abstractproperty
import pandas as pd
from config import globals as gs
from .trading_calendar import TradingCalendar
from pandas import DataFrame
from data.file_portal import (
    FileReader,
    ListFileFetcher
)

def create_ashare_cal_reader():
    acr = FileReader(file_path=gs.A_SHARE_TRADING_CALENDAR_PATH,
                     file_fetcher=ListFileFetcher())
    return acr

class AshareCalendar(TradingCalendar):

    def load_open_days(self):
        return create_ashare_cal_reader().read()
