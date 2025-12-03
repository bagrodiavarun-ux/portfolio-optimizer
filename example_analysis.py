"""
Example analysis demonstrating the portfolio optimizer functionality.
Replicates key analyses from the Excel model.
"""

import pandas as pd
from portfolio import PortfolioOptimizer, CapitalMarketLine, SecurityMarketLine
from example_data import simple_two_asset_example, generate_monthly_returns


def analyze_two_asset_portfolio():
    """
    Analyze simple two-asset portfolio: Stock A, Stock B, and Risk-Free Asset.
    Demonstrates: Efficient Frontier, Sharpe Ratio, CML, and optimal allocation.
    """
    print("=" * 80)
    print("EXAMPLE 1: TWO-ASSET PORTFOLIO ANALYSIS")
    print("=" * 80)

    returns = simple_two_asset_example()
    optimizer = PortfolioOptimizer(returns, risk_free_rate=0.025/252)  # 2.5% annual

    print("\n1. Asset Statistics")
    print("-" * 80)
    stats = pd.DataFrame({
        'Return (Annual)': returns.mean() * 252,
        'Volatility (Annual)': returns.std() * np.sqrt(252),
        'Correlation': [1.0, returns['Stock A'].corr(returns['Stock B'])]
    }, index=returns.columns)
    print(stats)

    print("\n2. Maximum Sharpe Ratio Portfolio")
    print("-" * 80)
    max_sharpe = optimizer.max_sharpe_portfolio()
    print(f"Stock A Weight: {max_sharpe['weights']['Stock A']:.1%}")
    print(f"Stock B Weight: {max_sharpe['weights']['Stock B']:.1%}")
    print(f"Expected Return: {max_sharpe['return']*252:.2%}")
    print(f"Volatility: {max_sharpe['volatility']*np.sqrt(252):.2%}")
    print(f"Sharpe Ratio: {max_sharpe['sharpe_ratio']:.4f}")

    print("\n3. Minimum Variance Portfolio")
    print("-" * 80)
    min_var = optimizer.min_variance_portfolio()
    print(f"Stock A Weight: {min_var['weights']['Stock A']:.1%}")
    print(f"Stock B Weight: {min_var['weights']['Stock B']:.1%}")
    print(f"Expected Return: {min_var['return']*252:.2%}")
    print(f"Volatility: {min_var['volatility']*np.sqrt(252):.2%}")
    print(f"Sharpe Ratio: {min_var['sharpe_ratio']:.4f}")

    print("\n4. Efficient Frontier (Sample Points)")
    print("-" * 80)
    frontier = optimizer.efficient_frontier(n_points=10)
    print(frontier.to_string())

    print("\n5. Capital Market Line (CML)")
    print("-" * 80)
    cml = CapitalMarketLine(max_sharpe, risk_free_rate=0.025/252)
    print(f"Market Return: {cml.market_return*252:.2%}")
    print(f"Market Volatility: {cml.market_volatility*np.sqrt(252):.2%}")
    print(f"Sharpe Ratio: {cml.sharpe_ratio:.4f}")
    print(f"\nExpected return for 15% volatility: {cml.expected_return(0.15):.2%}")
    print(f"Required volatility for 12% return: {cml.required_volatility(0.12):.2%}")

    print("\n6. Portfolio Allocation for Target Return (11.1%)")
    print("-" * 80)
    target_portfolio = optimizer.portfolio_for_target_return(0.111)
    print(f"Stock A Weight: {target_portfolio['weights']['Stock A']:.1%}")
    print(f"Stock B Weight: {target_portfolio['weights']['Stock B']:.1%}")
    print(f"Expected Return: {target_portfolio['return']*252:.2%}")
    print(f"Volatility: {target_portfolio['volatility']*np.sqrt(252):.2%}")


def analyze_ten_stock_portfolio():
    """
    Analyze 10-stock portfolio with CAPM/SML analysis.
    Demonstrates: Alpha, Beta, SML valuation, and efficient frontier.
    """
    print("\n\n")
    print("=" * 80)
    print("EXAMPLE 2: 10-STOCK PORTFOLIO WITH CAPM/SML ANALYSIS")
    print("=" * 80)

    returns = generate_monthly_returns(n_months=60)
    market_returns = returns['S&P500']
    asset_returns = returns.drop('S&P500', axis=1)

    optimizer = PortfolioOptimizer(asset_returns, risk_free_rate=0.025/12)  # 2.5% annual
    sml = SecurityMarketLine(
        market_return=market_returns.mean(),
        market_volatility=market_returns.std(),
        risk_free_rate=0.025/12,
        asset_returns=asset_returns
    )

    print("\n1. Portfolio Statistics")
    print("-" * 80)
    stats = pd.DataFrame({
        'Return': asset_returns.mean() * 12,
        'Volatility': asset_returns.std() * np.sqrt(12),
    })
    print(stats)

    print("\n2. Maximum Sharpe Ratio Portfolio")
    print("-" * 80)
    max_sharpe = optimizer.max_sharpe_portfolio()
    print("\nOptimal Weights:")
    for asset, weight in sorted(max_sharpe['weights'].items(), key=lambda x: x[1], reverse=True):
        if weight > 0.01:
            print(f"  {asset}: {weight:.1%}")
    print(f"\nExpected Return: {max_sharpe['return']*12:.2%}")
    print(f"Volatility: {max_sharpe['volatility']*np.sqrt(12):.2%}")
    print(f"Sharpe Ratio: {max_sharpe['sharpe_ratio']:.4f}")

    print("\n3. Security Market Line (SML) Analysis")
    print("-" * 80)
    sml_analysis = sml.analyze_assets(market_returns)
    print(sml_analysis.to_string())

    print("\n4. Efficient Frontier")
    print("-" * 80)
    frontier = optimizer.efficient_frontier(n_points=15)
    print(frontier.head(10).to_string())

    print("\n5. Market Risk Premium & Expected Returns")
    print("-" * 80)
    print(f"Risk-Free Rate: {sml.risk_free_rate*12:.2%}")
    print(f"Market Return: {sml.market_return*12:.2%}")
    print(f"Market Risk Premium: {sml.market_risk_premium*12:.2%}")
    print(f"Market Volatility: {sml.market_volatility*np.sqrt(12):.2%}")


if __name__ == '__main__':
    import numpy as np
    analyze_two_asset_portfolio()
    analyze_ten_stock_portfolio()
