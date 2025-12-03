"""
Fetch real stock data from Yahoo Finance (free, no API key needed).
"""

import yfinance as yf
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import requests


def get_current_risk_free_rate() -> float:
    """
    Get current US Treasury 10-year yield as risk-free rate.

    Returns:
        Annual risk-free rate (e.g., 0.045 for 4.5%)
    """
    try:
        # Fetch 10-year Treasury yield from Yahoo Finance
        treasury = yf.download('^TNX', period='1d', progress=False, timeout=5)
        if not treasury.empty:
            # TNX is already in percentage (e.g., 4.50 for 4.5%)
            current_yield_pct = float(treasury['Close'].iloc[-1])
            current_yield = current_yield_pct / 100  # Convert to decimal
            print(f"✓ Current 10-year Treasury yield: {current_yield_pct:.2f}%")
            return current_yield
    except Exception as e:
        print(f"⚠ Could not fetch current Treasury rate: {str(e)[:50]}")

    # Fallback to reasonable default if fetch fails
    default_rate = 0.045  # 4.5% as fallback
    print(f"✓ Using fallback risk-free rate: {default_rate*100:.2f}%")
    return default_rate


class YahooFinanceAPI:
    """Fetch historical stock data from Yahoo Finance."""

    def __init__(self):
        """Initialize Yahoo Finance fetcher (no API key needed)."""
        pass

    def get_daily_data(self, symbol: str, period: str = "2y") -> Optional[pd.DataFrame]:
        """
        Fetch daily historical stock data.

        Args:
            symbol: Stock ticker (e.g., 'AAPL')
            period: Data period ('1y', '2y', '5y', '10y', or specific dates)

        Returns:
            DataFrame with columns: Date, Close, Volume, or None if failed
        """
        try:
            print(f"Fetching data for {symbol}...", end=" ")

            # Download data from Yahoo Finance
            data = yf.download(
                symbol,
                period=period,
                progress=False,
                timeout=10
            )

            if data.empty:
                print(f"✗ No data found")
                return None

            # Reset index to make Date a column
            data.reset_index(inplace=True)

            # Keep only relevant columns
            data = data[['Date', 'Close', 'Volume']].copy()
            data.set_index('Date', inplace=True)

            print(f"✓ {len(data)} days of data")

            return data

        except Exception as e:
            print(f"✗ Error: {str(e)[:50]}")
            return None

    def get_multiple_stocks(self, symbols: List[str], period: str = "2y") -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple stocks.

        Args:
            symbols: List of stock tickers
            period: Data period

        Returns:
            Dictionary mapping symbol to DataFrame
        """
        data = {}
        for symbol in symbols:
            df = self.get_daily_data(symbol, period=period)
            if df is not None:
                data[symbol] = df
            else:
                print(f"Warning: Failed to fetch {symbol}")

        return data

    def get_returns_dataframe(self, symbols: List[str], period: str = "2y") -> Optional[pd.DataFrame]:
        """
        Fetch stock data and convert to daily returns.

        Args:
            symbols: List of stock tickers
            period: Data period ('1y', '2y', '5y', etc.)

        Returns:
            DataFrame with daily returns for each stock, or None if failed
        """
        print(f"\nFetching data for {len(symbols)} stocks...")
        print("=" * 60)

        try:
            # Download all data at once
            data = yf.download(
                symbols,
                period=period,
                progress=False,
                timeout=10
            )

            if data.empty:
                print("Failed to fetch any stock data!")
                return None

            # Extract closing prices
            if isinstance(data.columns, pd.MultiIndex):
                # Multiple stocks - columns are MultiIndex with ('Close', symbol)
                close_prices = data['Close']
            else:
                # Single stock - columns are simple
                close_prices = data[['Close']].rename(columns={'Close': symbols[0]})

            # Calculate daily returns
            returns_df = close_prices.pct_change().dropna()

            print("=" * 60)
            print(f"✓ Successfully fetched {len(returns_df.columns)} stocks")
            print(f"✓ Data range: {returns_df.index[0].date()} to {returns_df.index[-1].date()}")
            print(f"✓ Trading days: {len(returns_df)}")

            return returns_df

        except Exception as e:
            print(f"Failed to fetch data: {e}")
            return None


if __name__ == '__main__':
    # Example usage
    api = YahooFinanceAPI()
    returns = api.get_returns_dataframe(['AAPL', 'MSFT', 'GOOGL', 'TSLA'], period='2y')

    if returns is not None:
        print("\nReturns DataFrame:")
        print(returns.head())
        print(f"\nShape: {returns.shape}")
        print(f"Mean returns:\n{returns.mean()}")
