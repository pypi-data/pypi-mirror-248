from algoapi import AlgoAPI

client = AlgoAPI()
client.set_user_id('230992')

# get all filter_id pre-add
ori_filter_ids = [str(f['FilterId']) for f in client.get_all_filters()['data']]
print('Original filter_ids:', ori_filter_ids)

# run and save a filter to initiate
client.create_filter(
    filter=[
        {
            'code': 'MC',
            'low': 100,
            'high': 496311
        }, {
            'code': 'P_PER_MAX_52W',
            'low': 99,
            'high': 100
        }
    ],
    exchange='',
    industry='',
    name='TEST'
)

# get all filter_id pre-delete
filter_ids = [str(f['FilterId']) for f in client.get_all_filters()['data']]
print('Post-adding new filter:', filter_ids)

# try update filter params
selected_id = filter_ids[-1]
print(
    f'Pre-update filter w/ id {selected_id}:',
    client.get_filter_by_id(filter_id=selected_id)
)

client.update_filter(
    filter_id=selected_id,
    filter=[
        {
            'code': 'MC',
            'low': 100,
            'high': 1000
        }, {
            'code': 'P_PER_MAX_52W',
            'low': 95,
            'high': 100
        }
    ],
    exchange='HOSE',
    industry='',
    name='RENAMEDTEST',
)

print(
    f'Post-update filter w/ id {selected_id}:',
    client.get_filter_by_id(filter_id=selected_id)
)

# delete filter_id just added for testing
client.delete_filter(filter_id=selected_id)

# get all filter_id post-delete
filter_ids = [str(f['FilterId']) for f in client.get_all_filters()['data']]
print(f'Post-deleting filter w/ id {selected_id}:', filter_ids)
