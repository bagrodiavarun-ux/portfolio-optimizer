"""
Formula Validation Script
Demonstrates all calculations step-by-step for verification.
"""

import numpy as np
import pandas as pd

print("=" * 80)
print("PORTFOLIO OPTIMIZATION - FORMULA VALIDATION")
print("=" * 80)

# ============================================================================
# 1. BASIC CALCULATIONS
# ============================================================================
print("\n" + "=" * 80)
print("1. BASIC RETURN AND RISK CALCULATIONS")
print("=" * 80)

# Sample price data
prices = np.array([100, 102, 101, 103, 105])
print(f"\nSample Prices: {prices}")

# Calculate daily returns
returns = np.diff(prices) / prices[:-1]
print(f"\nDaily Returns:")
for i, r in enumerate(returns):
    print(f"  Day {i+1}: {r:.6f} ({r*100:.4f}%)")

# Expected return (mean)
expected_return = np.mean(returns)
print(f"\nExpected Daily Return: {expected_return:.6f} ({expected_return*100:.4f}%)")

# Variance
variance = np.var(returns, ddof=1)  # ddof=1 for sample variance
print(f"Daily Variance: {variance:.6f}")

# Standard deviation (volatility)
volatility = np.std(returns, ddof=1)
print(f"Daily Volatility: {volatility:.6f} ({volatility*100:.4f}%)")

# Verify: volatility = sqrt(variance)
print(f"\nVerification: √(variance) = {np.sqrt(variance):.6f}")
print(f"Matches volatility: {np.isclose(volatility, np.sqrt(variance))}")

# ============================================================================
# 2. ANNUALIZATION
# ============================================================================
print("\n" + "=" * 80)
print("2. ANNUALIZATION (252 trading days)")
print("=" * 80)

trading_days = 252
annual_return = expected_return * trading_days
annual_volatility = volatility * np.sqrt(trading_days)

print(f"\nDaily Return:     {expected_return:.6f}")
print(f"Annual Return:    {annual_return:.6f} ({annual_return*100:.4f}%)")
print(f"Formula:          Daily × 252 = {expected_return:.6f} × 252")

print(f"\nDaily Volatility:  {volatility:.6f}")
print(f"Annual Volatility: {annual_volatility:.6f} ({annual_volatility*100:.4f}%)")
print(f"Formula:           Daily × √252 = {volatility:.6f} × {np.sqrt(trading_days):.4f}")

# ============================================================================
# 3. TWO-ASSET PORTFOLIO
# ============================================================================
print("\n" + "=" * 80)
print("3. TWO-ASSET PORTFOLIO EXAMPLE")
print("=" * 80)

# Asset statistics
r1, r2 = 0.10, 0.15  # Annual returns
s1, s2 = 0.20, 0.30  # Annual volatilities
rho = 0.40           # Correlation
w1, w2 = 0.60, 0.40  # Weights

print(f"\nAsset 1: Return = {r1*100:.1f}%, Volatility = {s1*100:.1f}%")
print(f"Asset 2: Return = {r2*100:.1f}%, Volatility = {s2*100:.1f}%")
print(f"Correlation: {rho:.2f}")
print(f"Weights: {w1*100:.1f}% / {w2*100:.1f}%")

# Portfolio return
port_return = w1 * r1 + w2 * r2
print(f"\nPortfolio Return:")
print(f"  R_p = w1×r1 + w2×r2")
print(f"      = {w1}×{r1} + {w2}×{r2}")
print(f"      = {port_return:.4f} ({port_return*100:.2f}%)")

# Covariance
cov_12 = rho * s1 * s2
print(f"\nCovariance:")
print(f"  Cov(1,2) = ρ × σ1 × σ2")
print(f"           = {rho} × {s1} × {s2}")
print(f"           = {cov_12:.4f}")

# Portfolio variance
port_variance = (w1**2 * s1**2 +
                 w2**2 * s2**2 +
                 2 * w1 * w2 * cov_12)
print(f"\nPortfolio Variance:")
print(f"  σ_p² = w1²×σ1² + w2²×σ2² + 2×w1×w2×Cov(1,2)")
print(f"       = {w1**2}×{s1**2} + {w2**2}×{s2**2} + 2×{w1}×{w2}×{cov_12}")
print(f"       = {port_variance:.6f}")

# Portfolio volatility
port_volatility = np.sqrt(port_variance)
print(f"\nPortfolio Volatility:")
print(f"  σ_p = √(σ_p²)")
print(f"      = √{port_variance:.6f}")
print(f"      = {port_volatility:.4f} ({port_volatility*100:.2f}%)")

# ============================================================================
# 4. MATRIX FORM (3 ASSETS)
# ============================================================================
print("\n" + "=" * 80)
print("4. PORTFOLIO VARIANCE - MATRIX FORM (3 ASSETS)")
print("=" * 80)

# Three assets
weights = np.array([0.50, 0.30, 0.20])
returns_vec = np.array([0.10, 0.15, 0.08])

# Covariance matrix
cov_matrix = np.array([
    [0.040, 0.020, 0.015],
    [0.020, 0.090, 0.025],
    [0.015, 0.025, 0.050]
])

print(f"\nWeights: {weights}")
print(f"Expected Returns: {returns_vec}")
print(f"\nCovariance Matrix:")
print(cov_matrix)

# Portfolio return
port_ret_matrix = np.dot(weights, returns_vec)
print(f"\nPortfolio Return:")
print(f"  R_p = w^T × R")
print(f"      = {weights} · {returns_vec}")
print(f"      = {port_ret_matrix:.4f} ({port_ret_matrix*100:.2f}%)")

# Portfolio variance
port_var_matrix = np.dot(weights.T, np.dot(cov_matrix, weights))
print(f"\nPortfolio Variance:")
print(f"  σ_p² = w^T × Cov × w")
print(f"       = {port_var_matrix:.6f}")

port_vol_matrix = np.sqrt(port_var_matrix)
print(f"\nPortfolio Volatility:")
print(f"  σ_p = {port_vol_matrix:.4f} ({port_vol_matrix*100:.2f}%)")

# ============================================================================
# 5. SHARPE RATIO
# ============================================================================
print("\n" + "=" * 80)
print("5. SHARPE RATIO CALCULATION")
print("=" * 80)

risk_free = 0.04  # 4% annual risk-free rate
print(f"\nPortfolio Return:  {port_ret_matrix*100:.2f}%")
print(f"Risk-Free Rate:    {risk_free*100:.2f}%")
print(f"Portfolio Volatility: {port_vol_matrix*100:.2f}%")

sharpe_ratio = (port_ret_matrix - risk_free) / port_vol_matrix
print(f"\nSharpe Ratio:")
print(f"  Sharpe = (R_p - R_f) / σ_p")
print(f"         = ({port_ret_matrix:.4f} - {risk_free:.4f}) / {port_vol_matrix:.4f}")
print(f"         = {sharpe_ratio:.4f}")

# ============================================================================
# 6. DAILY TO ANNUAL SHARPE
# ============================================================================
print("\n" + "=" * 80)
print("6. SHARPE RATIO ANNUALIZATION")
print("=" * 80)

# Assume we have daily Sharpe
daily_return = 0.0004  # 0.04% per day
daily_volatility = 0.012  # 1.2% per day
daily_rf = risk_free / 252

daily_sharpe = (daily_return - daily_rf) / daily_volatility
print(f"\nDaily Sharpe: {daily_sharpe:.6f}")

# Method 1: Direct annualization
annual_sharpe_method1 = daily_sharpe * np.sqrt(252)
print(f"\nMethod 1 (Direct):")
print(f"  Annual Sharpe = Daily Sharpe × √252")
print(f"                = {daily_sharpe:.6f} × {np.sqrt(252):.4f}")
print(f"                = {annual_sharpe_method1:.4f}")

# Method 2: Calculate from annualized values
annual_ret = daily_return * 252
annual_vol = daily_volatility * np.sqrt(252)
annual_sharpe_method2 = (annual_ret - risk_free) / annual_vol
print(f"\nMethod 2 (From annualized values):")
print(f"  Annual Return = {annual_ret:.4f}")
print(f"  Annual Vol    = {annual_vol:.4f}")
print(f"  Annual Sharpe = ({annual_ret:.4f} - {risk_free:.4f}) / {annual_vol:.4f}")
print(f"                = {annual_sharpe_method2:.4f}")

print(f"\nMethods match: {np.isclose(annual_sharpe_method1, annual_sharpe_method2)}")

# ============================================================================
# 7. CAPM / BETA / ALPHA
# ============================================================================
print("\n" + "=" * 80)
print("7. CAPM, BETA, AND ALPHA")
print("=" * 80)

# Sample data
asset_returns = np.array([0.02, -0.01, 0.03, 0.01, 0.04])
market_returns = np.array([0.015, -0.005, 0.025, 0.008, 0.035])

print(f"\nAsset Returns:  {asset_returns}")
print(f"Market Returns: {market_returns}")

# Beta calculation
cov_asset_market = np.cov(asset_returns, market_returns)[0, 1]
var_market = np.var(market_returns, ddof=1)
beta = cov_asset_market / var_market

print(f"\nBeta Calculation:")
print(f"  Cov(Asset, Market) = {cov_asset_market:.6f}")
print(f"  Var(Market)        = {var_market:.6f}")
print(f"  Beta = Cov / Var   = {beta:.4f}")

# CAPM - Required return
avg_asset_return = np.mean(asset_returns)
avg_market_return = np.mean(market_returns)
daily_rf_rate = risk_free / 252
market_premium = avg_market_return - daily_rf_rate

required_return = daily_rf_rate + beta * market_premium
print(f"\nCAPM - Required Return:")
print(f"  Market Risk Premium = {market_premium:.6f}")
print(f"  Required Return = R_f + β × (R_M - R_f)")
print(f"                  = {daily_rf_rate:.6f} + {beta:.4f} × {market_premium:.6f}")
print(f"                  = {required_return:.6f}")

# Alpha (Jensen's Alpha)
alpha = avg_asset_return - required_return
print(f"\nJensen's Alpha:")
print(f"  Actual Return   = {avg_asset_return:.6f}")
print(f"  Required Return = {required_return:.6f}")
print(f"  Alpha = Actual - Required")
print(f"        = {alpha:.6f}")

if alpha > 0:
    print(f"  Interpretation: UNDERVALUED (α > 0)")
elif alpha < 0:
    print(f"  Interpretation: OVERVALUED (α < 0)")
else:
    print(f"  Interpretation: FAIRLY VALUED (α = 0)")

# ============================================================================
# 8. CAPITAL MARKET LINE
# ============================================================================
print("\n" + "=" * 80)
print("8. CAPITAL MARKET LINE (CML)")
print("=" * 80)

# Market portfolio stats
market_return_annual = 0.12
market_vol_annual = 0.18
risk_free_annual = 0.04

sharpe_market = (market_return_annual - risk_free_annual) / market_vol_annual
print(f"\nMarket Portfolio:")
print(f"  Return:     {market_return_annual*100:.1f}%")
print(f"  Volatility: {market_vol_annual*100:.1f}%")
print(f"  Sharpe:     {sharpe_market:.4f}")

# CML for different portfolio volatilities
print(f"\nCapital Market Line:")
print(f"  Formula: E[R_p] = R_f + Sharpe_M × σ_p")
print(f"\n  Portfolio Vol    Expected Return")
print(f"  -------------    ---------------")
for vol in [0.05, 0.10, 0.15, 0.20, 0.25]:
    expected_ret = risk_free_annual + sharpe_market * vol
    print(f"  {vol*100:5.0f}%           {expected_ret*100:6.2f}%")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("VALIDATION COMPLETE")
print("=" * 80)
print("\nAll formulas demonstrated:")
print("  ✓ Daily returns and volatility")
print("  ✓ Annualization (×252 for returns, ×√252 for volatility)")
print("  ✓ Portfolio return (weighted sum)")
print("  ✓ Portfolio variance (matrix form)")
print("  ✓ Sharpe ratio")
print("  ✓ Beta and Alpha (CAPM)")
print("  ✓ Capital Market Line")
print("\nCompare these calculations with:")
print("  - FORMULAS_AND_CALCULATIONS.md (detailed explanations)")
print("  - FORMULAS_QUICK_REFERENCE.txt (quick lookup)")
print("  - Your actual portfolio results")
print("\n" + "=" * 80)
