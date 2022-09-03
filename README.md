# Dexcellence
> Hassle-free, fair trading

## What is Dexcellence?

Dexcellence provides an alternative market structure aiming to facilitate the exchange of crypto assets with greater liquidity and price stability.

Where conventional crypto and equity exchanges employ a continuous limit order book, Dexcellence utilizes Small Batch Auctions to clear a group of
trades at a uniform price.

Retail and institutional traders alike will enjoy the benefits of lower transaction costs (market impact + slippage), greater liquidity and a
unified OMS for exchanging crypto assets. 

## Auction Engine

The core objective of the auction engine is to compute the optimal clearing quantities and price for an order book. The order book consists of limit
orders to buy and sell a particular asset or currency pair.

The multi-asset flow trading optimization problem was formulated by [Budish et. al][1] and our single asset implementation can be found [here](https://github.com/mycoalchen/Dexcellence/blob/f2a3737f08162da4f18359e7ffffa712a7f94e29/backend/auction_engine/engine.py#L120).

Additional literature on batch auctions can be found in [Sources](#Sources).

## Sources

- Eric Budish & Peter Cramton & Albert S. Kyle & Jeongmin Lee & David Malec, 2022. ["Flow Trading,"][1] ECONtribute Discussion Papers Series 146, University of Bonn and University of Cologne, Germany.
- Eric Budish, Peter Cramton, John Shim, [The High-Frequency Trading Arms Race: Frequent Batch Auctions as a Market Design Response][2] , The Quarterly Journal of Economics, Volume 130, Issue 4, November 2015, Pages 1547–1621

[1]: https://ideas.repec.org/p/ajk/ajkdps/146.html
[2]: https://doi.org/10.1093/qje/qjv027
