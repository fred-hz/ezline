from .fetch import DataFetch
from data.persistence.file_portal import (
    FileReader,
    FileWriter,
    DataframeFileSaver,
    DataframeFileFetcher
)
from data.business.storage.stock import (
    ashare_stocks_fields_map
)
import config.globals as gs


class AShareStockFetch(DataFetch):

    file_reader = FileReader(gs.A_SHARE_STOCKS_PATH,
                             DataframeFileFetcher())

    def __init__(self, data_reader):
        super(AShareStockFetch, self).__init__(data_reader=data_reader)
        columns = ashare_stocks_fields_map.values()
        for column in columns:
            setattr(self, column, column)

            # self.ticker_field = columns[0]
        # self.name_field = columns[1]
        # self.exchange_field = columns[2]
        # self.status_field = columns[3]
        # self.list_date_field = columns[4]

    def