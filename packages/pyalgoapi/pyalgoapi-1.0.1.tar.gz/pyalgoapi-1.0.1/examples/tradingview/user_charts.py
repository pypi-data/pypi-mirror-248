from algoapi import AlgoAPI
from tests.functional.utils import ts_to_dt

client = AlgoAPI()
# Original charts
resp = client.get_user_charts(client='test', user=1)
for chart in resp['data']:
    chart['timestamp'] = ts_to_dt(chart['timestamp'])
print('Original charts:', resp)

if len(resp['data']) == 0:
    next_id = 1
else:
    next_id = resp['data'][-1]['id'] + 1

# Add a chart
client.add_user_chart(
    client='test',
    user=1,
    name=f'bscalgo{next_id}',
    content='1',
    symbol='HPG',
    resolution='D',
)

resp = client.get_user_charts(client='test', user=1)
for chart in resp['data']:
    chart['timestamp'] = ts_to_dt(chart['timestamp'])
print('Charts after adding:', resp)

# Remove chart by ID
client.delete_user_chart(client='test', user=1, chart=next_id)
resp = client.get_user_charts(client='test', user=1)
for chart in resp['data']:
    chart['timestamp'] = ts_to_dt(chart['timestamp'])
print('Charts left after removing:', resp)
