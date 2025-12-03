"""Sample data matching the Excel model examples."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Example 1: Simple Two-Stock Portfolio (from Excel)
two_stock_example = {
    'Stock A': {
        'return': 0.157,  # 15.7%
        'std_dev': 0.176  # 17.6%
    },
    'Stock B': {
        'return': 0.171,  # 17.1%
        'std_dev': 0.293  # 29.3%
    },
    'RFA': {
        'return': 0.025,  # 2.5%
        'std_dev': 0.0    # 0%
    }
}

correlation_ab = 0.297

# Example 2: 10-Stock Market Portfolio (CAPM/SML Example)
stocks_10 = {
    'AAPL': {'beta': 1.253032, 'return': 0.0148},
    'XOM': {'beta': 0.865811, 'return': 0.0043},
    'LNC': {'beta': 1.970751, 'return': 0.0243},
    'MRK': {'beta': 0.8142, 'return': 0.0101},
    'WMT': {'beta': 0.387071, 'return': 0.0093},
    'HOG': {'beta': 0.806916, 'return': 0.0046},
    'RMD': {'beta': 0.820102, 'return': 0.0185},
    'AMZN': {'beta': 1.508175, 'return': 0.0284},
    'CMG': {'beta': 0.560292, 'return': -0.0010},
    'FB': {'beta': 0.675726, 'return': 0.0325}
}

sp500_return = 0.0077  # 0.77% monthly
risk_free_rate = 0.0025  # 0.25% monthly


def generate_monthly_returns(n_months: int = 60) -> pd.DataFrame:
    """
    Generate synthetic monthly returns data for 10 stocks.

    Args:
        n_months: Number of months to generate

    Returns:
        DataFrame with monthly returns
    """
    np.random.seed(42)
    dates = [datetime(2015, 1, 1) + timedelta(days=30*i) for i in range(n_months)]

    # Generate market returns
    market_returns = np.random.normal(sp500_return, 0.04, n_months)

    data = {}
    for stock, params in stocks_10.items():
        # Asset return = risk_free + beta * (market - risk_free) + alpha + noise
        alpha = 0.001  # 0.1% alpha
        idiosyncratic = np.random.normal(0, 0.02, n_months)
        asset_return = (
            risk_free_rate +
            params['beta'] * (market_returns - risk_free_rate) +
            alpha +
            idiosyncratic
        )
        data[stock] = asset_return

    data['S&P500'] = market_returns

    return pd.DataFrame(data, index=dates)


def simple_two_asset_example() -> pd.DataFrame:
    """
    Create simple example with two stocks and risk-free asset.
    Returns a DataFrame with daily returns for analysis.
    """
    np.random.seed(42)
    n_days = 252

    # Stock A: 15.7% annual return, 17.6% volatility
    stock_a = np.random.normal(0.157/252, 0.176/np.sqrt(252), n_days)

    # Stock B: 17.1% annual return, 29.3% volatility, corr=0.297 with A
    correlation = 0.297
    stock_b_independent = np.random.normal(0, 1, n_days)
    stock_b = (
        correlation * (stock_a / (0.176/np.sqrt(252))) +
        np.sqrt(1 - correlation**2) * stock_b_independent
    ) * (0.293/np.sqrt(252))
    stock_b += 0.171/252

    dates = pd.date_range('2015-01-01', periods=n_days, freq='D')

    return pd.DataFrame({
        'Stock A': stock_a,
        'Stock B': stock_b
    }, index=dates)


if __name__ == '__main__':
    # Generate and display example data
    returns = generate_monthly_returns()
    print("Sample returns data:")
    print(returns.head())
    print(f"\nShape: {returns.shape}")
    print(f"\nMean returns:\n{returns.mean()}")
