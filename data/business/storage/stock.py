from .storage import DataframeStorage
from data.persistence.file_portal import (
    FileReader,
    FileWriter,
    DataframeFileSaver,
    DataframeFileFetcher
)
from pandas import Series
import config.globals as gs
import tushare as ts

ashare_stocks_fields_map = {
    'ticker': 'ticker',
    'secShortName': 'name',
    'exchangeCD': 'exchange',
    'listStatusCD': 'status',
    'listDate': 'list_date'
}


class AShareStocksStorage(DataframeStorage):

    file_writer = FileWriter(gs.A_SHARE_STOCKS_PATH,
                             DataframeFileSaver())

    def __init__(self, data_writer=file_writer, fields_map=ashare_stocks_fields_map):
        super(AShareStocksStorage, self).__init__(data_writer=data_writer,
                                                  fields_map=fields_map)

    def load_data(self):
        mt = ts.Master()
        # Fetch data from tushare
        df = mt.SecID(assetClass='E', field=','.join(self.fields_map.keys()))

        # Change dtype of ticker to string
        ticker_field = self.fields_map.keys()[0]
        df[ticker_field] = df[ticker_field].astype('string')

        # Filter stocks not in Shanghai exchagne and Shenzhen exchange
        exchange_field = self.fields_map.keys()[2]
        df = df[df[exchange_field].isin([gs.SHANGHAI_EXCHANGE, gs.SHENZHEN_EXCHANGE])]

        # Recount index from 1 to len(df) + 1
        df.index = Series(range(1, len(df) + 1))

        self.data = df

