import numpy as np

from itertools import combinations
from typing import Optional, List

from logger import get_logger


logger = get_logger('SIMULATOR')


def sharpe_ratio(
        annual_return_rate: float,
        std_deviation: float,
        risk_free_rate: Optional[float] = 0
) -> float:
    return (annual_return_rate - risk_free_rate) / std_deviation


def compute_wallet_returns(
        daily_returns: np.ndarray,
        weights: np.ndarray,
) -> np.ndarray:
    return daily_returns @ weights


def compute_wallet_annual_return(
        returns_matrix: np.ndarray,
        trading_days: Optional[int] = 252
) -> float:
    return np.mean(returns_matrix) * trading_days


def compute_wallet_standard_deviation(
        weights: np.ndarray,
        cov_matrix: np.ndarray
) -> float:
    return np.sqrt(weights.T @ cov_matrix @ weights)


def compute_wallet_annual_standard_deviation(
        daily_standard_deviation: float,
        trading_days: Optional[int] = 252
) -> float:
    return daily_standard_deviation * (trading_days ** 0.5)


def generate_weights(
        n_assets: int,
        min_weight: Optional[float] = 0.0,
        max_weight: Optional[float] = 1.0,
        max_iterations: Optional[int] = 100000
) -> np.ndarray:
    weights = np.random.exponential(1, n_assets)
    weights /= weights.sum()

    vectorized_check_bound = np.vectorize(lambda w: min_weight <= w <= max_weight)

    for _ in range(max_iterations):
        bounds = vectorized_check_bound(weights)
        if np.all(bounds):
            return weights

        weights = np.random.exponential(1, n_assets)
        weights /= weights.sum()

    return weights


def generate_subsets(
        assets: List[any],
        subset_size: int
) -> List[List[any]]:
    if subset_size < 0 or subset_size > len(assets):
        logger.error('Invalid subset size')
        return [[]]

    return [
        list(subset) for subset in combinations(assets, subset_size)
    ]
