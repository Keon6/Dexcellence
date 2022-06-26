import asyncio
import datetime
import logging
from decimal import Decimal
from typing import Any
from uuid import uuid4

import cvxpy as cp
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from pydantic import Field

from auction_engine import one_inch
from auction_engine.schemas import LimitOrder, StrictModel, Transaction, OrderStateEnum


class AuctionOrder(StrictModel):
    order: LimitOrder
    received_timestamp: datetime.datetime


class AuctionResult(StrictModel):
    auction_id: str
    transactions: list[Transaction] = Field(repr=False)
    clearing_rate: Decimal
    from_token: str
    to_token: str
    result_timestamp: datetime.datetime


class Auction(StrictModel, arbitrary_types_allowed=True):
    from_token: str
    to_token: str
    orders: list[LimitOrder]
    auction_id: str = Field(default_factory=lambda: str(uuid4()))
    reference_rate_tolerance: Decimal = Decimal(0.01)
    
    # Runtime variables
    orders_by_id: dict[str, LimitOrder] | None = None
    order_book: pd.DataFrame | None = None

    def get_order_book(self) -> pd.DataFrame:
        logging.info('Compiling order book data')
        self.orders_by_id = {
            order.order_id: order for order in self.orders
        }
        order_book = pd.DataFrame.from_records(
            data=[order.dict() for order in self.orders],
            columns=LimitOrder.fields()
        )
        standard_pair = f'{self.from_token}/{self.to_token}'
        order_book['pair'] = (
            order_book['from_token'] + '/' + order_book['to_token']
        )
        fltr_standard_pair = order_book['pair'].eq(standard_pair)

        for rate in ['rate_upper_limit', 'rate_lower_limit']:
            standard_rate = order_book[rate].copy()
            standard_rate[~fltr_standard_pair] = (
                -standard_rate.loc[~fltr_standard_pair].pow(-1)
            )
            order_book[f'standard_{rate}'] = standard_rate

        order_book['standard_pair'] = standard_pair
        order_book['standard_amount'] = order_book['from_token_amount']
        order_book['side'] = order_book['pair'].map({standard_pair: 'BUY'}).fillna('SELL')
        return order_book

    def plot_order_book(
        self,
        reference_rate: float | None = None,
        clearing_rate: float | None = None,
    ) -> Line2D:
        order_book = self.get_order_book()
        col_map = {
            'standard_amount': 'amount',
            'side': 'side',
            'standard_pair': 'pair',
            'standard_rate_upper_limit': 'limit_rate',
        }
        plot_data = order_book[col_map.keys()].rename(columns=col_map).copy()
        plot_data['limit_rate'] = plot_data['limit_rate'].abs()

        plt = plot_data.plot.scatter(
            x='amount',
            y='limit_rate',
            c=order_book['side'].replace({'BUY': 'green', 'SELL': 'red'}),
            title=f'Auction Order Book {self.from_token}/{self.to_token}',
            alpha=0.6,
            figsize=(10, 7)
        )
        if reference_rate:
            plt.axhline(y=reference_rate, color='lightblue', linestyle='-')
        if clearing_rate:
            plt.axhline(y=clearing_rate, color='blue', linestyle='-')
        return plt

    @staticmethod
    def get_optimization_problem(order_book: pd.DataFrame) -> cp.Problem:
        logging.info('Constructing optimization problem')
        # Optimization problem
        side = order_book['side'].map({'BUY': 1, 'SELL': -1}).values

        n = len(order_book)
        x = cp.Variable(n)                                              # Auction fill quantity
        p_h = order_book['standard_rate_upper_limit'].values            # upper bound
        p_l = order_book['standard_rate_lower_limit'].values            # lower bound
        w = side                                                        # "Portfolio" weights
        q = order_book['standard_amount'].values                        # Order quantity

        if (p_l > p_h).any():
            raise ValueError('Invalid orders: some p_l > p_h!')

        D = np.diag((p_h - p_l) / (2 * q))
        objective = cp.Maximize(x @ p_h - cp.quad_form(x, D))
        constraints = [
            x @ w == 0,     # executed quantities must net to 0
            x >= 0,         # non-negative fill quantity
            x <= q,         # limit fill quantity
        ]
        return cp.Problem(objective, constraints)

    def update_order_book(
        self,
        order_book: pd.DataFrame,
        optimal_fills: pd.Series,
        clearing_rate: Decimal,
    ) -> pd.DataFrame:
        logging.info('Updating the order book')

        order_book['optimal_fill'] = optimal_fills
        order_book['standard_clearing_rate'] = clearing_rate
        order_book['fill_status'] = None
        fltr_filled = order_book['optimal_fill'].eq(order_book['standard_amount'])
        fltr_partial = order_book['optimal_fill'].between(
            left=0,
            right=order_book['standard_amount'],
            inclusive='neither',
        )
        fltr_unfilled = order_book['optimal_fill'].lt(1e-10)

        states = {
            OrderStateEnum.FILLED: fltr_filled,
            OrderStateEnum.PARTIAL: fltr_partial,
            OrderStateEnum.INCOMPLETE: fltr_unfilled,
        }

        for state, fltr in states.items():
            order_book.loc[fltr, 'fill_status'] = state

        # Convert SELL orders back to their original basis
        standard_pair = f'{self.from_token}/{self.to_token}'
        fltr_standard_pair = order_book['pair'].eq(standard_pair)
        order_book['clearing_rate'] = order_book['standard_clearing_rate']
        order_book.loc[~fltr_standard_pair, 'clearing_rate'] = (
            order_book.loc[~fltr_standard_pair, 'clearing_rate'].pow(-1)
        )

        return order_book

    def get_transactions(self, order_book: pd.DataFrame) -> list[Transaction]:
        logging.info('Compiling transactions')
        fltr_has_fill = ~order_book['fill_status'].eq('unfilled')
        transactions: list[Transaction] = [
            Transaction(
                order=self.orders_by_id[row['order_id']],
                order_state=row['fill_status'],
                rate=row['clearing_rate'],
                from_token=row['from_token'],
                to_token=row['to_token'],
                amount=row['optimal_fill'],
                auction_id=str(self.auction_id),
            )
            for _, row in order_book.loc[fltr_has_fill].iterrows()
        ]
        return transactions

    def run(self) -> AuctionResult:
        logging.info('Starting auction')
        order_book = self.get_order_book()
        opt_problem: cp.Problem = self.get_optimization_problem(order_book)

        logging.info('Optimizing')
        opt_problem.solve()

        reference_rate = one_inch.get_reference_rate(self.from_token, self.to_token)
        clearing_rate = opt_problem.constraints[0].dual_value
        logging.info(f'Validating clearing_rate {clearing_rate} with 1inch')

        if clearing_rate > reference_rate.rate * (1 + self.reference_rate_tolerance):
            raise ValueError(f'Clearing rate {clearing_rate} is >1% above ref rate {reference_rate}')
        if clearing_rate < reference_rate.rate * (1 - self.reference_rate_tolerance):
            raise ValueError(f'Clearing rate {clearing_rate} is >1% below ref rate {reference_rate}')

        self.update_order_book(
            order_book,
            optimal_fills=opt_problem.variables()[0].value,
            clearing_rate=clearing_rate,
        )

        transactions = self.get_transactions(order_book)
        self.order_book = order_book
        return AuctionResult(
            auction_id=str(self.auction_id),
            clearing_rate=clearing_rate,
            transactions=transactions,
            from_token=self.from_token,
            to_token=self.to_token,
            result_timestamp=datetime.datetime.utcnow(),
        )
