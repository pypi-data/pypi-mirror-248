from algoapi import AlgoAPI

client = AlgoAPI()
client.set_user_id('230992')

active_signals = client.get_signals_by_status(active=True)
print('Original active signals:', active_signals)

# Register formula
client.register_signal(formula_id=1133)
active_signals = client.get_signals_by_status(active=True)
print('Activated new formula:', active_signals)

# Unsub formula
client.unsubcribe_signal(formula_id=1133)
active_signals = client.get_signals_by_status(active=True)
print('Deactivated just-added formula:', active_signals)
