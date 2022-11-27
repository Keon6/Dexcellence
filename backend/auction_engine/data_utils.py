import pandas as pd
import requests
import os
import collections

# TODO: Still need to figure out how to upload data from the OMS.
# there's not a whole lot of documentation besides uploading content using Infura UI

def add_new_order_requests(endpoint: str, proj_id: str, api_secret: str, data_file_path: str) -> str:
    """
    Do this only once per auction 
    :param endpoint - string of endpoint for Infura IPFS
    :param proj_id - str for the INFURA IPFS project ID
    :param api_secret - str for the INFURA IPFS secret API key
    :param data_file_path - str for the file path to store the data on
    return auction_id as hash of the order table
    """
    # curl -X POST -F file=@{data_file_path}
    # -u "{proj_id}:{api_secret}" 
    # "{endpoint}api/v0/add"

    files = {
        'file': open(data_file_path, 'rb'),
    }
    response = requests.post(endpoint + '/api/v0/add', files=files, auth=(proj_id, api_secret))

    if response.status_code != 200:
        raise IOError("Request to add order to IPFS has ended up in RESPONSE:[{}]".format(response.status_code))
    
    os.system("rm {}".format(data_file_path))
    auction_id = response.text.split(",")[1].split(":")[1].replace('"','')
    return auction_id

def get_auction_orders(auction_id, endpoint: str, proj_id: str, api_secret: str) -> pd.DataFrame:
    """
    :param auction_id - string of current hash of the IPFS CID of current orders
    :param endpoint - string of endpoint for Infura IPFS
    :param proj_id - str for the INFURA IPFS project ID
    :param api_secret - str for the INFURA IPFS secret API key
    return 
    """
    params = {
        'arg': auction_id
    }
    response = requests.post(endpoint + '/api/v0/cat', params=params, auth=(proj_id, api_secret))
    if response.status_code != 200:
        raise IOError("Request to add order to IPFS has ended up in RESPONSE:[{}]".format(response.status_code))

    # TODO: should this be in Dataframe vs Pydantic ?
    # return pd.DataFrame.from_records(
    #     json.loads(response.text)
    # ) 

    # return LimitOrder.parse_obj(response.json())
    return pd.DataFrame.from_records(response.json())

def get_transactions(transaction_table_id, endpoint: str, proj_id: str, api_secret: str) -> pd.DataFrame:
    """
    :param transaction_table_id - string of current hash of the IPFS CID of txns
    :param endpoint - string of endpoint for Infura IPFS
    :param proj_id - str for the INFURA IPFS project ID
    :param api_secret - str for the INFURA IPFS secret API key
    return 
    """
    params = {
        'arg': transaction_table_id
    }
    response = requests.post(endpoint + '/api/v0/cat', params=params, auth=(proj_id, api_secret))
    if response.status_code != 200:
        raise IOError("Request to add order to IPFS has ended up in RESPONSE:[{}]".format(response.status_code))

    return pd.DataFrame.from_records(response.json())


# TODO: where should I keep the info on (time:auction_id)
def get_historical_orders(start_time, end_time, time_to_auction_id, endpoint, proj_id, api_secret):
    df = []
    for time, auction_id in time_to_auction_id.items():
        if start_time <= time and time <= end_time:
            df_time = get_auction_orders(auction_id, endpoint, proj_id, api_secret)
            df_time["time"] = time
            df.append(df_time)
    return pd.concat(df)

# TODO: Does it make sense to store all txns in 1 place? vs. txn table per auction?
# TODO: How will auctio nengine output txns & how will on-chain txns be executed?
def get_historical_transactions(start_time, end_time, txn_table_id, endpoint, proj_id, api_secret):
    # IF all in 1 table:
    df_txn = get_transactions(txn_table_id, endpoint, proj_id, api_secret)
    return df_txn[(df_txn["time"]>=end_time) & (df_txn["time"]<=end_time)]
    pass
