# Portfolio Optimizer

A Python library for modern portfolio theory calculations with **live market data** integration. Fetch real stock data from Yahoo Finance (free, no API key), optimize portfolios, and generate professional analysis reports.

## Overview

This project automates portfolio analysis with real-world data:

- **Live Data Fetching**: Automatically download historical stock prices from Yahoo Finance (free, no API key)
- **Efficient Frontier Calculation**: Find optimal portfolios across risk-return tradeoff
- **Sharpe Ratio Optimization**: Maximize risk-adjusted returns
- **Capital Market Line (CML)**: Analyze optimal combinations of risky and risk-free assets
- **Automated Report Generation**: Professional text reports with insights and recommendations
- **Portfolio Statistics**: Returns, volatility, correlation, covariance matrices

## Problem

Traditional portfolio analysis requires:
- Manual data collection from multiple sources
- Excel spreadsheets prone to errors
- No version control or reproducibility
- Tedious manual calculations
- No professional reporting

This library makes portfolio analysis **fully automated, data-driven, and professional**.

## Solution

A complete end-to-end portfolio analysis system:

1. **YahooFinanceAPI**: Fetch real historical stock data (free, no API key)
2. **PortfolioOptimizer**: Core class for efficient frontier and optimization
3. **CapitalMarketLine**: CML calculations and analysis
4. **SecurityMarketLine**: CAPM-based valuation and alpha calculations
5. **PortfolioReport**: Automated professional report generation
6. **Interactive Main Script**: User-friendly CLI for analysis

## Tech Stack

- **Python 3.8+**
- **pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **SciPy**: Optimization algorithms (SLSQP for constrained optimization)
- **yfinance**: Free stock data from Yahoo Finance
- **Matplotlib**: Visualization (optional)

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start (No API Key Needed!)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Interactive Analysis

```bash
python3 main.py
```

### 3. Follow the Prompts

The script will guide you through:
1. Enter stock tickers (e.g., AAPL, MSFT, GOOGL, TSLA)
2. Select historical data period (1, 2, 5, or 10 years)
3. Name your portfolio
4. Automatic analysis and report generation (takes 10-30 seconds)

### Example Output

```
PORTFOLIO ANALYSIS REPORT
My Tech Portfolio
December 02, 2024 at 14:32:00

================================================================================
1. ASSET STATISTICS
================================================================================
           Annual Return  Annual Volatility  Monthly Return  Monthly Volatility
AAPL             0.285230          0.342156        0.021286          0.098857
MSFT             0.298120          0.315642        0.022110          0.091187
GOOGL            0.267890          0.298765        0.019850          0.086378
TSLA             0.425300          0.487623        0.031525          0.140896

...
[Full detailed report with optimal allocations, risk analysis, CML analysis, etc.]
```

## Usage Examples

### Basic Example: Programmatic Use

```python
from data_fetcher_yfinance import YahooFinanceAPI
from portfolio import PortfolioOptimizer
from report_generator import PortfolioReport

# Fetch real data (free, no API key needed)
api = YahooFinanceAPI()
returns = api.get_returns_dataframe(['AAPL', 'MSFT', 'GOOGL'], period='2y')

# Optimize
optimizer = PortfolioOptimizer(returns, risk_free_rate=0.045)

# Generate report
report = PortfolioReport(optimizer, portfolio_name="Tech Portfolio")
report.print_report()
report.save_report("my_portfolio_report.txt")
```

### Efficient Frontier

```python
# Generate efficient frontier
frontier = optimizer.efficient_frontier(n_points=100)
print(frontier)

# Find portfolio with specific target return
target_portfolio = optimizer.portfolio_for_target_return(target_return=0.12)
```

### CAPM Analysis

```python
from portfolio import SecurityMarketLine

# Initialize SML with market data
sml = SecurityMarketLine(
    market_return=0.10,
    market_volatility=0.15,
    risk_free_rate=0.025,
    asset_returns=returns
)

# Analyze individual assets
analysis = sml.analyze_assets(market_proxy=sp500_returns)
print(analysis[['asset', 'beta', 'alpha', 'valuation']])
```

## Core Classes

### PortfolioOptimizer

Optimizes portfolio allocations based on mean-variance framework.

**Key Methods:**
- `portfolio_stats(weights)`: Calculate return, volatility, Sharpe ratio for given weights
- `max_sharpe_portfolio()`: Find portfolio maximizing Sharpe ratio
- `min_variance_portfolio()`: Find minimum variance portfolio
- `efficient_frontier(n_points)`: Generate efficient frontier points
- `portfolio_for_target_return(target_return)`: Minimum variance for target return

### CapitalMarketLine

Analyzes optimal combinations of risky and risk-free assets.

**Key Methods:**
- `expected_return(portfolio_volatility)`: Expected return for volatility on CML
- `required_volatility(target_return)`: Volatility needed to achieve return on CML

### SecurityMarketLine

CAPM-based analysis and valuation.

**Key Methods:**
- `calculate_beta(asset_returns, market_returns)`: Beta relative to market
- `calculate_alpha(asset_return, beta)`: Jensen's alpha
- `required_return(beta)`: Expected return per CAPM
- `analyze_assets(market_proxy)`: Full SML analysis for portfolio

## Example Data

### Two-Asset Portfolio
- Stock A: 15.7% return, 17.6% volatility
- Stock B: 17.1% return, 29.3% volatility
- Risk-Free Asset: 2.5% return, 0% volatility
- Correlation: 0.297

**Usage:**
```python
from example_data import simple_two_asset_example
returns = simple_two_asset_example()
```

### 10-Stock Market Portfolio
Real-world style data with 10 stocks (AAPL, XOM, LNC, MRK, WMT, HOG, RMD, AMZN, CMG, FB) with realistic betas and returns.

**Usage:**
```python
from example_data import generate_monthly_returns
returns = generate_monthly_returns(n_months=60)
```

## Results You Get

Running `example_analysis.py` demonstrates:

1. **Portfolio Statistics**: Returns, volatility, correlations
2. **Optimal Allocations**: Sharpe-maximizing and min-variance weights
3. **Efficient Frontier**: Risk-return frontier for all possible portfolios
4. **CML Analysis**: Optimal risky-safe asset combinations
5. **SML Valuation**: Alpha and beta for each security (which are under/overvalued)
6. **Target Return Portfolios**: Minimal-risk portfolio for desired returns

## Mathematical Foundation

### Sharpe Ratio
```
Sharpe = (Portfolio Return - Risk-Free Rate) / Portfolio Volatility
```

### Portfolio Return
```
E(R_p) = Σ w_i * E(R_i)
```

### Portfolio Volatility
```
σ_p = √(w^T * Σ * w)
where Σ is the covariance matrix
```

### Capital Market Line
```
E(R) = r_f + Sharpe * σ_p
```

### CAPM / Security Market Line
```
E(R_i) = r_f + β_i * (E(R_m) - r_f)
where β_i = Cov(R_i, R_m) / Var(R_m)
```

### Jensen's Alpha
```
α = R_i - [r_f + β_i * (R_m - r_f)]
```

## How to Run

### Basic Analysis
```bash
python3 example_analysis.py
```

### With Jupyter
```bash
jupyter notebook
# Open and run the example notebooks
```

## Project Structure

```
portfolio-optimizer/
├── portfolio.py              # Core classes and functions
├── example_data.py           # Sample data generators
├── example_analysis.py       # Example analyses
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

## Next Steps

Extensions possible:
- Constraint-based optimization (min/max weights, sector limits)
- Black-Litterman model for subjective return views
- Risk factor models (Fama-French, etc.)
- Portfolio backtesting engine
- Interactive Streamlit dashboard
- Support for constraints and transaction costs

## Real-World Applications

1. **Wealth Management**: Build optimal client portfolios
2. **Fund Management**: Construct index funds or active strategies
3. **Risk Management**: Analyze portfolio risk and volatility
4. **Research**: Validate CAPM, test alpha/beta strategies
5. **Education**: Teach modern portfolio theory concepts

## References

- Markowitz, H. (1952). "Portfolio Selection"
- Sharpe, W. (1964). "Capital Asset Prices"
- Lintner, J. (1965). "The valuation of risk assets"

## License

MIT

## Author

Built as a portfolio project demonstrating Python, quantitative finance, and software architecture.
