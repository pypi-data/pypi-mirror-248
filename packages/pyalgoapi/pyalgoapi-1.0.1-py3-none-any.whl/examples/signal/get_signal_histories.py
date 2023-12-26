from algoapi import AlgoAPI

client = AlgoAPI()
client.set_user_id('230992')
client.register_signal(formula_id=1133)
print(client.get_signal_histories(1133))
client.unsubcribe_signal(formula_id=1133)
