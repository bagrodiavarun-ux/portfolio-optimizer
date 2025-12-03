# Portfolio Optimizer - Execution Workflow

## Complete User Flow

### 1. Initial Setup (One-time)

```bash
# Clone or navigate to project
cd ~/portfolio-optimizer

# Install dependencies
pip install -r requirements.txt

# Get free API key
# Go to: https://www.alphavantage.co/api/
# Enter email, get key instantly
```

### 2. Set API Key (Every session)

Option A - Environment variable (recommended):
```bash
export ALPHA_VANTAGE_API_KEY="your_key_here"
python3 main.py
```

Option B - Enter when prompted:
```bash
python3 main.py
# Script asks for key on startup
```

### 3. Interactive Analysis Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. START: python3 main.py                                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 2. API KEY VALIDATION                                           │
│    - Check environment variable                                 │
│    - Or ask user to enter                                       │
│    - Validate with test API call                                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 3. STOCK SELECTION                                              │
│    Stock 1: AAPL                                                │
│    Stock 2: MSFT                                                │
│    Stock 3: GOOGL                                               │
│    Stock 4: TSLA                                                │
│    Stock 5: done                                                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 4. DATA PERIOD SELECTION                                        │
│    How many months? (default 24): 24                            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 5. PORTFOLIO NAMING                                             │
│    Portfolio name (default My Portfolio): Tech Giants           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 6. DATA FETCHING (AlphaVantageAPI)                              │
│    Fetching data for AAPL... ✓ 504 days                        │
│    Fetching data for MSFT... ✓ 504 days                        │
│    Fetching data for GOOGL... ✓ 504 days                       │
│    Fetching data for TSLA... ✓ 504 days                        │
│    ✓ Successfully fetched 4 stocks                             │
│    ✓ Data range: 2022-12-02 to 2024-12-02                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 7. PORTFOLIO OPTIMIZATION (PortfolioOptimizer)                  │
│    Calculating efficient frontier...                            │
│    Calculating Sharpe ratio portfolio...                        │
│    Calculating minimum variance portfolio...                    │
│    ✓ Optimization complete!                                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 8. REPORT GENERATION (PortfolioReport)                          │
│    Generating asset statistics...                              │
│    Generating correlation analysis...                          │
│    Calculating optimal allocations...                          │
│    Building Capital Market Line...                             │
│    Creating efficient frontier...                              │
│    Generating insights...                                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 9. OUTPUT: REPORT DISPLAY & SAVE                                │
│    ✓ Report printed to console                                 │
│    ✓ Report saved to: portfolio_report_20241202_182500.txt     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 10. END: Analysis complete!                                     │
│     Review report and make investment decisions                 │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌─────────────────┐
│  User Input     │
│  - Stock tickers│
│  - Time period  │
└────────┬────────┘
         │
         ↓
┌──────────────────────────────────────────┐
│  AlphaVantageAPI                         │
│  ├─ HTTP requests to API                 │
│  ├─ Parse JSON response                  │
│  └─ Calculate daily returns              │
└────────┬─────────────────────────────────┘
         │
         ↓
┌──────────────────────────────────────────┐
│  Returns DataFrame                       │
│  ├─ Date index                           │
│  ├─ Stock columns (daily returns %)      │
│  └─ 500+ rows of historical data         │
└────────┬─────────────────────────────────┘
         │
         ↓
┌──────────────────────────────────────────┐
│  PortfolioOptimizer                      │
│  ├─ Calculate statistics                 │
│  ├─ Build covariance matrix              │
│  ├─ Optimize Sharpe ratio                │
│  ├─ Generate efficient frontier          │
│  └─ Calculate all metrics                │
└────────┬─────────────────────────────────┘
         │
         ↓
┌──────────────────────────────────────────┐
│  PortfolioReport                         │
│  ├─ Format asset statistics              │
│  ├─ Build tables (correlations, etc.)    │
│  ├─ Generate insights                    │
│  └─ Combine into report                  │
└────────┬─────────────────────────────────┘
         │
         ↓
┌──────────────────────────────────────────┐
│  Output                                  │
│  ├─ Print to console                     │
│  └─ Save to file (.txt)                  │
└──────────────────────────────────────────┘
```

## Code Execution Path

```python
# main.py (Entry point)
def main():
    # Step 1: Get API key
    api_key = get_api_key()

    # Step 2: Get user inputs
    symbols = get_stock_symbols()        # ["AAPL", "MSFT", "GOOGL", "TSLA"]
    months = get_data_period()           # 24
    portfolio_name = get_portfolio_name()  # "Tech Giants"

    # Step 3: Fetch data
    api = AlphaVantageAPI(api_key)
    returns_df = api.get_returns_dataframe(symbols, months=months)
    # Returns: DataFrame with shape (500, 4) - 500 trading days, 4 stocks

    # Step 4: Optimize portfolio
    optimizer = PortfolioOptimizer(returns_df, risk_free_rate=0.045)
    # Now optimizer has:
    # - Mean returns per stock
    # - Covariance matrix
    # - Correlation matrix
    # - 10+ optimization methods

    # Step 5: Generate report
    report = PortfolioReport(optimizer, portfolio_name=portfolio_name)

    # Step 6: Output
    report.print_report()      # Print to console
    report.save_report()       # Save to file
```

## Example: What Gets Calculated

For portfolio of AAPL, MSFT, GOOGL, TSLA:

```
STEP 1: Data Fetching
├─ AAPL: 504 days of prices
├─ MSFT: 504 days of prices
├─ GOOGL: 504 days of prices
└─ TSLA: 504 days of prices
  Result: 503 daily returns per stock

STEP 2: Asset Statistics
├─ AAPL: 28.5% annual return, 34.2% volatility
├─ MSFT: 29.8% annual return, 31.6% volatility
├─ GOOGL: 26.8% annual return, 29.9% volatility
└─ TSLA: 42.5% annual return, 48.8% volatility

STEP 3: Risk Relationships
├─ Correlation Matrix (4x4):
│  ├─ AAPL-MSFT: 0.652
│  ├─ AAPL-GOOGL: 0.623
│  ├─ AAPL-TSLA: 0.541
│  └─ ... (6 total correlations)
└─ Covariance Matrix (4x4) - Annualized

STEP 4: Optimization
├─ Max Sharpe Portfolio:
│  ├─ AAPL: 22.5%
│  ├─ MSFT: 28.3%
│  ├─ GOOGL: 25.1%
│  ├─ TSLA: 24.1%
│  ├─ Expected Return: 31.8%
│  ├─ Volatility: 28.5%
│  └─ Sharpe Ratio: 0.9347
│
└─ Min Variance Portfolio:
   ├─ AAPL: 18.2%
   ├─ MSFT: 32.1%
   ├─ GOOGL: 28.7%
   ├─ TSLA: 21.0%
   ├─ Expected Return: 29.4%
   ├─ Volatility: 27.1%
   └─ Sharpe Ratio: 0.8621

STEP 5: Capital Market Line
├─ Risk-free rate: 4.5%
├─ Market return: 31.8%
├─ Market volatility: 28.5%
├─ Market Sharpe: 0.9347
└─ For 20% volatility → 18.5% expected return

STEP 6: Efficient Frontier
├─ 20 portfolio points along optimal frontier
├─ Range: 27.1% - 42.5% volatility
└─ Range: 29.4% - 42.5% return

STEP 7: Insights
├─ Diversification benefit: 15.2%
├─ Risk reduction vs equal-weight: 3.2%
├─ Best risk-adjusted returns in Max Sharpe
└─ Recommendation: Use Max Sharpe allocation
```

## Performance Characteristics

```
Operation                          Time
─────────────────────────────────────────
API calls (4 stocks × 24 months)   8-12 sec
Data processing & cleaning         0.5 sec
Optimization calculations          2-3 sec
Report generation                  1 sec
─────────────────────────────────────────
Total end-to-end                   12-17 sec
```

## Error Handling Flow

```
Invalid API Key
  → User enters key
  → Validate with test call
  → If invalid: ask again
  → If valid: continue

Rate Limited
  → Wait 1 minute
  → Retry request
  → If still limited: inform user

Network Error
  → Inform user
  → Ask to retry
  → Continue if possible

Stock Not Found
  → Skip that stock
  → Continue with others
  → Warn user about failures

Insufficient Data
  → Need minimum 2 stocks
  → Need minimum 6 months data
  → Inform user if not met
```

## File Outputs

After running analysis, you get:

```
~/portfolio-optimizer/
├── portfolio_report_20241202_182500.txt
│   └─ 500+ lines of detailed analysis
├── portfolio_report_20241202_190000.txt
│   └─ (Another analysis if run again)
└── ... (new report each time you run)
```

Each report contains:
- 7 major sections
- Tables with statistics
- Optimal allocations
- Risk analysis
- Key insights
- Investment recommendations

---

**The entire workflow takes 15-20 seconds from pressing Enter to getting a professional analysis report.**
