# @version 0.3.3


from vyper.interfaces import ERC20


from_wallet: public(address)
to_wallet: public(address)

event Transfer:
    amount: uint256
    sender: indexed(address)
    receiver: indexed(address)

event Buy:
    buyer: indexed(address)
    buy_order: uint256

event Sell:
    seller: indexed(address)
    sell_order: uint256


@external
def __init__(_from_wallet: address, _to_wallet: address, _transfer_amount: uint256, _transfer_asset: address):
    self.from_wallet = _from_wallet
    self.to_wallet = _to_wallet
    self.transfer_amount = _transfer_amount
    self.transfer_asset = _transfer_asset


@view
@internal
def _check_balance() -> uint256:
    return self.from_wallet[]
