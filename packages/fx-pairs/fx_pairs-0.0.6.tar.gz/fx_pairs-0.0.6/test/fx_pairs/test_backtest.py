import pandas as pd
import pytest

from fx_pairs.backtest import realised_pnl, unrealised_pnl


@pytest.fixture
def prices():
    prices_data = {"Asset1": [95, 100, 105, 110], "Asset2": [45, 50, 55, 60]}
    prices_df = pd.DataFrame(prices_data)
    date_index = pd.date_range("2023-01-01", periods=len(prices_df), freq="D")
    prices_df.index = date_index
    return prices_df


@pytest.fixture
def positions():
    positions_data = {"Asset1": [0, 10, -5, 8], "Asset2": [0, 5, 3, -2]}
    positions_df = pd.DataFrame(positions_data)

    date_index = pd.date_range(
        "2023-01-01", periods=len(positions_df), freq="D"
    )
    positions_df.index = date_index
    return positions_df


def test_unrealised_pnl(
    prices,
    positions,
):
    result = unrealised_pnl(positions, prices)

    expected_result = pd.DataFrame(
        {
            "Asset1": [0, 50.0, 47.619048, -76.923077],
            "Asset2": [0, 50.0, 50.909091, 18.333333],
        },
        index=positions.index,
    )

    pd.testing.assert_frame_equal(result, expected_result)


def test_realised_pnl(
    prices,
    positions,
):
    returns_df = realised_pnl(positions, prices)

    expected_result = pd.DataFrame(
        {
            "Asset1": [0, 50.0, -52.380952, 84.615385],
            "Asset2": [0, 50.0, 49.090909, -18.333333],
        },
        index=positions.index,
    )

    pd.testing.assert_frame_equal(returns_df, expected_result)


if __name__ == "__main__":
    pytest.main()
