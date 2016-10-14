from abc import ABCMeta

from data.persistence.data_portal import (
    DataWriter
)


# Begin of example of multi-extension on DataWriter
class SQLInterface(object):
    __metaclass__ = ABCMeta

class SQLWriter(DataWriter, SQLInterface):
    __metaclass__ = ABCMeta
# End of example of multi-extension on DataWriter