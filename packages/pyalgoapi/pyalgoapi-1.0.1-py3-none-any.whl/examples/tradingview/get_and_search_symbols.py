from algoapi import AlgoAPI

client = AlgoAPI()
print('VN30F1M info:', client.get_symbol(symbol='VN30F1M'))
print()
print(
    'Future contracts starting with "VN":',
    client.search_symbols(limit=30, query='VN', type='FUT')
)
