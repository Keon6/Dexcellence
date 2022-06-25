from queue import PriorityQueue
from time import time

#TODO: key names - coordinate with auction engine


def process_transactions_per_asset(transactions: list):
    """

    :param transactions: List of Transactions , where transaction = {wallet, currency_ID, quantity, timestamp}
    :return:
    """
    asset_to_sells = dict()
    asset_to_buys = dict()

    for txn in transactions:
        currency_ID = txn["currency_ID"]
        quantity = txn["quantity"]
        # negative numbers are sell orders
        if quantity < 0:
            try:
                asset_to_sells[currency_ID].append(txn)
            except KeyError:
                asset_to_sells[currency_ID] = [txn]
        else:
            try:
                asset_to_buys[currency_ID].append(txn)
            except KeyError:
                asset_to_buys[currency_ID] = [txn]

    return asset_to_sells, asset_to_buys


def matching_algo_2heaps(sells_per_asset: list, buys_per_asset: list):
    """
    O(nlogn) algo
    :param sells_per_asset:
    :param buys_per_asset:
    :return: from_to = list of dictionary with fields {from_wallet, to_wallet, quantity, currency_ID}
    """
    # currency:
    currency_ID = sells_per_asset[0]["currency_ID"]

    # Create Min Heap of Sell Orders

    sell_queue = PriorityQueue()
    for sell_order in sells_per_asset:
        sell_queue.put((sell_order["quantity"], sell_order["wallet"]))


    # Create Max Heap of Buy Orders
    buy_queue = PriorityQueue()
    for buy_order in buys_per_asset:
        buy_queue.put((-1*buy_order["quantity"], buy_order["wallet"]))

    # Identify transactions
    from_to = []
    while sell_queue.empty() is not True and buy_queue.empty() is not True:
        sell_quantity, from_wallet = sell_queue.get()
        buy_quantity, to_wallet = buy_queue.get()

        # if demand_surplus > 0 then the buy order was not totally cleared and will be put back to the queue
        # if demand_surplus <0 then the sell order was not totally cleared and will be put back to the queue
        # if demand_surplus == 0, then all good!
        demand_surplus = sell_quantity - buy_quantity
        if demand_surplus > 0: # demand shortage
            buy_queue.put((-demand_surplus, to_wallet))
            txn_quantity = -1*sell_quantity
        elif demand_surplus < 0: # supply surplus
            sell_queue.put((demand_surplus, from_wallet))
            txn_quantity = -1*buy_quantity
        else:
            pass
            txn_quantity = -1*buy_quantity
        from_to.append({"from_wallet": from_wallet, "to_wallet": to_wallet,
                        "quantity": txn_quantity, "currency_ID": currency_ID})

    return from_to


def matching_algo_unordered_list_iteration(sells_per_asset: list, buys_per_asset: list):
    """
    O(n) Algo
    :param sells_per_asset:
    :param buys_per_asset:
    :return: from_to = list of dictionary with fields {from_wallet, to_wallet, quantity, currency_ID}
    """

    currency_ID = sells_per_asset[0]["currency_ID"]
    from_to = []
    si, bi = 0, 0

    while si < len(sells_per_asset) and bi < len(buys_per_asset):
        sell_order = sells_per_asset[si]
        sell_quantity, from_wallet = sell_order["quantity"], sell_order["wallet"]

        buy_order = buys_per_asset[bi]
        buy_quantity, to_wallet = buy_order["quantity"], buy_order["wallet"]

        # IF current supply hasn't been fulfilled, then move to the next one
        demand_surplus = buy_quantity + sell_quantity

        if demand_surplus > 0:  # Current buy order hasn't cleared yet
            buys_per_asset[bi]["quantity"] = demand_surplus
            txn_quantity = -sell_quantity
            si += 1

        elif demand_surplus < 0:  # Not all sell orders are cleared
            sells_per_asset[si]["quantity"] = demand_surplus
            txn_quantity = buy_quantity
            bi += 1

        else:  # supply = demand!
            txn_quantity = buy_quantity
            si += 1
            bi += 1
        from_to.append({"from_wallet": from_wallet, "to_wallet": to_wallet,
                        "quantity": txn_quantity, "currency_ID": currency_ID})

    return from_to
