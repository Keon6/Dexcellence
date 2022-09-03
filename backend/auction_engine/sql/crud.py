from sqlalchemy.orm import Session

from auction_engine import schemas
from auction_engine.sql import models


def get_limit_order(
    session: Session,
    order_id: str,
) -> models.LimitOrder:
    return (
        session.query(models.LimitOrder)
        .filter(models.LimitOrder.order_id == order_id)
        .all()
    )


def get_outstanding_limit_orders(
    session: Session,
) -> list[models.LimitOrder]:
    return (
        session.query(models.LimitOrder)
        .join(
            models.OrderState,
            models.OrderState.order_id == models.LimitOrder.order_id
        )
        .filter(models.OrderState.state == schemas.OrderStateEnum.SUBMITTED)
        .all()
    )


def get_order_status(
    session: Session,
    order_id: str,
) -> models.OrderState:
    return (
        session.query(models.OrderState)
        .filter(models.OrderState.order_id == order_id)
        .all()
    )


def create_limit_order(
    session: Session,
    limit_order: schemas.LimitOrder,
) -> models.OrderState:
    db_limit_order = models.LimitOrder(**limit_order.dict())
    db_order_status = models.OrderState(
        order_id=limit_order.order_id,
        state=schemas.OrderStateEnum.SUBMITTED,
    )

    session.add_all([db_limit_order, db_order_status])
    session.commit()
    session.refresh(db_limit_order)
    session.refresh(db_order_status)

    return db_order_status


def update_order_status(
    session: Session,
    order_id: str,
    state: schemas.OrderStateEnum,
) -> None:
    order_status = get_order_status(session, order_id)
    order_status.state = state
    session.add(order_status)
    session.commit()
    session.refresh(order_status)
