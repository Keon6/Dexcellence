import requests

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

# TODO: for now just write TATUM API version