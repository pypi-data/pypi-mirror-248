import redis
import json
global r

def create_connection():
    global r
    host = "redis-caas-prod-temp.redis.cache.windows.net"
    port = 6380  # Default Redis SSL port
    password = "q6pDnF1CFxJyDwAMgvXm6mJZcRTfTWAJkAzCaAkA9DM="  # Primary or secondary access key
    r = redis.StrictRedis(host=host, port=port, password=password, ssl=True, decode_responses=True)


def persist_value(table,key,value):
    global r
    create_connection()
    r.hset(table,key, json.dumps(value))
    r.connection_pool.disconnect()

def get_by_key(table,key):
    global r
    create_connection()
    value = r.get(f'{table}.{key}')
    r.connection_pool.disconnect()
    return json.loads(value)

def get_table_values(table, key):
    global r
    create_connection()
    value = r.hget(table, key)
    r.connection_pool.disconnect()
    return json.loads(value)


# persist_value('algo_block','1.etl-lake-test',{
#     'app_id':'1',
#     'block-identifier':'etl-lake-test',
#     'repo_creds':{
#         'account_name':'stincreffmsproindev',
#         'file_system_name':'commons',
#         'storage_account_key':'hYeu5xvCGjPi7pCOhwtuvJOcnfpqBBN3QSl1hKMkh+l+WrZUvABZnltS18gf0N7qLLgBoDT53vrq+AStV6MbXA==',
#         'folder_path':'caas-test'
#     },
#     'repo_type':'data_lake',
#     'resource_type':'functions'
# })

