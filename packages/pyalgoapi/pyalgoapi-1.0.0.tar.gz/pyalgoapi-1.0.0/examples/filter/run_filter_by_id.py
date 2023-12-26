from algoapi import AlgoAPI

client = AlgoAPI()
client.set_user_id('230992')
sec_codes = [
    r['SECURITY_CODE'] for r in client.run_filter_by_id('2353')['data']['items']
]

print('Sec codes returned by filter:', sec_codes)
