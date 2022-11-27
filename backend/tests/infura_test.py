import requests


proj_id = "2HW9bLC9orMwRorClkGVXDOKqOR"

api_key_secret = "0e1325ec0037917ac402612b9c55771a"

http_endpoint = "https://2HW9bLC9orMwRorClkGVXDOKqOR:0e1325ec0037917ac402612b9c55771a@filecoin.infura.io"
wss_endpoint = "wss://2HW9bLC9orMwRorClkGVXDOKqOR:0e1325ec0037917ac402612b9c55771a@filecoin.infura.io"

# curl -X POST -H "Content-Type: application/json" \
#   --user <PROJECT_ID>:<PROJECT_SECRET> \
#   --url https://<PROJECT_ID>:<PROJECT_SECRET>@filecoin.infura.io \
#   --data '{ "id": 0, "jsonrpc": "2.0", "method": "Filecoin.ChainHead", "params": [] }'


# requests.post(http_endpoint, data="hello.csv", params={
#     "user": "{}:{}".format(proj_id, api_key_secret)
#     })

requests.get(
    http_
)