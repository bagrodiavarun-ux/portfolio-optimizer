# Portfolio Optimization: Formulas and Calculations

## Table of Contents
1. [Data Collection and Returns](#data-collection-and-returns)
2. [Risk and Return Metrics](#risk-and-return-metrics)
3. [Portfolio Statistics](#portfolio-statistics)
4. [Portfolio Optimization](#portfolio-optimization)
5. [Capital Market Line (CML)](#capital-market-line-cml)
6. [Security Market Line (SML) and CAPM](#security-market-line-sml-and-capm)
7. [Annualization Formulas](#annualization-formulas)

---

## 1. Data Collection and Returns

### 1.1 Daily Returns
Data source: Yahoo Finance (yfinance library)

**Formula:**
```
R_t = (P_t - P_{t-1}) / P_{t-1}
```

Where:
- `R_t` = Return on day t
- `P_t` = Adjusted close price on day t
- `P_{t-1}` = Adjusted close price on day t-1

**Implementation:** `data_fetcher_yfinance.py`, line 154
```python
returns_df = close_prices.pct_change().dropna()
```

### 1.2 Price Adjustment
Prices are automatically adjusted for stock splits and dividends using `auto_adjust=True` in yfinance.
This ensures accurate return calculations that reflect true investment performance.

---

## 2. Risk and Return Metrics

### 2.1 Expected Return (Daily)
**Formula:**
```
E[R] = (1/n) × Σ(R_i)
```

Where:
- `E[R]` = Expected daily return
- `n` = Number of observations
- `R_i` = Daily return on day i

**Implementation:** `portfolio.py`, line 29
```python
self.mean_returns = returns.mean()
```

### 2.2 Variance (Daily)
**Formula:**
```
σ² = (1/n) × Σ[(R_i - E[R])²]
```

Where:
- `σ²` = Daily variance
- `R_i` = Daily return on day i
- `E[R]` = Expected daily return
- `n` = Number of observations

### 2.3 Standard Deviation / Volatility (Daily)
**Formula:**
```
σ = √(σ²)
```

**Implementation:** `portfolio.py`, line 42
```python
self.std_devs = returns.std()
```

### 2.4 Covariance Matrix (Daily)
**Formula:**
```
Cov(R_i, R_j) = (1/n) × Σ[(R_{i,t} - E[R_i]) × (R_{j,t} - E[R_j])]
```

Where:
- `Cov(R_i, R_j)` = Covariance between asset i and asset j
- `R_{i,t}` = Return of asset i on day t
- `E[R_i]` = Expected return of asset i

**Implementation:** `portfolio.py`, line 30
```python
self.cov_matrix = returns.cov()
```

### 2.5 Correlation Matrix
**Formula:**
```
ρ(i,j) = Cov(R_i, R_j) / (σ_i × σ_j)
```

Where:
- `ρ(i,j)` = Correlation between asset i and asset j
- `σ_i` = Standard deviation of asset i
- `σ_j` = Standard deviation of asset j

**Implementation:** `portfolio.py`, line 43
```python
self.correlation_matrix = returns.corr()
```

---

## 3. Portfolio Statistics

### 3.1 Portfolio Return (Daily)
**Formula:**
```
R_p = Σ(w_i × R_i)
```

Where:
- `R_p` = Portfolio return
- `w_i` = Weight of asset i
- `R_i` = Expected return of asset i
- Constraint: Σ(w_i) = 1

**Implementation:** `portfolio.py`, line 71
```python
port_return = np.sum(self.mean_returns * weights)
```

### 3.2 Portfolio Variance (Daily)
**Formula:**
```
σ_p² = w^T × Cov × w
```

Matrix notation:
```
σ_p² = Σ_i Σ_j (w_i × w_j × Cov(R_i, R_j))
```

Where:
- `σ_p²` = Portfolio variance
- `w` = Weight vector [w_1, w_2, ..., w_n]
- `Cov` = Covariance matrix
- `w^T` = Transpose of weight vector

**Implementation:** `portfolio.py`, line 72
```python
variance = np.dot(weights.T, np.dot(self.cov_matrix, weights))
```

### 3.3 Portfolio Volatility (Daily)
**Formula:**
```
σ_p = √(σ_p²)
```

**Implementation:** `portfolio.py`, line 84
```python
port_std = np.sqrt(variance)
```

### 3.4 Sharpe Ratio (Daily)
**Formula:**
```
Sharpe = (R_p - R_f) / σ_p
```

Where:
- `R_p` = Portfolio return (daily)
- `R_f` = Risk-free rate (daily)
- `σ_p` = Portfolio volatility (daily)

**Implementation:** `portfolio.py`, line 90
```python
sharpe = (port_return - self.risk_free_rate) / port_std
```

**Note:** Risk-free rate is converted from annual to daily in line 23:
```python
self.risk_free_rate = risk_free_rate / 252
```

---

## 4. Portfolio Optimization

### 4.1 Maximum Sharpe Ratio Portfolio
**Objective:**
```
Maximize: Sharpe = (R_p - R_f) / σ_p
```

**Constraints:**
```
1. Σ(w_i) = 1         (weights sum to 1)
2. 0 ≤ w_i ≤ 0.40     (long-only, max 40% per asset)
```

**Implementation:** `portfolio.py`, lines 105-134
- Uses `scipy.optimize.minimize` with SLSQP method
- Minimizes negative Sharpe ratio (equivalent to maximizing Sharpe)

### 4.2 Minimum Variance Portfolio
**Objective:**
```
Minimize: σ_p = √(w^T × Cov × w)
```

**Constraints:**
```
1. Σ(w_i) = 1         (weights sum to 1)
2. 0 ≤ w_i ≤ 0.40     (long-only, max 40% per asset)
```

**Implementation:** `portfolio.py`, lines 138-167

### 4.3 Efficient Frontier
For each target return `R_target`:

**Objective:**
```
Minimize: σ_p
```

**Constraints:**
```
1. Σ(w_i) = 1         (weights sum to 1)
2. R_p = R_target     (achieve target return)
3. 0 ≤ w_i ≤ 0.40     (long-only, max 40% per asset)
```

**Implementation:** `portfolio.py`, lines 169-217
- Generates n_points portfolios between min and max asset returns

---

## 5. Capital Market Line (CML)

### 5.1 CML Equation
**Formula:**
```
E[R_p] = R_f + Sharpe_M × σ_p
```

Where:
- `E[R_p]` = Expected portfolio return
- `R_f` = Risk-free rate
- `Sharpe_M` = Sharpe ratio of market portfolio (max Sharpe portfolio)
- `σ_p` = Portfolio volatility

**Implementation:** `portfolio.py`, lines 280-295
```python
def expected_return(self, portfolio_volatility: float) -> float:
    # Convert annual volatility to daily
    daily_vol = portfolio_volatility / np.sqrt(252)
    # Calculate daily return using daily sharpe ratio
    daily_return = self.risk_free_rate_daily + self.sharpe_ratio_daily * daily_vol
    # Annualize the result
    return daily_return * 252
```

### 5.2 Required Volatility for Target Return
**Formula:**
```
σ_p = (E[R_p] - R_f) / Sharpe_M
```

**Implementation:** `portfolio.py`, line 309
```python
return (target_return - self.risk_free_rate_annual) / self.sharpe_ratio_annual
```

---

## 6. Security Market Line (SML) and CAPM

### 6.1 Beta Calculation
**Formula:**
```
β_i = Cov(R_i, R_M) / Var(R_M)
```

Where:
- `β_i` = Beta of asset i
- `R_i` = Returns of asset i
- `R_M` = Market returns (S&P 500)
- `Cov(R_i, R_M)` = Covariance between asset and market
- `Var(R_M)` = Variance of market

**Implementation:** `portfolio.py`, lines 332-344
```python
def calculate_beta(self, asset_returns: pd.Series,
                  market_returns: pd.Series) -> float:
    covariance = asset_returns.cov(market_returns)
    market_variance = market_returns.var()
    return covariance / market_variance
```

### 6.2 CAPM - Required Return
**Formula:**
```
E[R_i] = R_f + β_i × (E[R_M] - R_f)
```

Where:
- `E[R_i]` = Required return for asset i
- `R_f` = Risk-free rate
- `β_i` = Beta of asset i
- `E[R_M]` = Expected market return
- `(E[R_M] - R_f)` = Market risk premium

**Implementation:** `portfolio.py`, lines 355-357
```python
def required_return(self, beta: float) -> float:
    return self.risk_free_rate + beta * self.market_risk_premium
```

### 6.3 Jensen's Alpha
**Formula:**
```
α_i = R_i - [R_f + β_i × (R_M - R_f)]
α_i = R_i - E[R_i]
```

Where:
- `α_i` = Jensen's alpha for asset i
- `R_i` = Actual return of asset i
- `E[R_i]` = Required return (from CAPM)

**Interpretation:**
- `α > 0`: Asset is undervalued (outperforming expectations)
- `α < 0`: Asset is overvalued (underperforming expectations)

**Implementation:** `portfolio.py`, lines 346-353
```python
def calculate_alpha(self, asset_return: float, beta: float) -> float:
    required_return = self.risk_free_rate + beta * self.market_risk_premium
    return asset_return - required_return
```

---

## 7. Annualization Formulas

### 7.1 Annual Return from Daily Return
**Formula:**
```
R_annual = R_daily × 252
```

Where:
- 252 = approximate number of trading days per year

**Implementation:** Throughout report generation
```python
annual_return = daily_return * 252
```

### 7.2 Annual Volatility from Daily Volatility
**Formula:**
```
σ_annual = σ_daily × √252
```

**Rationale:** Variance scales linearly with time, so:
```
Var_annual = Var_daily × 252
σ_annual = √(Var_daily × 252) = σ_daily × √252
```

**Implementation:** Throughout report generation
```python
annual_volatility = daily_volatility * np.sqrt(252)
```

### 7.3 Annual Sharpe from Daily Sharpe
**Formula:**
```
Sharpe_annual = Sharpe_daily × √252
```

**Derivation:**
```
Sharpe_daily = (R_daily - R_f_daily) / σ_daily
Sharpe_annual = (R_annual - R_f_annual) / σ_annual
              = (R_daily × 252 - R_f_daily × 252) / (σ_daily × √252)
              = 252 × (R_daily - R_f_daily) / (σ_daily × √252)
              = (R_daily - R_f_daily) / σ_daily × (252 / √252)
              = Sharpe_daily × √252
```

**Implementation:** Throughout report generation
```python
annual_sharpe = daily_sharpe * np.sqrt(252)
```

### 7.4 Annual Covariance from Daily Covariance
**Formula:**
```
Cov_annual(i,j) = Cov_daily(i,j) × 252
```

**Note:** This follows from variance scaling linearly with time.

---

## 8. Key Implementation Details

### 8.1 Risk-Free Rate
- **Source:** US Treasury 10-year yield via Yahoo Finance (^TNX)
- **Conversion:** Annual rate divided by 252 for daily calculations
- **Code:** `data_fetcher_yfinance.py`, lines 12-34

### 8.2 Optimization Method
- **Library:** `scipy.optimize.minimize`
- **Algorithm:** SLSQP (Sequential Least Squares Programming)
- **Constraints:** Equality constraint (weights sum to 1), Bounds (0 ≤ w_i ≤ 0.40)

### 8.3 Position Size Constraint
- **Default:** Maximum 40% per asset
- **Purpose:** Prevent unrealistic portfolios from over-concentration
- **Configurable:** Can be changed via `max_position_size` parameter

---

## 9. Verification Checklist

To verify these calculations against external sources:

### 9.1 Basic Metrics
- [ ] Daily returns match percentage changes in adjusted prices
- [ ] Mean returns calculated correctly
- [ ] Standard deviations calculated correctly
- [ ] Covariance matrix is symmetric and positive semi-definite

### 9.2 Portfolio Calculations
- [ ] Portfolio return = weighted sum of individual returns
- [ ] Portfolio variance = w^T × Cov × w
- [ ] Sharpe ratio = (return - risk_free) / volatility

### 9.3 Annualization
- [ ] Annual return = daily return × 252
- [ ] Annual volatility = daily volatility × √252
- [ ] Annual Sharpe = daily Sharpe × √252

### 9.4 CAPM
- [ ] Beta = Cov(asset, market) / Var(market)
- [ ] Required return = risk_free + beta × market_premium
- [ ] Alpha = actual_return - required_return

### 9.5 Optimization
- [ ] Maximum Sharpe portfolio maximizes (R_p - R_f) / σ_p
- [ ] Minimum variance portfolio minimizes σ_p
- [ ] All weights sum to 1
- [ ] All weights are between 0 and max_position_size

---

## 10. References

### Academic References
1. **Modern Portfolio Theory:**
   - Markowitz, H. (1952). "Portfolio Selection". The Journal of Finance, 7(1), 77-91.

2. **Sharpe Ratio:**
   - Sharpe, W. F. (1966). "Mutual Fund Performance". The Journal of Business, 39(1), 119-138.

3. **Capital Asset Pricing Model (CAPM):**
   - Sharpe, W. F. (1964). "Capital Asset Prices: A Theory of Market Equilibrium under Conditions of Risk".
     The Journal of Finance, 19(3), 425-442.

4. **Efficient Frontier:**
   - Markowitz, H. (1959). "Portfolio Selection: Efficient Diversification of Investments".
     New York: John Wiley & Sons.

### Online Resources
- Investopedia: Portfolio Theory
- CFA Institute: Quantitative Methods
- Python for Finance (2nd Edition) by Yves Hilpisch

---

## Notes

1. **Trading Days:** We use 252 as the standard number of trading days per year (excluding weekends and holidays).

2. **Daily vs Annual:** All calculations are performed in daily space, then annualized for reporting.
   This maintains consistency and numerical accuracy.

3. **Long-Only Constraint:** We only allow positive weights (no short selling).

4. **Position Limits:** Maximum 40% allocation to any single asset prevents unrealistic concentration.

5. **Data Quality:** Yahoo Finance data is adjusted for splits and dividends, ensuring accurate historical returns.

---

**Generated:** 2025-12-03
**Portfolio Optimizer Version:** 1.0 with Position Constraints
**Python Libraries:** numpy, pandas, scipy, yfinance
