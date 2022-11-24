import numpy as np
import qpsolvers as qs
import cvxpy as cp

# TODO: really having trouble figuring out what the appropriate W and q need to e for multi asset auctions.

def raw_orders_to_portfolio_order(W, low_prices, high_prices):
    """
    :param W: N x I
    :param low_prices: N x I
    :param high_prices: N x I
    :return: low prices and high prices vectors for the portfolios (each instance of order across multiple assets = portfolio)

    """
    p_l = np.einsum('ij,ij->j', W, low_prices)
    p_h = np.einsum('ij,ij->j', W, high_prices)
    return p_l, p_h


def portfolio_order_optimization(W: np.array, p_l: np.array, p_h: np.array, q: np.array):
    """

    :param W: np.array
    :param p_l: low price to pay for portfolio
    :param p_h: high price to pay for portfolio
    :param q:
    :return: np.array - clearing quantities per portfolio order
    """
    return qs.solve_qp(
        P=0.5*np.diag(np.divide(p_h - p_l, q)), q=-p_h,
        A=W, b=np.zeros(len(W)),
        # G=np.identity(len(q)), h=q,
        lb=np.zeros(len(q)), ub=q,
        solver="osqp"
    )

def clearing_price(clearing_volumes, submitted_volumes, p_l, p_h):
    """
    For single asset auction
    """
    # TODO: Apparently this doesn't work too well....

    price_indices = np.argwhere(clearing_volumes < submitted_volumes)

    sell_indices = np.intersect1d(price_indices, np.argwhere(p_l < 0))
    buy_indices = np.intersect1d(price_indices, np.argwhere(p_l > 0))


    # sell_indices = np.argwhere(p_l < 0)
    # buy_indices = np.argwhere(p_l > 0)
    
    buy_prices, sell_prices = None, None

    

    if len(buy_indices) > 0:
        print("-----")
        print(submitted_volumes[buy_indices])
        print(clearing_volumes[buy_indices])
        buy_prices = p_h[buy_indices] - (p_h[buy_indices] - p_l[buy_indices])*clearing_volumes[buy_indices]/submitted_volumes[buy_indices]
    if len(sell_indices) > 0:
        print("-----")
        print(submitted_volumes[sell_indices])
        print(clearing_volumes[sell_indices])
        sell_prices = -p_h[sell_indices] + (-p_l[sell_indices] + p_h[sell_indices])*clearing_volumes[sell_indices]/submitted_volumes[sell_indices]

    return buy_prices, sell_prices

# TODO: still having some serious issue with multi-asset auction
# -> turning into portfolio units loses out a lot on actual volume that could've been executed. also having issues determining q and w

W = np.array([[1, 0.5 , -2, -0.5, 0.9, 0.1]])
# print(W)
p_l = np.array([1000, 1000, -1150, -1200, 1010, 1005])
p_h = np.array([1200, 1185, -1000, -1100, 1020, 1015])
# 1112.5
# print(W.shape, p_l.shape, p_h.shape)
q = np.array([1, 1 , 1, 1, 1, 1])

res = portfolio_order_optimization(W, p_l, p_h, q)
# print(res)


x = cp.Variable(6) # Auction fill quantity

D = np.diag((p_h - p_l) / (2 * q))
objective = cp.Maximize(x @ p_h - cp.quad_form(x, D))
constraints = [
    x @ W.T == 0,     # executed quantities must net to 0
    x >= 0,         # non-negative fill quantity
    x <= q,         # limit fill quantity
]
prob = cp.Problem(objective, constraints)
prob.solve()
# print(x)
# print(x.attributes)
print(res)
print(x.value)
print(p_l, p_h)
print(prob.constraints[0].dual_value)

print(clearing_price(np.abs(W[0]*res), np.abs(W[0]), p_l, p_h))
