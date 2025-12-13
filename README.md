# Portfolio Optimizer

A comprehensive Python-based portfolio optimization tool that implements Modern Portfolio Theory (MPT), Capital Asset Pricing Model (CAPM), and generates interactive reports with professional visualizations.

![Sample Report](https://img.shields.io/badge/Sample-Report-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Overview

This tool helps investors optimize their portfolio allocation by:
- Calculating optimal asset weights for maximum risk-adjusted returns
- Generating efficient frontiers and Capital Market Line analysis
- Performing CAPM-based security valuation
- Creating interactive HTML reports with embedded visualizations

**[📊 View Sample Report](SAMPLE_REPORT.html)** (Download and open in browser)

**[📋 Complete Feature List](FEATURES.md)**

## Key Features

### Portfolio Optimization
✓ **Maximum Sharpe Ratio Portfolio**: Find the optimal allocation that maximizes risk-adjusted returns
✓ **Minimum Variance Portfolio**: Identify the least risky portfolio combination
✓ **Efficient Frontier**: Generate the complete set of optimal portfolios
✓ **Position Size Constraints**: Prevent unrealistic over-concentration (default: max 40% per asset)

### Analysis Tools
✓ **Capital Market Line (CML)**: Analyze risk-return tradeoffs with leverage/lending
✓ **Security Market Line (SML)**: CAPM-based asset valuation with beta and alpha calculations
✓ **Correlation Analysis**: Understand asset relationships and diversification benefits
✓ **Risk Metrics**: Comprehensive volatility, covariance, and Sharpe ratio calculations

### Reporting
✓ **Interactive HTML Reports**: Professional reports with embedded charts
✓ **6 Visualization Types**: Efficient Frontier, Correlation Heatmap, Risk-Return Scatter, Sharpe Comparison, Cumulative Returns, Allocation Charts
✓ **CAPM Analysis**: Beta, alpha, and valuation for each asset vs market (S&P 500)

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/portfolio-optimizer.git
cd portfolio-optimizer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Run the interactive portfolio optimizer
python main.py
```

The program will guide you through:
1. Selecting stock tickers (e.g., AAPL, GOOGL, MSFT)
2. Choosing the historical data period (1, 2, 5, or 10 years)
3. Naming your portfolio
4. Selecting report format (HTML with charts recommended)

### Example Output

```
📊 Generating visualizations and HTML report...
✓ HTML report saved: portfolio_report_20251203_233928.html

Maximum Sharpe Ratio Portfolio:
  SHY:    40.00%
  JNJ:    31.99%
  GOOGL:  14.28%
  NVDA:   12.20%
  META:    1.54%

  Annual Return:  25.35%
  Volatility:      9.49%
  Sharpe Ratio:    2.25
```

## Advanced Usage

### Programmatic API

```python
from portfolio import PortfolioOptimizer
from data_fetcher_yfinance import YahooFinanceAPI
import numpy as np

# Fetch data
api = YahooFinanceAPI()
returns = api.get_returns_dataframe(['AAPL', 'GOOGL', 'MSFT'], period='2y')

# Create optimizer with position constraints
optimizer = PortfolioOptimizer(
    returns,
    risk_free_rate=0.04,      # 4% annual
    max_position_size=0.40    # Max 40% per asset
)

# Get optimal portfolios
max_sharpe = optimizer.max_sharpe_portfolio()
min_variance = optimizer.min_variance_portfolio()
frontier = optimizer.efficient_frontier(n_points=100)

# Access results
print(f"Optimal weights: {max_sharpe['weights']}")
print(f"Expected return: {max_sharpe['return'] * 252:.2%}")
print(f"Sharpe ratio: {max_sharpe['sharpe_ratio'] * np.sqrt(252):.4f}")
```

### Generate Custom Reports

```python
from report_generator_enhanced import EnhancedPortfolioReport

# Generate HTML report with charts
report = EnhancedPortfolioReport(
    optimizer,
    returns,
    portfolio_name="My Tech Portfolio"
)
html_file = report.save_html_report()
```

## Mathematical Foundation

All calculations are based on Modern Portfolio Theory and CAPM:

### Core Formulas

**Portfolio Return:**
```
R_p = Σ(w_i × R_i)
```

**Portfolio Variance:**
```
σ_p² = w^T × Cov × w
```

**Sharpe Ratio:**
```
Sharpe = (R_p - R_f) / σ_p
```

**CAPM Beta:**
```
β_i = Cov(R_i, R_M) / Var(R_M)
```

**Jensen's Alpha:**
```
α_i = R_i - [R_f + β_i × (R_M - R_f)]
```

**Capital Market Line:**
```
E[R_p] = R_f + Sharpe_M × σ_p
```

### Complete Documentation
- **[FORMULAS_AND_CALCULATIONS.md](FORMULAS_AND_CALCULATIONS.md)** - Detailed mathematical explanations
- **[FORMULAS_QUICK_REFERENCE.txt](FORMULAS_QUICK_REFERENCE.txt)** - Quick lookup guide
- **[validate_formulas.py](validate_formulas.py)** - Working examples with step-by-step calculations

## Example Results

Using stocks: AAPL, AMD, GOOGL, JNJ, META, MSFT, NVDA, SHY, TSLA (2-year period)

### Maximum Sharpe Portfolio (Constrained)
- **Allocation**: 40% SHY, 32% JNJ, 14% GOOGL, 12% NVDA, 2% META
- **Annual Return**: 25.35%
- **Annual Volatility**: 9.49%
- **Sharpe Ratio**: 2.25

### Minimum Variance Portfolio
- **Allocation**: 40% SHY, 37% JNJ, 15% MSFT, 4% GOOGL
- **Annual Return**: 15.40%
- **Annual Volatility**: 7.59%
- **Sharpe Ratio**: 1.50

## Project Structure

```
portfolio-optimizer/
├── main.py                          # Interactive CLI interface
├── portfolio.py                     # Core optimization engine
├── data_fetcher_yfinance.py         # Yahoo Finance data retrieval
├── report_generator.py              # Text report generation
├── report_generator_enhanced.py     # HTML report with charts
├── visualization.py                 # Chart generation
├── validate_formulas.py             # Formula verification script
├── FORMULAS_AND_CALCULATIONS.md     # Complete mathematical documentation
├── FORMULAS_QUICK_REFERENCE.txt     # Quick formula lookup
├── FEATURES.md                      # Detailed feature list
├── SAMPLE_REPORT.html               # Example generated report
├── requirements.txt                 # Python dependencies
├── LICENSE                          # MIT License
└── README.md                        # This file
```

## Technical Details

### Optimization
- **Algorithm**: Sequential Least Squares Programming (SLSQP)
- **Library**: scipy.optimize.minimize
- **Constraints**: Weights sum to 1, Long-only (0 ≤ w ≤ 0.40)

### Data Processing
- **Source**: Yahoo Finance (free, no API key)
- **Frequency**: Daily returns
- **Annualization**:
  - Returns: × 252 (trading days)
  - Volatility: × √252
  - Sharpe Ratio: × √252

### Key Assumptions
- Normal distribution of returns
- No transaction costs
- Static portfolio (no rebalancing)
- Historical data reflects future patterns

## Data Sources

- **Stock Prices**: Yahoo Finance (yfinance)
- **Risk-Free Rate**: US Treasury 10-year yield (^TNX)
- **Market Proxy**: S&P 500 (^GSPC)

All prices are auto-adjusted for splits and dividends.

## Validation

Run the validation script to verify all calculations:

```bash
python validate_formulas.py
```

This demonstrates:
- Daily to annual conversions
- Portfolio variance calculations
- Sharpe ratio computation
- Beta and Alpha calculations
- Capital Market Line

## Requirements

```
numpy>=1.21.0
pandas>=1.3.0
scipy>=1.7.0
matplotlib>=3.4.0
seaborn>=0.11.0
yfinance>=0.1.63
```

## Limitations

1. **Historical Data**: Past performance ≠ future results
2. **Normal Distribution**: Assumes Gaussian returns
3. **No Transaction Costs**: Ignores trading fees
4. **Static Model**: No dynamic rebalancing
5. **Market Efficiency**: Assumes efficient markets

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

### Academic Papers
1. Markowitz, H. (1952). "Portfolio Selection". *The Journal of Finance*, 7(1), 77-91.
2. Sharpe, W. F. (1964). "Capital Asset Prices: A Theory of Market Equilibrium under Conditions of Risk". *The Journal of Finance*, 19(3), 425-442.
3. Sharpe, W. F. (1966). "Mutual Fund Performance". *The Journal of Business*, 39(1), 119-138.

### Resources
- [Investopedia - Modern Portfolio Theory](https://www.investopedia.com/terms/m/modernportfoliotheory.asp)
- [CFA Institute - Portfolio Management](https://www.cfainstitute.org/en/membership/professional-development/refresher-readings/portfolio-concepts)

## Disclaimer

This tool is for **educational and research purposes only**. It should not be considered as financial advice. Always consult with a qualified financial advisor before making investment decisions.

---

**Created by:** Varun
**Last Updated:** December 2025
**Version:** 1.0 (with Position Constraints)
