# Setup Guide - Portfolio Optimizer

## Step 1: Get Alpha Vantage API Key (Free)

1. Go to https://www.alphavantage.co/api/
2. Enter your email address
3. You'll receive a free API key immediately
4. Keep this key safe - you'll use it to fetch stock data

## Step 2: Install Python Dependencies

```bash
cd ~/portfolio-optimizer
pip install -r requirements.txt
```

This installs:
- pandas: Data manipulation
- numpy: Numerical computing
- scipy: Optimization algorithms
- requests: API calls
- matplotlib: Charting
- jupyter: Notebooks (optional)

## Step 3: Run the Portfolio Optimizer

### Option A: Using Environment Variable (Recommended)

```bash
export ALPHA_VANTAGE_API_KEY="your_api_key_here"
python3 main.py
```

### Option B: Enter Key When Prompted

```bash
python3 main.py
```

The script will ask for your API key if not set in environment.

## Step 4: Follow the Interactive Prompts

When you run `python3 main.py`, you'll be guided through:

1. **Select Stocks**: Enter stock tickers (AAPL, MSFT, GOOGL, TSLA, etc.)
   - Enter one per line
   - Type "done" when finished
   - Need at least 2 stocks

2. **Data Period**: Choose how many months of history
   - Default: 24 months (2 years)
   - Min: 6 months
   - Max: 120 months

3. **Portfolio Name**: Give your portfolio a name
   - Example: "My Tech Portfolio"
   - Default: "My Portfolio"

4. **Automatic Analysis**: The script will:
   - Fetch real market data from Alpha Vantage
   - Calculate optimal allocations
   - Generate analysis report
   - Save to file

## Example: Tech Portfolio Analysis

```bash
$ python3 main.py

Enter stock tickers:
Stock 1: AAPL
Stock 2: MSFT
Stock 3: GOOGL
Stock 4: TSLA
Stock 5: done

Data period (default 24): 24

Portfolio name: Tech Giants 2024

[Script fetches data and generates report...]

✓ Report saved to: portfolio_report_20241202_182500.txt
```

## What You Get

The analysis report includes:

1. **Asset Statistics**
   - Annual and monthly returns
   - Annual and monthly volatility

2. **Correlation Matrix**
   - How stocks move together
   - Diversification insights

3. **Covariance Matrix**
   - Risk relationships between assets

4. **Optimal Portfolios**
   - Maximum Sharpe Ratio (best risk-adjusted returns)
   - Minimum Variance (lowest risk)
   - Recommended allocations in percentages

5. **Capital Market Line (CML)**
   - Optimal risk-free/risky asset combinations
   - Expected returns at different risk levels

6. **Efficient Frontier**
   - Portfolio points along optimal frontier
   - Risk-return tradeoff visualization

7. **Key Insights**
   - Diversification analysis
   - Risk-return profile
   - Recommendations

## Troubleshooting

### "Invalid API key"
- Get your free API key: https://www.alphavantage.co/api/
- Make sure you copied it correctly (no spaces)

### "Rate limited"
- Alpha Vantage free tier: 5 requests per minute
- Wait a minute and try again
- Use fewer stocks (2-5 recommended)

### "No data found"
- Check stock ticker is correct (AAPL, not APPLE)
- Some tickers may not be available
- Try with major stocks: AAPL, MSFT, GOOGL, AMZN, TSLA

### Network errors
- Check your internet connection
- Alpha Vantage servers might be temporarily down
- Try again in a few minutes

## Using Programmatically

Instead of the interactive script, you can use the library directly:

```python
from data_fetcher import AlphaVantageAPI
from portfolio import PortfolioOptimizer
from report_generator import PortfolioReport

# Fetch data
api = AlphaVantageAPI("YOUR_API_KEY")
returns = api.get_returns_dataframe(['AAPL', 'MSFT', 'GOOGL'], months=24)

# Analyze
optimizer = PortfolioOptimizer(returns, risk_free_rate=0.045)

# Report
report = PortfolioReport(optimizer, portfolio_name="My Portfolio")
report.print_report()
report.save_report("my_analysis.txt")
```

## Next Steps

1. **Try it out**: Run with 3-5 favorite stocks
2. **Save reports**: All analysis is saved to text files
3. **Review insights**: Look at optimal allocations and risk metrics
4. **Iterate**: Try different stock combinations
5. **Learn**: Understand Modern Portfolio Theory concepts

## Project Structure

```
portfolio-optimizer/
├── main.py                 # Interactive CLI (START HERE)
├── data_fetcher.py         # Fetch live data from Alpha Vantage
├── portfolio.py            # Core optimization engine
├── report_generator.py     # Generate analysis reports
├── visualization.py        # Charts and graphs
├── example_data.py         # Sample data generators
├── example_analysis.py     # Example analysis script
├── requirements.txt        # Python dependencies
├── README.md              # Full documentation
└── SETUP.md               # This file
```

## Support

**Common Issues:**
- Typo in API key → Get new one from Alpha Vantage
- Stock ticker not found → Use official ticker (e.g., AAPL, not APPLE)
- Rate limit hit → Wait 1 minute, try with fewer stocks

**Questions?**
- Read README.md for detailed documentation
- Check example_analysis.py for code examples
- Review the generated report for interpretation help

Good luck with your portfolio analysis! 📊
