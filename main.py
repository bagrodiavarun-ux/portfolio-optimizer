"""
Main execution script for portfolio analysis.
User inputs stock tickers, downloads real data, and generates report.
"""

import sys
from typing import List
from data_fetcher_yfinance import YahooFinanceAPI, get_current_risk_free_rate
from portfolio import PortfolioOptimizer
from report_generator import PortfolioReport


def get_stock_symbols() -> List[str]:
    """
    Get stock symbols from user input.

    Returns:
        List of stock tickers
    """
    print("\n" + "=" * 80)
    print("PORTFOLIO STOCK SELECTION")
    print("=" * 80)
    print("\nEnter the stock tickers you want to analyze.")
    print("Examples: AAPL, MSFT, GOOGL, TSLA, META, etc.")
    print("(Enter one ticker per line. Type 'done' when finished)\n")

    symbols = []
    while True:
        symbol = input(f"Stock {len(symbols) + 1}: ").strip().upper()

        if symbol.lower() == 'done':
            if len(symbols) < 2:
                print("✗ Please enter at least 2 stocks for portfolio analysis")
                continue
            break

        if symbol and len(symbol) <= 5 and symbol.isalpha():
            symbols.append(symbol)
        else:
            print("✗ Invalid ticker. Please try again.")

    return symbols


def get_data_period() -> str:
    """
    Get historical data period from user.

    Returns:
        Period string for yfinance ('1y', '2y', '5y', '10y')
    """
    print("\n" + "=" * 80)
    print("HISTORICAL DATA PERIOD")
    print("=" * 80)
    print("\nHow many years of historical data would you like?")
    print("Options: 1y (1 year), 2y (2 years), 5y (5 years), 10y (10 years)")
    print("Default: 2y (recommended for portfolio analysis)\n")

    valid_periods = {'1': '1y', '2': '2y', '5': '5y', '10': '10y'}

    while True:
        choice = input("Enter years (1, 2, 5, or 10) [default 2]: ").strip() or "2"
        if choice in valid_periods:
            return valid_periods[choice]
        else:
            print("✗ Please enter 1, 2, 5, or 10")


def get_portfolio_name() -> str:
    """Get custom portfolio name from user."""
    print("\n" + "=" * 80)
    print("PORTFOLIO NAME")
    print("=" * 80)
    name = input("\nEnter a name for this portfolio (default 'My Portfolio'): ").strip()
    return name if name else "My Portfolio"


def main():
    """Main execution flow."""
    try:
        print("\n")
        print("╔" + "=" * 78 + "╗")
        print("║" + "PORTFOLIO OPTIMIZER - LIVE DATA ANALYSIS".center(78) + "║")
        print("║" + "Real-time stock portfolio optimization and analysis".center(78) + "║")
        print("╚" + "=" * 78 + "╝")

        # Step 1: Initialize Yahoo Finance API (no key needed)
        api = YahooFinanceAPI()
        print("\n✓ Yahoo Finance ready (no API key needed)")

        # Step 2: Get stock symbols
        symbols = get_stock_symbols()
        print(f"\n✓ Selected stocks: {', '.join(symbols)}")

        # Step 3: Get data period
        period = get_data_period()
        print(f"✓ Data period: {period}")

        # Step 4: Get portfolio name
        portfolio_name = get_portfolio_name()
        print(f"✓ Portfolio name: {portfolio_name}")

        # Step 5: Fetch data
        print("\n" + "=" * 80)
        print("FETCHING REAL MARKET DATA")
        print("=" * 80)

        returns_df = api.get_returns_dataframe(symbols, period=period)

        if returns_df is None or returns_df.empty or len(returns_df.columns) < 2:
            print("\n✗ Failed to fetch sufficient data. Please try again later.")
            return

        # Step 6: Get current risk-free rate and initialize optimizer
        print("\n" + "=" * 80)
        print("OPTIMIZING PORTFOLIO")
        print("=" * 80)
        print("\nFetching current risk-free rate...")

        # Get latest US Treasury 10-year yield
        risk_free_rate = get_current_risk_free_rate()

        print("Calculating efficient frontier, optimal allocations, and metrics...")
        optimizer = PortfolioOptimizer(returns_df, risk_free_rate=risk_free_rate)

        print("✓ Optimization complete!")

        # Step 7: Generate report
        print("\n" + "=" * 80)
        print("GENERATING REPORT")
        print("=" * 80)

        report = PortfolioReport(optimizer, portfolio_name=portfolio_name)

        # Print to console
        report.print_report()

        # Save to file
        report.save_report()

        print("\n" + "=" * 80)
        print("✓ ANALYSIS COMPLETE")
        print("=" * 80)
        print("\nNext steps:")
        print("  • Review the report above")
        print("  • Check the saved report file for detailed analysis")
        print("  • Consider your risk tolerance and investment goals")
        print("  • Consult a financial advisor before investing")

    except KeyboardInterrupt:
        print("\n\n✗ Analysis cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
