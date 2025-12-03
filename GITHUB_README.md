# Portfolio Optimizer 📊

A **Python-based portfolio optimization system** that automates modern portfolio theory analysis with real-time market data.

Input your stock portfolio → Get instant analysis → Optimal allocations + risk metrics.

**No API keys. No complex setup. Works in seconds.**

---

## 🎯 What It Does

Given a list of stocks, this tool automatically:

1. **Fetches real market data** from Yahoo Finance (2-10 years of historical prices)
2. **Calculates key metrics** (returns, volatility, correlations, covariance)
3. **Optimizes allocations** using Modern Portfolio Theory
4. **Generates professional reports** with actionable insights

### Example Analysis

Input:
```
Stocks: AAPL, MSFT, GOOGL
Period: 2 years
```

Output:
```
✓ Max Sharpe Ratio Portfolio: 60% AAPL + 40% MSFT
  Expected Return: 22.14% | Volatility: 22.58% | Sharpe: 0.049

✓ Minimum Variance Portfolio: 27% AAPL + 73% MSFT
  Expected Return: 19.59% | Volatility: 20.89% | Sharpe: 0.046

✓ Efficient Frontier: 20 optimal portfolios mapped
✓ CML Analysis: Risk-free rate, market premium, optimal combinations
✓ Report: Saved as portfolio_report_<timestamp>.txt
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/portfolio-optimizer.git
cd portfolio-optimizer

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
python3 main.py
```

Then follow the interactive prompts:
1. Enter stock tickers (e.g., AAPL, MSFT, GOOGL)
2. Select historical data period (1, 2, 5, or 10 years)
3. Name your portfolio
4. Get instant analysis report!

**Complete analysis takes 15-30 seconds.**

---

## 💡 Key Features

### Live Data Integration
- ✅ Real-time stock prices from Yahoo Finance
- ✅ Current US Treasury 10-year yield for risk-free rate
- ✅ Automatic data cleaning and daily returns calculation
- ✅ Support for 2-10 years of historical data

### Portfolio Optimization
- ✅ **Efficient Frontier**: Find all optimal portfolio combinations
- ✅ **Maximum Sharpe Ratio**: Best risk-adjusted returns
- ✅ **Minimum Variance**: Lowest risk portfolio
- ✅ **Target Return**: Find minimum-risk portfolio for desired return
- ✅ **Correlation Analysis**: Understand diversification benefits

### Advanced Analytics
- ✅ **Capital Market Line (CML)**: Optimal risky-safe asset combinations
- ✅ **Security Market Line (SML)**: CAPM valuation (extensible)
- ✅ **Risk Metrics**: Annual/monthly returns, volatility, Sharpe ratio
- ✅ **Covariance Matrix**: Full asset relationship mapping

### Professional Reports
- ✅ 7-section analysis reports
- ✅ Asset statistics and correlations
- ✅ Optimal portfolio allocations (as percentages)
- ✅ Efficient frontier summary
- ✅ CML analysis with implied returns
- ✅ Key insights and recommendations
- ✅ Auto-saved with timestamps

---

## 📋 Example Report

```
================================================================================
PORTFOLIO ANALYSIS REPORT
My Tech Portfolio
December 02, 2025 at 18:50:49
================================================================================

1. ASSET STATISTICS
        Annual Return  Annual Volatility
AAPL         25.18%           28.09%
MSFT         17.45%           22.10%

2. CORRELATION MATRIX
         AAPL   MSFT
AAPL     1.00   0.49
MSFT     0.49   1.00

3. OPTIMAL PORTFOLIOS
A. Maximum Sharpe Ratio Portfolio
   Allocation: AAPL 59.84% | MSFT 40.16%
   Return: 22.07% | Volatility: 22.50% | Sharpe: 0.0504

B. Minimum Variance Portfolio
   Allocation: MSFT 72.26% | AAPL 27.74%
   Return: 19.59% | Volatility: 20.89% | Sharpe: 0.0468

4. CAPITAL MARKET LINE
   Risk-Free Rate: 4.09%
   Market Return: 22.07%
   Sharpe Ratio: 0.0504

5. EFFICIENT FRONTIER
   20 optimal portfolios along the frontier
   Risk range: 20.89% - 28.09%
   Return range: 19.59% - 25.18%

[Full report with insights and recommendations...]
================================================================================
```

---

## 🏗️ Architecture

```
portfolio-optimizer/
├── main.py                      # Interactive CLI (entry point)
├── data_fetcher_yfinance.py     # Yahoo Finance integration + Treasury rate
├── portfolio.py                 # Core optimization engine (3 classes)
├── report_generator.py          # Professional report generation
├── visualization.py             # Matplotlib charts (optional)
├── requirements.txt             # Dependencies
└── README.md                    # Documentation
```

### Core Classes

**PortfolioOptimizer**
- Efficient frontier calculation
- Max Sharpe & min variance portfolios
- Target return portfolios
- Full statistical analysis

**CapitalMarketLine**
- CML calculations
- Risk-return combinations
- Implied return analysis

**SecurityMarketLine** (CAPM-ready)
- Alpha & beta calculations
- Asset valuation analysis
- Extensible for factor models

---

## 📚 Technical Details

### Formulas Implemented

**Portfolio Return** (daily)
```
E(R_p) = Σ w_i * E(R_i)
```

**Portfolio Volatility**
```
σ_p = √(w^T * Σ * w)
```

**Sharpe Ratio**
```
Sharpe = (E(R_p) - r_f) / σ_p
```

**Capital Market Line**
```
E(R) = r_f + Sharpe * σ
```

**Daily to Annual Scaling**
```
Annual Return = Daily Return × 252
Annual Volatility = Daily Volatility × √252
```

### Data Processing

1. **Yahoo Finance API**: Fetch historical daily prices
2. **Daily Returns**: Calculate `pct_change()` of closing prices
3. **Annualization**: Scale daily metrics by 252 trading days
4. **Covariance**: Annual covariance matrix from daily returns
5. **Optimization**: Constrained optimization using SciPy (SLSQP)

---

## 🎓 What You'll Learn

- Modern Portfolio Theory (Markowitz)
- Efficient Frontier optimization
- Sharpe ratio and risk-adjusted returns
- CAPM and Security Market Line
- Constrained optimization with scipy
- Real API integration
- Data pipelines with pandas
- Professional report generation

---

## 📊 Use Cases

✅ **Personal Finance**: Analyze your stock portfolio
✅ **Financial Advisors**: Generate client reports
✅ **Research**: Test portfolio theories
✅ **Education**: Learn MPT interactively
✅ **Fund Management**: Benchmark allocations
✅ **Risk Analysis**: Understand portfolio risk profile

---

## 🔧 Requirements

- Python 3.8+
- pandas (data handling)
- numpy (math/arrays)
- scipy (optimization)
- yfinance (Yahoo Finance data)
- matplotlib (visualizations - optional)

---

## 📝 Example Workflow

```python
from data_fetcher_yfinance import YahooFinanceAPI, get_current_risk_free_rate
from portfolio import PortfolioOptimizer
from report_generator import PortfolioReport

# Step 1: Fetch data
api = YahooFinanceAPI()
returns = api.get_returns_dataframe(['AAPL', 'MSFT', 'GOOGL'], period='2y')

# Step 2: Get current risk-free rate
rf_rate = get_current_risk_free_rate()

# Step 3: Optimize
optimizer = PortfolioOptimizer(returns, risk_free_rate=rf_rate)
max_sharpe = optimizer.max_sharpe_portfolio()
efficient_frontier = optimizer.efficient_frontier(n_points=50)

# Step 4: Report
report = PortfolioReport(optimizer, portfolio_name="My Portfolio")
report.print_report()
report.save_report()
```

---

## ⚠️ Disclaimer

**This tool is for educational and informational purposes only.**
- Past performance ≠ future results
- Not financial advice
- Consult a financial advisor before investing
- Test thoroughly with your own risk tolerance

---

## 🤝 Contributing

Contributions welcome! Ideas:
- Add Black-Litterman model
- Support for international equities
- Factor-based risk models
- Portfolio backtesting engine
- Web dashboard (Streamlit)
- Risk constraints (sector limits, max weights)
- Monte Carlo simulations

---

## 📄 License

MIT License - Free to use, modify, and distribute.

---

## 👨‍💻 Author

Built as a portfolio project demonstrating:
- Quantitative finance knowledge
- Python proficiency
- API integration
- Software engineering practices
- Clean code architecture

---

## 🚀 Getting Help

- **Setup Issues**: Check `SETUP.md`
- **How It Works**: See `WORKFLOW.md`
- **Project Overview**: Read `PROJECT_SUMMARY.md`
- **Code Examples**: Check `example_analysis.py`

---

**⭐ If you find this useful, please give it a star!**

Questions? Open an issue or reach out.

Happy analyzing! 📈
