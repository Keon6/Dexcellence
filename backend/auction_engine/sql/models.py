from sqlalchemy import (
    Enum,
    Column,
    DateTime,
    DECIMAL,
    Integer,
    String,
)

from auction_engine.schemas import OrderStateEnum
from auction_engine.sql.database import Base


class LimitOrder(Base):
    __tablename__ = 'limit_orders'

    order_id = Column(String, primary_key=True, index=True)
    wallet_id = Column(String, index=True)
    from_token = Column(String)
    to_token = Column(String)
    from_token_amount = Column(Integer)
    rate_upper_limit = Column(DECIMAL)
    rate_lower_limit = Column(DECIMAL)
    sent_timestamp = Column(DateTime)
    received_timestamp = Column(DateTime)


class OrderState(Base):
    __tablename__ = 'order_states'

    order_id = Column(String, primary_key=True, index=True)
    state = Column(Enum(OrderStateEnum))
