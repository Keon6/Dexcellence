import pandas as pd
import requests
import os
import json
import collections
from datetime import datetime
from schemas import AuctionMetadata, AuctionTableMetadata
import aiohttp, asyncio

temp_path = "/Users/keonshikkim/Documents/Dexcellence-1/backend/temp/"

# TODO: Still need to figure out how to upload data from the OMS.
# there's not a whole lot of documentation besides uploading content using Infura UI


def _upload_new_data_to_IPFS(endpoint: str, proj_id: str, api_secret: str, data_file_path: str) -> requests.Response:
    """
    simply add new file to IPFS and return its hash
    """
    files = {
        'file': open(data_file_path, 'rb'),
    }
    response = requests.post(endpoint + '/api/v0/add', files=files, auth=(proj_id, api_secret))

    if response.status_code != 200:
        raise IOError("Request to add new file {} to IPFS has ended up in RESPONSE:[{}]".format(data_file_path, response.status_code))
    
    os.system("rm {}".format(data_file_path))
    # _upload_new_data_to_IPFS.counter += 1
    return response
    

def _retrieve_data_from_IPFS(cid_hash, endpoint, proj_id, api_secret) -> requests.Response:
    """
    Return a particular data stored on IPFS
    """
    response = requests.post(
        endpoint + '/api/v0/cat', 
        params={'arg': cid_hash}, 
        auth=(proj_id, api_secret)
    )

    if response.status_code != 200:
        raise IOError(
            "Issue retrieving the file of the following CID from IPFS | RESPONSE:[{}]".format(cid_hash, response.status_code)
            )

    # _retrieve_data_from_IPFS.counter += 1

    return response

def _get_IPFS_cid_from_response(response):
    return response.text.split(",")[1].split(":")[1].replace('"','')

def create_new_auction(auction_metadata_hash, endpoint, proj_id, api_secret) -> str:
    # TODO: How do we deal with orders that come in btw previous auction end and before new 
    #   auction metadata hash has been communicated to everyone (all OMS clients)

    if auction_metadata_hash is not None:
        auction_metadata_response = _retrieve_data_from_IPFS(auction_metadata_hash, endpoint, proj_id, api_secret)
        current_CID = _get_IPFS_cid_from_response(auction_metadata_response)
        # remove old table
        requests.post(endpoint + '/api/v0/pin/rm', params={'arg': current_CID}, auth=(proj_id, api_secret))
        
        auction_metadata = auction_metadata_response.json()
        if type(auction_metadata) is str:
            auction_metadata = json.loads(auction_metadata)
        del auction_metadata_response
    else: # Create from scratch!
        auction_metadata = AuctionTableMetadata(auction_metadata=[])
        
    new_auction_meta = AuctionMetadata(start_time=datetime.now(), order_ids=[]) # TODO: is this necessary to pydantically do this?
    auction_metadata["auction_metadata"].append(new_auction_meta)

    # Re-add new metadata to IPFS
    with open(temp_path + "temp_auction_metadata.json", "w") as outfile:
        json.dump(auction_metadata.json(), outfile)

    response = _upload_new_data_to_IPFS(endpoint, proj_id, api_secret, data_file_path=temp_path+"temp_auction_metadata.json")
    return _get_IPFS_cid_from_response(response) # return CID of the newly updated auction_metadata


def add_new_order(auction_metadata_hash, endpoint: str, proj_id: str, api_secret: str, data_file_path: str) -> str:
    """
    Do this only once per auction 
    :param endpoint - string of endpoint for Infura IPFS
    :param proj_id - str for the INFURA IPFS project ID
    :param api_secret - str for the INFURA IPFS secret API key
    :param data_file_path - str for the file path to store the data on
    return auction_id as hash of the order table
    """
    # First add the order to IPFS and retrieve its hash

    # in cURL...
    # curl -X POST -F file=@{data_file_path}
    # -u "{proj_id}:{api_secret}" 
    # "{endpoint}api/v0/add"

    order_id = _get_IPFS_cid_from_response(
        _upload_new_data_to_IPFS(endpoint, proj_id, api_secret, data_file_path)
    )
    
    # Second, update auction metadata by adding the new order
    auction_metadata_response = _retrieve_data_from_IPFS(auction_metadata_hash, endpoint, proj_id, api_secret)
    current_CID = _get_IPFS_cid_from_response(auction_metadata_response) 
    # remove old table
    requests.post(endpoint + '/api/v0/pin/rm', params={'arg': current_CID}, auth=(proj_id, api_secret))

    auction_metadata = auction_metadata_response.json()
    if type(auction_metadata) == str:
        auction_metadata = json.loads(auction_metadata)
    del auction_metadata_response

    auction_metadata["auction_metadata"][-1]["order_ids"].append(order_id)
    
    # 3rd, Re-add new metadata to IPFS
    with open(temp_path + "temp_auction_metadata.json", "w") as outfile:
        json.dump(auction_metadata, outfile)
    return order_id, _get_IPFS_cid_from_response(
        _upload_new_data_to_IPFS(endpoint, proj_id, api_secret, data_file_path=temp_path+"temp_auction_metadata.json")
    )

##################### These are really to be used by the auction engine

async def _retrieve_data_from_IPFS_parallel(cid_hash, endpoint, proj_id, api_secret, session) -> requests.Response:
    """
    Return a particular data stored on IPFS
    """
    async with session.post(url=endpoint + '/api/v0/cat', params={'arg': cid_hash}, auth=(proj_id, api_secret)) as response:
        # _retrieve_data_from_IPFS_parallel.counter += 1
        if response.status_code != 200:
            raise IOError(
                "Issue retrieving the file of the following CID from IPFS | RESPONSE:[{}]".format(cid_hash, response.status_code)
                )
        else:
            return response

# TODO: dedug
async def get_auction_orders(auction_metadata_hash, endpoint: str, proj_id: str, api_secret: str) -> pd.DataFrame:
    """
    :param auction_id - string of current hash of the IPFS CID of current orders
    :param endpoint - string of endpoint for Infura IPFS
    :param proj_id - str for the INFURA IPFS project ID
    :param api_secret - str for the INFURA IPFS secret API key
    return 
    """
    # Get auction metadata
    auction_metadata_response = _retrieve_data_from_IPFS(auction_metadata_hash, endpoint, proj_id, api_secret)
    current_CID = _get_IPFS_cid_from_response(auction_metadata_response)
    # remove old table
    requests.post(endpoint + '/api/v0/pin/rm', params={'arg': current_CID}, auth=(proj_id, api_secret))

    auction_metadata = auction_metadata_response.json()
    if type(auction_metadata) is str:
        auction_metadata = json.loads(auction_metadata)
    del auction_metadata_response

    # Get the orders!
    async with aiohttp.ClientSession() as session:
        responses = await asyncio.gather(
            *[_retrieve_data_from_IPFS_parallel(auction_id, endpoint, proj_id, api_secret, session) for auction_id in auction_metadata["auction_metadata"][-1]["order_ids"]]
        )
        print(responses)

# TODO: test & debug
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

########################### The below are to be used by data API endpoints

# TODO: fix so that you could just use auction_metadata
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
