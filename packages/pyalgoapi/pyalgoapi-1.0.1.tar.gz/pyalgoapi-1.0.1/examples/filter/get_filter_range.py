from algoapi import AlgoAPI

client = AlgoAPI()
[print(f) for f in client.get_filter_range()['data']]
