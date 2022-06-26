import logging
import sys

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from auction_engine import schemas
from auction_engine.sql import crud, models
from auction_engine.sql.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stdout,
    force=True,
)

APP = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@APP.get('/')
def index() -> dict[str, str]:
    return {'Dexcellence': 'Fast & Fair Trading'}


@APP.put('/submit/', response_model=schemas.OrderState)
def submit_limit_order(
    limit_order: schemas.LimitOrder,
    db: Session = Depends(get_db),
) -> None:
    logging.debug('Received order: %s', limit_order)
    crud.create_limit_order(db, limit_order)


@APP.get('/status/{order_id}', response_model=schemas.OrderState)
def get_order_status(
    order_id: str,
    db: Session = Depends(get_db),
):
    return crud.get_order_status(db, order_id)


@APP.get('/info/{order_id}', response_model=schemas.LimitOrder)
def get_order(
    order_id: str,
    db: Session = Depends(get_db),
):
    return crud.get_limit_order(db, order_id)
