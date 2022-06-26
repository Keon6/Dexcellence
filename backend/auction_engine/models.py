import datetime
from decimal import Decimal
from enum import IntEnum

from pydantic import BaseModel


class BaseEnum(IntEnum):
    @classmethod
    def from_string(cls, other: str) -> 'BaseEnum':
        pass

    @classmethod
    def as_dict(cls) -> dict[str, int]:
        pass


class StrictModel(BaseModel, extra='forbid'):
    pass


class BaseOrder(StrictModel):
    order_id: str
    wallet_id: str
    from_token: str
    to_token: str
    from_token_amount: int
    sent_timestamp: datetime.datetime


class LimitOrder(BaseOrder):
    rate_upper_limit: Decimal
    rate_lower_limit: Decimal


class Transaction(StrictModel):
    order: BaseOrder
    order_state: str
    from_token: str
    to_token: str
    rate: Decimal
    amount: int
    auction_id: str


class OrderStateEnum(BaseEnum):
    SUBMITTED = 0
    INCOMPLETE = 1
    FILLED = 2


class OrderState(StrictModel):
    order_id: str
    state: OrderStateEnum


class ReferenceRate(BaseModel):
    from_token: str
    to_token: str
    amount: int
    rate: Decimal

    def __repr__(self) -> str:
        return f'ReferenceRate({self.rate} {self.to_token}/{self.from_token})'

