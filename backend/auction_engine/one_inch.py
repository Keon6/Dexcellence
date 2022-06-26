import datetime
import json
import logging
import requests
from decimal import Decimal
from typing import Any

import pandas as pd
from pydantic import BaseModel, Field

API_BASE_URL = 'https://api.1inch.exchange'
API_ENDPOINTS = dict(
    swap = "swap",
    quote = "quote",
    tokens = "tokens",
    protocols = "protocols",
    protocols_images = "protocols/images",
    approve_spender = "approve/spender",
    approve_calldata = "approve/calldata"
)
API_CHAINS = dict(
    ethereum = '1',
    binance = '56'
)

class UnknownTokenError(Exception):
    pass


class TokenInfo(BaseModel):
    symbol: str
    name: str
    decimals: int
    address: str
    logoURI: str
    tags: list[str]


class Quote(BaseModel):
    from_token: TokenInfo = Field(alias='fromToken')
    to_token: TokenInfo = Field(alias='toToken')
    from_token_amount: str = Field(alias='fromTokenAmount')
    to_token_amount: str = Field(alias='toTokenAmount')
    protocols: list[Any]
    estimated_gas: int = Field(alias='estimatedGas')
    timestamp: datetime.datetime | None = None


class OneInchExchange(BaseModel):
    chain: str = 'ethereum'
    version: str = 'v4.0'
    tokens: dict[str, TokenInfo] = Field(default_factory=dict)
    tokens_by_address: dict[str, Any] = Field(default_factory=dict)
    chain_id: str | None = None

    def initialize(self) -> None:
        self.chain_id = API_CHAINS[self.chain]
        if self.health_check() != 'OK':
            raise ValueError('Health check for chain failed!')
        self.tokens = self.get_tokens()


    @staticmethod
    def _get(url: str, as_json: bool = True) -> dict[str, Any]:
        try:
            logging.debug(f'GET {url}')
            response = requests.get(url)
            if as_json:
                data = json.loads(response.text)
            else:
                data = response
        except requests.exceptions.ConnectionError as e:
            logging.error("ConnectionError when doing a GET request from {}".format(url))
            data = None
        return data  


    def health_check(self) -> Any:
        url = f'{API_BASE_URL}/{self.version}/{self.chain_id}/healthcheck'
        response = requests.get(url)
        result = json.loads(response.text)
        if 'status' in result:
            return result['status']
        return result


    def get_tokens(self) -> dict[str, TokenInfo]:
        url = f'{API_BASE_URL}/{self.version}/{self.chain_id}/tokens'
        result = self._get(url)
        if 'tokens' not in result:
            return result

        tokens = {
            token['symbol']: TokenInfo(**token)
            for token in result['tokens'].values()
        }
        return tokens


    def get_quote(
        self,
        from_token_symbol:str,
        to_token_symbol: str,
        amount:int,
    ) -> Quote:
        """
        Requests an aggregated quote from the 1inch dex to exchange an amount
        of one token into another
        """
        if from_token_symbol not in self.tokens:
            raise UnknownTokenError(from_token_symbol)
        if to_token_symbol not in self.tokens:
            raise UnknownTokenError(to_token_symbol)

        query_amount = (
            Decimal(
                10 ** self.tokens[from_token_symbol].decimals * amount
            )
            .quantize(Decimal('1.'))
        )
        query = 'fromTokenAddress={}&toTokenAddress={}&amount={}'.format(
            self.tokens[from_token_symbol].address, 
            self.tokens[to_token_symbol].address,
            query_amount,
        )
        url = f'{API_BASE_URL}/{self.version}/{self.chain_id}/quote?{query}'
        response = self._get(url, as_json=False)
        quote = Quote.parse_obj(json.loads(response.text))
        quote.timestamp = pd.to_datetime(response.headers['Date']).to_pydatetime()
        return quote

    def convert_amount_to_decimal(self, token_symbol: str, amount: int) -> Decimal:
        if token_symbol not in self.tokens:
            raise UnknownTokenError(token_symbol)

        decimal = self.tokens[token_symbol].decimals
        return Decimal(amount) / Decimal(10**decimal)


class ReferenceRate(BaseModel):
    from_token: str
    to_token: str
    amount: int
    rate: Decimal
    quote: Quote

    def __repr__(self) -> str:
        return f'ReferenceRate({self.rate} {self.to_token}/{self.from_token})'

API = OneInchExchange()
API.initialize()


def get_reference_rate(
    from_token: str,
    to_token: str,
    amount: int = 1,
) -> ReferenceRate:
    quote = API.get_quote(from_token, to_token, amount)
    from_decimal = API.convert_amount_to_decimal(
        token_symbol=from_token,
        amount=quote.from_token_amount,
    )
    to_decimal = API.convert_amount_to_decimal(
        token_symbol=to_token,
        amount=quote.to_token_amount,
    )

    return ReferenceRate(
        from_token=from_token,
        to_token=to_token,
        amount=amount,
        rate=to_decimal / from_decimal,
        quote=quote,
    )
    
