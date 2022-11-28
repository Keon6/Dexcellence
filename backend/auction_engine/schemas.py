import datetime
from decimal import Decimal
from enum import IntEnum
from typing import (
    Deque, Dict, FrozenSet, List, Optional, Sequence, Set, Tuple, Union
)

from pydantic import BaseModel, Field

class BaseEnum(IntEnum):
    @classmethod
    def from_string(cls, other: str) -> 'BaseEnum':
        pass

    @classmethod
    def as_dict(cls) -> dict[str, int]:
        pass


class StrictModel(BaseModel, extra='forbid'):
    @classmethod
    def fields(cls) -> list[str]:
        return list(cls.__fields__.keys())

class AuctionMetadata(StrictModel):
    start_time: datetime.datetime
    end_time: datetime.datetime = None
    order_ids: List[str]
    txn_id: str = None #TODO: should txns be stored per txn or as a single giant Table

    def __getitem__(self, item):
        return getattr(self, item)

class AuctionTableMetadata(StrictModel):
    auction_metadata: List[AuctionMetadata]

    def __getitem__(self, item):
        return getattr(self, item)

class LimitOrder(StrictModel):
    order_id: str
    wallet_id: str
    from_token: str
    to_token: str
    from_token_amount: Decimal
    rate_upper_limit: Decimal = Field(
        description='The upper bound on the clearing price',
    )
    rate_lower_limit: Decimal = Field(
        description='The lower bound on the clearing price',
    )
    sent_timestamp: datetime.datetime
    received_timestamp: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
    )

    class Config:
        orm_mode = True


class Transaction(StrictModel):
    order: LimitOrder
    order_state: str
    from_token: str
    to_token: str
    rate: Decimal
    amount: int
    auction_id: str


class OrderStateEnum(BaseEnum):
    SUBMITTED = 0
    INCOMPLETE = 1
    PARTIAL = 2
    FILLED = 3


class OrderState(StrictModel):
    order_id: str
    state: OrderStateEnum

    class Config:
        orm_mode = True


class ReferenceRate(BaseModel):
    from_token: str
    to_token: str
    amount: int
    rate: Decimal

    def __repr__(self) -> str:
        return f'ReferenceRate({self.rate} {self.to_token}/{self.from_token})'

