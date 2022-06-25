# Frequent Batch Auctions

## Sources

- [2015 Paper](https://academic.oup.com/qje/article/130/4/1547/1916146)

## Notes

- Orders
  - types
    - limit order
    - market order

> At any moment in time during a batch interval, traders (i.e., investors or trading firms) may submit offers to buy and sell shares of stock in the form of limit orders and market orders. Just as in the continuous market, a limit order is a price-quantity pair expressing an offer to buy or sell a specific quantity at a specific price, and a market order specifies a quantity but not a price.

- Auction Execution
  - Intersection of supply + demand functions = uniform clearing price
  - If intersection DNE -> no transaction
  
> At the end of each batch interval, the exchange batches all outstanding orders—both new orders received during this interval, and orders outstanding from previous intervals—and computes the aggregate demand and supply functions out of all bids and asks, respectively. If demand and supply do not intersect, then there is no trade and all orders remain outstanding for the next batch auction. If demand and supply do intersect, then the market clears where supply equals demand, with all transactions occurring at the same price—that is, at a “uniform price.”
> If demand and supply intersect horizontally or at a point, this pins down a unique market-clearing price p∗ and a unique maximum possible quantity q∗ . In this case, offers to buy with bids strictly greater than p∗ and offers to sell with asks strictly less than p∗ transact their full quantity at price p∗ , whereas for bids and asks of exactly p∗ it may be necessary to ration one side of the market to enable market clearing.
> If demand and supply intersect vertically, this pins down a unique quantity q∗ and an interval of market-clearing prices, [p∗L, p∗H] . In this case, all offers to buy with bids weakly greater than p∗H and all offers to sell with asks weakly lower than p∗L transact their full quantity, and the price is (p∗L + p∗H) / 2 .
