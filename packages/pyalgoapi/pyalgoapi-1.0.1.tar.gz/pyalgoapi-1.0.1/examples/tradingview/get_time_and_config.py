from algoapi import AlgoAPI
from tests.functional.utils import ts_to_dt

client = AlgoAPI()
print('Server time:', ts_to_dt(client.get_time()))
print()
print('Config:', client.get_config())
