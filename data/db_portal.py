from data.data_portal import (
    DataWriter
)
from abc import ABCMeta, abstractproperty, abstractmethod
import pandas as pd
import codecs
import csv

# Begin of example of multi-extension on DataWriter
class SQLInterface(object):
    __metaclass__ = ABCMeta

class SQLWriter(DataWriter, SQLInterface):
    __metaclass__ = ABCMeta
# End of example of multi-extension on DataWriter