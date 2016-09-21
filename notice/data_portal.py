from data.data_portal import (
    DataReader,
    DataWriter,
    read_csv_to_dictlist,
    write_dictlist_to_csv
)
import conf

class NoticeDataWriter(DataWriter):

    def __init__(self, _write=write_dictlist_to_csv()):
        super(NoticeDataWriter, self).__init__(_write)

    def file_path(self):
        pass