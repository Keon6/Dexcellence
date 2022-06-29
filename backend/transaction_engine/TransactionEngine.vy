# @version 0.3.3

from vyper.interfaces import ERC20, ERC20Detailed

#TODO: Do I need one of these for each token?? Or can I call Token.balanceOf?



struct Transaction:
    from_wallet: indexed(address)
    to_wallet: indexed(address)
    quantity: uint256
    currency: indexed(address)

transactions: DynArray[Transaction, 1024] # TODO: how many transactions to run per contract?

event Transfer:
    _from: indexed(address)
    _to: indexed(address)
    _value: uint256


@external
def __init__(_transactions: Transaction[], _auction_ID: uint256, _auction_time: timestamp):
    self.transactions = _transactions
    self.auction_ID = _auction_ID
    self.auction_time = _auction_time


@view
@internal
def check_balance(_wallet: address, _token: address) -> uint256:
    return _token.balanceOf[_wallet]


@external
def transferFrom(_from: address, _to: address, _quantity: uint256, _token: address) -> bool:
    assert _check_balance(_from, _token) >= _quantity # check if there's enough balance to be transferred
    assert _check_balance(_to, _token) + _quantity >= check_balance(_to, _token) # check for overflow

    return _token.transferFrom(_from, _to)


@external
# TODO: doesn't make sense to check if transaction is valid until the auction finishes running...
def transfer_en_masse():
    # For each transaction that fails
    txn_success_count = 0
    txn_failure_report = []
    for txn in self.transactions:
        try:
            txn_success_count += transferFrom(txn["from_wallet"], txn["to_wallet"], txn["quantity"], txn["currency_ID"])
        except AssertionError:
            txn_failure_report.append({
                "from_wallet": txn["from_wallet"], "to_wallet": txn["to_wallet"],
                "quantity": txn["quantity"], "currency_ID": txn["currency_ID"]
            })
    # TODO: what to return here?