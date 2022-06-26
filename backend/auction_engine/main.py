import datetime
import logging
import sys
from time import sleep

from auction_engine import engine, schemas
from auction_engine.sql import crud, models
from auction_engine.sql.database import SessionLocal, engine

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stdout,
    force=True,
)
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def update_order_states(transactions: list[schemas.Transaction]) -> None:
    with get_db() as session:
        for transaction in transactions:
            crud.update_order_status(
                session=session,
                order_id=transaction.order.order_id,
                state=transaction.order_state,
            )


def run_auction(from_token: str, to_token: str) -> None:
    with get_db() as session:
        limit_orders = [
            schemas.LimitOrder.from_orm(obj)
            for obj in crud.get_outstanding_limit_orders(
                session=session
            )
        ]

    auction = engine.Auction(
        from_token=from_token,
        to_token=to_token,
        orders=limit_orders,
    )
    result = auction.run()
    # TODO: Send auctio results

    update_order_states(result.transactions)


def main(
    interval: datetime.timedelta = datetime.timedelta(minutes=5),
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
