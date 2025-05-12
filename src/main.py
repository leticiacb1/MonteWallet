import argparse
import numpy as np
import pandas as pd

from tqdm import tqdm
from itertools import product
from functools import partial
from pathlib import Path
from typing import Dict
from multiprocessing import Pool, cpu_count

from simulate import *
from data_loader import *

from indexes import indexes
from logger import get_logger


logger = get_logger('MAIN')


def task_generator(
        assets_subsets: List[List[str]],
        weights_subsets: List[np.ndarray]
):
    for assets in assets_subsets:
        for weights in weights_subsets:
            yield (assets, weights)


def run_wallet(
        asset_subset: List[str],
        weights: np.ndarray,
        index_close_prices: pd.DataFrame
) -> Dict:
    filtered_data = index_close_prices.loc[:, asset_subset]
    returns = filtered_data.pct_change()
    cov_matrix = returns.cov().values.tolist()
    returns = returns[1:].values.tolist()

    wallet_return = compute_wallet_returns(
        daily_returns=returns,
        weights=weights
    )
    annual_wallet_return = compute_wallet_annual_return(
        returns_matrix=wallet_return
    )
    wallet_std_deviation = compute_wallet_standard_deviation(
        weights=weights,
        cov_matrix=cov_matrix
    )
    annual_wallet_std_deviation = compute_wallet_annual_standard_deviation(
        daily_standard_deviation=wallet_std_deviation
    )
    wallet_sharpe_ratio = sharpe_ratio(
        annual_return_rate=annual_wallet_return,
        std_deviation=annual_wallet_std_deviation
    )

    return {
        'Assets': asset_subset,
        'Weights': weights,
        'Annual Return': annual_wallet_return,
        'Annual Std Dev': annual_wallet_std_deviation,
        'Sharpe Ratio': wallet_sharpe_ratio
    }


def run_wallet_wrapper(args, index_close_prices):
    assets, weights = args
    return run_wallet(assets, weights, index_close_prices)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--index', type=str, required=True)
    parser.add_argument('--data_path', type=str, required=True)
    parser.add_argument('--start_date', type=str, required=True)
    parser.add_argument('--end_date', type=str, required=True)
    parser.add_argument('--n_assets', type=int, default=25)
    parser.add_argument('--n_wallets', type=int, default=1000)

    args = parser.parse_args()

    TOTAL_ASSETS = indexes[args.index]
    N_ASSETS = int(args.n_assets)
    N_WALLETS = int(args.n_wallets)
    PATH = Path(args.data_path)

    logger.debug(f'Running {N_WALLETS} wallets with {N_ASSETS} assets each from {args.index}')

    assets_data = {}
    for asset in TOTAL_ASSETS:
        logger.debug(f'Fetch data for {asset} from {args.start_date} to {args.end_date}')
        data = fetch_stock(
            ticker=asset,
            start_date=args.start_date,
            end_date=args.end_date
        )
        assets_data[asset] = data['Close']

    index_close_prices = pd.DataFrame(assets_data)

    assets_subsets = generate_subsets(TOTAL_ASSETS, N_ASSETS)
    weights_subsets = [
        generate_weights(
            n_assets=N_ASSETS,
            min_weight=0.0,
            max_weight=0.2
        ) for _ in range(N_WALLETS)
    ]
    logger.debug(f'Weights and assets subsets created')

    total_tasks = len(assets_subsets) * len(weights_subsets)
    logger.debug(f'Total number of tasks: {total_tasks}')

    task_func = partial(run_wallet_wrapper, index_close_prices=index_close_prices)
    tasks = list(task_generator(assets_subsets, weights_subsets))
    wallets = []

    with Pool(processes=cpu_count()) as pool:
        results = pool.imap(task_func, tasks, chunksize=1000)
        for result in tqdm(results, total=total_tasks, desc='Simulating wallets'):
            wallets.append(result)

    if wallets:
        best_wallet = max(wallets, key=lambda w: w['Sharpe Ratio'])
        logger.debug(f'Best wallet from {args.start_date} to {args.end_date} was:')
        for asset, weight in zip(best_wallet['Assets'], best_wallet['Weights']):
            logger.debug(f'{asset} - {round(weight * 100, 2)}%')
        logger.debug(f'Annual Return: {round(best_wallet["Annual Return"] * 100, 2)}%')
        logger.debug(f'Annual Std Dev: {round(best_wallet["Annual Std Dev"], 2)}')
        logger.debug(f'Sharpe Ratio: {round(best_wallet["Sharpe Ratio"], 2)}')
        pd.DataFrame(wallets).to_csv(PATH / 'wallets.csv')
