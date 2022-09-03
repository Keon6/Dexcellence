import requests

<<<<<<< HEAD
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



=======
url = "https://api-eu1.tatum.io/v3/ethereum/smartcontract"


def __invoke_transaction_smart_contract(API_KEY, from_wallet, to_wallet, contract_address, gas_limit, gas_price):
    headers = {
        "Content-Type": "application/json",
        "x-testnet-type": "ethereum-ropsten",
        "x-api-key": API_KEY,
    }
    payload = {
        "contractAddress": contract_address, # TODO,
        "methodName": "transfer",
        "methodABI": {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256"
                }
            ],
            "name": "stake",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        "params": [
            "0x632"
        ],
        "amount": "100000",
        "fromPrivateKey": "0x05e150c73f1920ec14caa1e0b6aa09940899678051a78542840c2668ce5080c2",
        "nonce": 0,
        "fee": {
            "gasLimit": gas_limit,
            "gasPrice": gas_price
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    data = response.json()
    print(data)
>>>>>>> 82d24b17d43118fd259449e0e61f168b965be8d9

