import requests
import sys
sys.path.append("/Users/keonshikkim/Documents/Dexcellence-1/backend/auction_engine/")
from data_utils import *

proj_id = "2HQaxQAcNTEPFTFnn76bMTkynZc"
api_key_secret = "e70d7b11311acfbaf4da4d4d2fc70749"
endpoint = "https://ipfs.infura.io:5001"



print("---- new auction !")
auction_metadata_cid = create_new_auction(None, endpoint, proj_id, api_key_secret)
print(auction_metadata_cid)

print("---- retrieve auction metadata !")
response = requests.post(
        endpoint + '/api/v0/cat', 
        params={'arg': auction_metadata_cid}, 
        auth=(proj_id, api_key_secret),
        headers={'content-type': "application/json", 'cache-control': "no-cache", 'postman-token': "c71c65a6-07f4-a2a4-a6f8-dca3fd706a7a"}
    )
print(response.status_code)
print(response.json(), type(response.json()))

print("---- store orders!")
o1_id, auction_metadata_cid = add_new_order(auction_metadata_cid, endpoint, proj_id, api_key_secret, "order1.json")
o2_id, auction_metadata_cid = add_new_order(auction_metadata_cid, endpoint, proj_id, api_key_secret, "order2.json")
print(o1_id, o2_id, auction_metadata_cid)

response = requests.post(
        endpoint + '/api/v0/cat', 
        params={'arg': auction_metadata_cid}, 
        auth=(proj_id, api_key_secret),
        headers={'content-type': "application/json", 'cache-control': "no-cache", 'postman-token': "c71c65a6-07f4-a2a4-a6f8-dca3fd706a7a"}
    )
print(response.status_code)
print(response.json(), type(response.json()))


# 
print("----- get_auction_orders")
async def main():
    a = await get_auction_orders(auction_metadata_cid, endpoint, proj_id, api_key_secret)

import asyncio
asyncio.run(main())