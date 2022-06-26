import requests

# TODO: for now just write TATUM API version. Once done worry about the rest

# free testnet API KEY: 39b60a57-e3b6-4706-ad75-299a589bc2a6
# free mainnet API KEY: 39b60a57-e3b6-4706-ad75-299a589bc2a6


URL = "https://api-eu1.tatum.io/v3/ethereum/transaction"

# TODO: Can I use streaming service like superfluid here?

def __transact_given_set_price_and_quantities(API_key, from_wallet, to_wallet, quantity):
    headers = {
        "Content-Type": "application/json",
        "x-testnet-type": "ethereum-ropsten", #"ethereum-ropsten" "ethereum-rinkeby"
        "x-api-key": API_key
    }

    # TODO: Gas Fee Limits???
    payload = {
        "data": "My note to recipient.",
        "nonce": 0,
        "to": to_wallet,
        "currency": "ETH",
        "fee": {
            "gasLimit": "40000",
            "gasPrice": "20"
        },
        "amount": quantity,
        "fromPrivateKey": from_wallet  # TODO wallet's private key?
    }

    response = requests.post(URL, json=payload, headers=headers)

    data = response.json()
    print(data)




