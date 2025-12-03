"""
Fetch real stock data from Alpha Vantage API.
"""

import requests
import pandas as pd
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class AlphaVantageAPI:
    """Fetch historical stock data from Alpha Vantage API."""

    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key: str):
        """
        Initialize Alpha Vantage API client.

        Args:
            api_key: Your Alpha Vantage API key (get free from https://www.alphavantage.co/api/)
        """
        self.api_key = api_key
        self.rate_limit_delay = 0.25  # 0.25 second between requests (rate limit: 5 req/min)

    def get_daily_data(self, symbol: str, months: int = 24) -> Optional[pd.DataFrame]:
        """
        Fetch daily historical stock data.

        Args:
            symbol: Stock ticker (e.g., 'AAPL')
            months: How many months of data to fetch (default 24)

        Returns:
            DataFrame with columns: Date, Close, Volume, or None if failed
        """
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'outputsize': 'full',  # Get max available data
            'apikey': self.api_key
        }

        try:
            print(f"Fetching data for {symbol}...", end=" ")
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Check for errors
            if 'Error Message' in data:
                print(f"✗ Error: {data['Error Message']}")
                return None
            if 'Note' in data:
                print(f"✗ Rate limited: {data['Note']}")
                return None
            if 'Time Series (Daily)' not in data:
                print(f"✗ No data found")
                return None

            # Extract time series
            time_series = data['Time Series (Daily)']
            df = pd.DataFrame.from_dict(time_series, orient='index')
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()

            # Clean column names
            df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            df = df.astype(float)

            # Filter to requested months
            cutoff_date = datetime.now() - timedelta(days=30 * months)
            df = df[df.index >= cutoff_date]

            print(f"✓ {len(df)} days of data")
            time.sleep(self.rate_limit_delay)  # Respect rate limits

            return df

        except requests.exceptions.RequestException as e:
            print(f"✗ Network error: {e}")
            return None
        except Exception as e:
            print(f"✗ Error processing {symbol}: {e}")
            return None

    def get_multiple_stocks(self, symbols: List[str], months: int = 24) -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple stocks.

        Args:
            symbols: List of stock tickers
            months: Months of historical data

        Returns:
            Dictionary mapping symbol to DataFrame
        """
        data = {}
        for symbol in symbols:
            df = self.get_daily_data(symbol, months=months)
            if df is not None:
                data[symbol] = df
            else:
                print(f"Warning: Failed to fetch {symbol}")

        return data

    def get_returns_dataframe(self, symbols: List[str], months: int = 24) -> Optional[pd.DataFrame]:
        """
        Fetch stock data and convert to daily returns.

        Args:
            symbols: List of stock tickers
            months: Months of historical data

        Returns:
            DataFrame with daily returns for each stock, or None if failed
        """
        print(f"\nFetching data for {len(symbols)} stocks...")
        print("=" * 60)

        stock_data = self.get_multiple_stocks(symbols, months=months)

        if not stock_data:
            print("Failed to fetch any stock data!")
            return None

        # Extract closing prices
        close_prices = {}
        for symbol, df in stock_data.items():
            close_prices[symbol] = df['Close']

        prices_df = pd.DataFrame(close_prices)

        # Calculate daily returns
        returns_df = prices_df.pct_change().dropna()

        print("=" * 60)
        print(f"✓ Successfully fetched {len(returns_df.columns)} stocks")
        print(f"✓ Data range: {returns_df.index[0].date()} to {returns_df.index[-1].date()}")
        print(f"✓ Trading days: {len(returns_df)}")

        return returns_df


def validate_api_key(api_key: str) -> bool:
    """Test if API key is valid."""
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        return False

    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': 'AAPL',
        'apikey': api_key
    }

    try:
        response = requests.get(AlphaVantageAPI.BASE_URL, params=params, timeout=5)
        data = response.json()
        return 'Error Message' not in data and 'Note' not in data
    except:
        return False


if __name__ == '__main__':
    # Example usage
    API_KEY = "YOUR_API_KEY_HERE"  # Get from https://www.alphavantage.co/api/

    if not validate_api_key(API_KEY):
        print("Invalid API key! Get a free key from https://www.alphavantage.co/api/")
    else:
        api = AlphaVantageAPI(API_KEY)
        returns = api.get_returns_dataframe(['AAPL', 'MSFT', 'GOOGL'], months=12)
        if returns is not None:
            print("\nReturns DataFrame:")
            print(returns.head())
