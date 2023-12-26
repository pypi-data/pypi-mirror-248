from algoapi import AlgoAPI

client = AlgoAPI()
client.set_user_id('230992')
print('Active Signals:', client.get_signals_by_status(active=True))
print('Inactive Signals:', client.get_signals_by_status(active=False))
