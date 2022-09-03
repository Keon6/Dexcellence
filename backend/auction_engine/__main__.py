import datetime
import logging
import sys
from time import sleep

from auction_engine import engine, schemas
from auction_engine.sql import crud, models
from auction_engine.sql.database import SessionLocal, engine as db_engine

models.Base.metadata.create_all(bind=db_engine)
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stdout,
    force=True,
)

def update_order_states(transactions: list[schemas.Transaction]) -> None:
    with SessionLocal() as session:
        for transaction in transactions:
            crud.update_order_status(
                session=session,
                order_id=transaction.order.order_id,
                state=transaction.order_state,
            )


def run_auction(from_token: str, to_token: str) -> None:
    with SessionLocal() as session:
        limit_orders = [
            schemas.LimitOrder.from_orm(obj)
            for obj in crud.get_outstanding_limit_orders(
                session=session
            )
        ]
    if len(limit_orders) == 0:
        logging.info('No orders, skipping auction')
        return

    auction = engine.Auction(
        from_token=from_token,
        to_token=to_token,
        orders=limit_orders,
    )
    result = auction.run()
    # TODO: Send auction results

    update_order_states(result.transactions)


def main(
    interval: datetime.timedelta = datetime.timedelta(seconds=30),
    from_token: str = 'ETH',
    to_token: str = 'USDT',
) -> None:
    while True:
        now = datetime.datetime.now()
        run_at = now + interval
        logging.info('Next auction scheduled for %s', run_at)

        delay = interval.total_seconds()
        sleep(delay)
        logging.info('Starting auction')
        run_auction(from_token, to_token)


if __name__ == '__main__':
    main()
