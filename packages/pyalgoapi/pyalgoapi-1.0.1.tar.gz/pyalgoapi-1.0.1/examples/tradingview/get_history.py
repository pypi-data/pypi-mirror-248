import datetime as dt

from algoapi import AlgoAPI
from tests.functional.utils import ts_to_dt

client = AlgoAPI()
resp = client.get_history(
    symbol='VNINDEX',
    resolution='30',
    from_ts=dt.datetime(2023, 10, 16, 7, 0),
    to_ts=dt.datetime(2023, 10, 16, 16, 0),
)
resp['nextTime'] = ts_to_dt(resp['nextTime'])
resp['t'] = [ts_to_dt(ts) for ts in resp['t']]
print(resp)
