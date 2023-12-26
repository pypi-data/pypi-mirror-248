from algoapi import AlgoAPI

client = AlgoAPI()
client.set_user_id('230992')

# run a filter without saving
sec_codes = [
    r['SECURITY_CODE'] for r in client.run_filter(
        filter=[
            {
                'code': 'MC',
                'low': 1000,
                'high': 10000
            }, {
                'code': 'P_PER_MAX_52W',
                'low': 99,
                'high': 100
            }
        ],
        exchange='HOSE',
        industry='',
    )['data']['items']
]

print('Sec codes returned by filter:', sec_codes)
