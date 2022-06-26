import datetime
import os
import random
from collections.abc import Generator
from decimal import Decimal

os.chdir('/code')

from auction_engine.one_inch import (
    API as one_inch_api,
    ReferenceRate,
    UnknownTokenError,
)
from auction_engine.schemas import LimitOrder


def generate_limit_orders(
    order_id_generator: Generator[None, None, int],
    wallet_id_generator: Generator[None, None, int],
    from_token: str,
    to_token: str,
    base_rate: ReferenceRate,
    min_amount: int = 1,
    max_amount: int = 1000,
) -> list[LimitOrder]:
    if from_token not in one_inch_api.tokens:
        raise UnknownTokenError(from_token)
    if to_token not in one_inch_api.tokens:
        raise UnknownTokenError(to_token)
    
    rate_pair = (base_rate.from_token, base_rate.to_token)

    match (from_token, to_token):
        case (base_rate.from_token, base_rate.to_token):
            # BUY
            rate = base_rate.rate
        case (base_rate.to_token, base_rate.from_token):
            # SELL
            rate = base_rate.rate**-1
        case _:
            raise ValueError(f'Unrecognized base_rate pair: {rate_pair}') 

    orders = [
        LimitOrder(
            order_id=order_id,
            wallet_id=wallet_id,
            from_token=from_token,
            to_token=to_token,
            from_token_amount=random.randint(min_amount, max_amount),
            sent_timestamp=datetime.datetime.utcnow(),
            rate_upper_limit=Decimal(random.uniform(-0.1, 0.01) + 1) * rate,
            rate_lower_limit=Decimal(random.uniform(-0.2, -0.11) + 1) * rate,
        )
        for order_id, wallet_id, in zip(
            order_id_generator,
            wallet_id_generator,
        )
    ]
    return orders


