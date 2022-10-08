from multiprocessing import freeze_support
import argparse

import cvxpy as cp
# import cvxopt as co
import qpsolvers as qs

import numpy as np
import pandas as pd
# from timeit import timeit
from time import time
import concurrent.futures as parallel


# Basic architecture: Orders -> Optimization Readable Format (portfolio orders)
#   -> Results into Clearing Prices per asset and Quantities per order per asset

# TODO: Python numeric approx, would it be an issue?

Iterations = 100 # of iterations per approach


def orders_to_portfolio_order(W, low_prices, high_prices):
    # TODO: W can be normalized per order or not. As long as all the auctions hold on to what the actual volume were
    """
    :param W: N x I
    :param low_prices: N x I
    :param high_prices: N x I
    :return: low prices and high prices vectors for the portfolios (each instance of order across multiple assets = portfolio)

    """
    p_l = np.einsum('ij,ij->j', W, low_prices)
    p_h = np.einsum('ij,ij->j', W, high_prices)
    return p_l, p_h

def order_to_quadratic_program(W: np.array, p_l: np.array, p_h: np.array, q: np.array, package: str, solver):
    """

    :param W: np.array
    :param p_l: low price to pay for portfolio
    :param p_h: high price to pay for portfolio
    :param q:
    :return:
    """
    n = len(p_h)  # number of assets
    i = len(W)  # number of orders
    D = np.diag(np.divide(p_h - p_l, q))
    G = np.identity(n)
    # print(D.shape, G.shape, p_h.shape, W.shape, q.shape)
    if package == "cvxpy":
        x = cp.Variable(n)
        objective = cp.Maximize(x @ p_h - (1/2) * cp.quad_form(x, D))
        constraints = [
            W @ x == np.zeros(i),  # executed quantities must net to 0
            x >= 0,  # non-negative fill quantity
            x <= q,  # limit fill quantity
        ]

        prob = cp.Problem(
            objective, constraints
        )
        # D  IxI, p_h = 1 x I
        # G IxI, q = 1 x I
        # W NxI
        prob.solve(solver=solver)
        return x.value
    # elif package == "cvxopt":
    #     x = co.solvers.qp(
    #         P=co.matrix(D), q=co.matrix(-p_h.T),
    #         G=co.matrix(G), h=co.matrix(q),
    #         A=co.matrix(W), b=co.matrix(np.zeros(i))
    #     )
    #     return x
    elif package == "qpsolver":
        return qs.solve_qp(
            P=D, q=-p_h,
            G=G, h=q,
            A=W, b=np.zeros(i),
            solver=solver
        )
    else:
        raise ValueError("unrecognized package")


def portfolio_to_asset(clearing_portfolio_amounts, clearing_portfolio_prices, W):
    """
    Given clearing portoflio quantities, convert into clearing quantities per asset per order &
    calculate clearing price per asset
    :param clearing_portfolio_amount: x -
    :param W:
    :return:
    """
    clearing_amounts = W*clearing_portfolio_amounts
    def clearing_amount_to_price(clearing_amounts, clearing_portfolio_prices, W): # TODO how to convert from clearing amount ot prices
        pass



def main(N, I):
    def run_qp(W, p_l, p_h, q, package, solver, i):
        try:
            st = time()
            x = order_to_quadratic_program(W=W, p_l=p_l, p_h=p_h, q=q, package=package, solver=solver)
            return {"Package": package, "Solver": solver, "Iteration": i, "Time": time()-st, "Error": None}
        except Exception as e:
            print(e)
            return {"Package": package, "Solver": solver, "Iteration": i, "Time": None, "Error": e}

    def run_qp_cvxopt(W, p_l, p_h, q, package, i):
        try:
            st = time()
            x = order_to_quadratic_program(W=W, p_l=p_l, p_h=p_h, q=q, package=package, solver="")
            return {"Package": package, "Solver": None, "Iteration": i, "Time": time() - st, "Error": None}
        except Exception as e:
            return {"Package": package, "Solver": None, "Iteration": i, "Time": None, "Error": e}

    # TODO: Make sure we set q =

    np.random.seed(120)
    # 5 assets & 10 orders
    W = 2*np.random.random((N, I)) # we can normalzie this or not, that's our choice
    low_prices = 2000*np.random.random((N, I)) - 1000
    high_prices = low_prices + 5*np.random.random((N, I))
    p_l, p_h = orders_to_portfolio_order(W, low_prices, high_prices)
    del low_prices, high_prices
    q = 20*(np.random.random(I)+1) # we should let the system determine what q is

    packages = ["cvxpy", 
                # "cvxopt", 
                "qpsolver"]
    solvers = {
        "cvxpy": [cp.OSQP, cp.ECOS, cp.GLOP, cp.MOSEK, cp.CBC, cp.CVXOPT, cp.NAG, cp.PDLP, cp.GUROBI, cp.SCS],
        "qpsolver": ["osqp", "ecos", "cvxopt", "scs",  "quadprog"]
    }

    df_res = pd.DataFrame(columns=["Package", "Solver", "Iteration", "Time", "Error"])

    for package in packages:
        if package in solvers:
            for solver in solvers[package]:
                with parallel.ThreadPoolExecutor(100) as executor:
                    future_res = {executor.submit(run_qp, W, p_l, p_h, q, package, solver, i):  i for i in range(Iterations)}  
                    for future in parallel.as_completed(future_res):
                        row = future.result()
                        df_res = df_res.append(row, ignore_index=True)
        else:
            with parallel.ThreadPoolExecutor(100) as executor:
                future_res = {executor.submit(run_qp_cvxopt, W, p_l, p_h, q, package, i): i for i in range(Iterations)}
                for future in parallel.as_completed(future_res):
                    row = future.result()
                    df_res = df_res.append(row, ignore_index=True)
            
                # print("Package:", package, "| Error: ", e)
    # print(df_res)
    df_res.to_csv("/Users/keonshikkim/Desktop/Dexcellence/test/results/quad_program_library_comparison_numbAssets={}_numbOrders={}.csv".format(N, I))

    # x1 = order_to_quadratic_program(W=W, p_l=p_l, p_h=p_h, q=q, package="qpsolver", solver="quadprog")
    # x2 = order_to_quadratic_program(W=W/200, p_l=p_l, p_h=p_h, q=q, package="qpsolver", solver="quadprog")
    # a = (x1 - x2)
    # print(a)
    # print(sum(a))
    # portfolio_to_asset(x, W, p_l, p_h)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--numb_assets", type=int)
    parser.add_argument("-i", "--numb_orders", type=int)
    args = parser.parse_args()

    freeze_support()
    main(N=args.numb_assets, I=args.numb_orders)
