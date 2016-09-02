from pandas.compat import StringIO
import pandas as pd
from tushare.util import vars as vs
from tushare.util.common import Client
from tushare.util import upass as up

# To implement some apis of tushare

client = Client(up.get_token())

MKTADJF = '/api/market/getMktAdjf.csv?secID=%s&ticker=%s&exDivDate=%s&beginDate=%s&endDate=%s&field=%s'

def MktAdjf(secID='', ticker='', exDivDate='', beginDate='', endDate='', field=''):
    # Get the forward adjust factor
    code, result = client.getData(MKTADJF%(secID, ticker, exDivDate, beginDate, endDate, field))
    return _ret_data(code, result)


def _ret_data(code, result):
    if code == 200:
        result = result.decode('utf-8') if vs.PY3 else result
        df = pd.read_csv(StringIO(result))
        return df
    else:
        print(result)
        return None

