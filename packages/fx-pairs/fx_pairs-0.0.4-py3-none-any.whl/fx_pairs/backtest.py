import numpy as np
import pandas as pd


def log_returns(dollar_prices):
    return np.log(dollar_prices / dollar_prices.shift()).dropna()


def calculate_trades(
    position: pd.DataFrame,
) -> pd.DataFrame:
    trades = position.diff()
    return trades[trades != 0].dropna(axis=1, how="all").fillna(0)


def trade_balance(
    trades: pd.DataFrame,
    dollar_prices: pd.DataFrame,
) -> pd.DataFrame:
    return (trades * dollar_prices).cumsum()


def realised_pnl(
    positions: pd.DataFrame,
    dollar_prices: pd.DataFrame,
) -> pd.DataFrame:
    trades = calculate_trades(positions)
    reindexed_positions = positions.reindex_like(trades)
    reindexed_prices = dollar_prices.reindex_like(trades)
    return (-1 * (trades * reindexed_prices)).cumsum() + (
        reindexed_positions * reindexed_prices
    )


def unrealised_pnl(
    positions: pd.DataFrame,
    dollar_prices: pd.DataFrame,
) -> pd.DataFrame:
    return (positions.multiply(dollar_prices)).diff().fillna(0)


def total_pnl(
    trades: pd.DataFrame,
    positions: pd.DataFrame,
    dollar_prices: pd.DataFrame,
) -> pd.DataFrame:
    return unrealised_pnl(trades, positions, dollar_prices)


def sharpe_ratio(
    positions: pd.DataFrame,
    dollar_prices: pd.DataFrame,
):
    trades = calculate_trades(positions)
    pnl = total_pnl(
        trades=trades, positions=positions, dollar_prices=dollar_prices
    ).sum(axis=1)
    ewm = log_returns(pnl).ewm(halflife=120)
    return ewm.mean() / ewm.std()
