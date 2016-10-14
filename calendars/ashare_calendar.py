from config import globals as gs
from data.persistence.file_portal import (
    FileReader,
    ListFileFetcher
)
from .trading_calendar import TradingCalendar


def create_ashare_cal_reader():
    acr = FileReader(file_path=gs.A_SHARE_TRADING_CALENDAR_PATH,
                     file_fetcher=ListFileFetcher())
    return acr

class AshareCalendar(TradingCalendar):

    def load_open_days(self):
        return create_ashare_cal_reader().read()
