import numpy as np
from time import time
from matching_engine import *

assets = ["BTC", "ETH", "SOL", "1INCH", "DOGE"]
quantities = {"BTC": 1000, "ETH": 1565, "SOL": 420, "1INCH": 3453, "DOGE": 500}

transactions = []

for asset in assets:
    Q = quantities[asset]
    sell_percentages = np.random.dirichlet(np.ones(30), size=None)
    buy_percentages = np.random.dirichlet(np.ones(43), size=None)
    i = 2
    for p in sell_percentages:
        q = -np.multiply(Q, p)
        transactions.append({"wallet": hash(asset)//(i*1e15),
                             "currency_ID": asset, "quantity": q, "timestamp": 0})
        i *= 2

    i = 3
    for p in buy_percentages:
        q = np.multiply(Q, p)
        transactions.append({"wallet": hash(asset)//(i*1e15),
                             "currency_ID": asset, "quantity": q, "timestamp": 0})
        i *= 2

print(transactions)
asset_to_sells, asset_to_buys = process_transactions_per_asset(transactions)

print(asset_to_sells)
print(asset_to_buys)

for asset in assets:
    print("-----", asset, "-----")
    print(asset_to_sells[asset], asset_to_buys[asset])
    sellQ = 0
    for sell in asset_to_sells[asset]:
        sellQ += sell["quantity"]

    buyQ = 0
    for buy in asset_to_buys[asset]:
        buyQ += buy["quantity"]
    print(sellQ + buyQ)


    from_to_2heaps = matching_algo_2heaps(asset_to_sells[asset], asset_to_buys[asset])
    sold_2heaps, bought_2heaps = dict(), dict()
    for ft in from_to_2heaps:
        sold_2heaps[ft["from_wallet"]] = sold_2heaps.get(ft["from_wallet"], 0) + ft["quantity"]
        bought_2heaps[ft["to_wallet"]] = bought_2heaps.get(ft["to_wallet"], 0) + ft["quantity"]

    print(from_to_2heaps)
    print(len(from_to_2heaps))


    from_to_iteration = matching_algo_unordered_list_iteration(asset_to_sells[asset], asset_to_buys[asset])
    sold_iteration, bought_iteration = dict(), dict()
    for ft in from_to_2heaps:
        sold_iteration[ft["from_wallet"]] = sold_iteration.get(ft["from_wallet"], 0) + ft["quantity"]
        bought_iteration[ft["to_wallet"]] = bought_iteration.get(ft["to_wallet"], 0) + ft["quantity"]

    print(from_to_iteration)
    print(len(from_to_iteration))

    assert sold_2heaps == sold_iteration
    assert bought_2heaps == bought_iteration


