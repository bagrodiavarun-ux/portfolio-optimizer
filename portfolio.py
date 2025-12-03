import numpy as np
import pandas as pd
from scipy.optimize import minimize
from typing import Tuple, Dict, List


class PortfolioOptimizer:
    """
    Portfolio optimization engine that calculates efficient frontiers,
    Sharpe ratios, and performance metrics for multi-asset portfolios.
    """

    def __init__(self, returns: pd.DataFrame, risk_free_rate: float = 0.025):
        """
        Initialize portfolio optimizer.

        Args:
            returns: DataFrame with asset returns (rows: dates, columns: assets) - DAILY returns
            risk_free_rate: Annual risk-free rate (default 2.5%)
        """
        self.returns = returns
        # Convert annual risk-free rate to daily rate (for use with daily returns)
        self.risk_free_rate = risk_free_rate / 252
        self.annual_risk_free_rate = risk_free_rate
        self.assets = returns.columns.tolist()
        self.n_assets = len(self.assets)

        # Calculate statistics (daily)
        self.mean_returns = returns.mean()
        self.cov_matrix = returns.cov()
        self.std_devs = returns.std()
        self.correlation_matrix = returns.corr()

    def portfolio_stats(self, weights: np.ndarray) -> Tuple[float, float, float]:
        """
        Calculate portfolio return, volatility, and Sharpe ratio.

        Args:
            weights: Array of portfolio weights (must sum to 1)

        Returns:
            Tuple of (return, volatility, sharpe_ratio)
        """
        port_return = np.sum(self.mean_returns * weights)
        port_std = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))
        sharpe = (port_return - self.risk_free_rate) / port_std

        return port_return, port_std, sharpe

    def _negative_sharpe(self, weights: np.ndarray) -> float:
        """Negative Sharpe for minimization."""
        return -self.portfolio_stats(weights)[2]

    def _portfolio_volatility(self, weights: np.ndarray) -> float:
        """Portfolio volatility for minimization."""
        return self.portfolio_stats(weights)[1]

    def max_sharpe_portfolio(self) -> Dict:
        """
        Find portfolio that maximizes Sharpe ratio.

        Returns:
            Dict with weights, return, volatility, and Sharpe ratio
        """
        constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        bounds = tuple((0, 1) for _ in range(self.n_assets))
        initial_guess = np.array([1 / self.n_assets] * self.n_assets)

        result = minimize(
            self._negative_sharpe,
            initial_guess,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )

        weights = result.x
        port_return, port_vol, sharpe = self.portfolio_stats(weights)

        return {
            'weights': dict(zip(self.assets, weights)),
            'return': port_return,
            'volatility': port_vol,
            'sharpe_ratio': sharpe
        }

    def min_variance_portfolio(self) -> Dict:
        """
        Find portfolio with minimum variance.

        Returns:
            Dict with weights, return, volatility, and Sharpe ratio
        """
        constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        bounds = tuple((0, 1) for _ in range(self.n_assets))
        initial_guess = np.array([1 / self.n_assets] * self.n_assets)

        result = minimize(
            self._portfolio_volatility,
            initial_guess,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )

        weights = result.x
        port_return, port_vol, sharpe = self.portfolio_stats(weights)

        return {
            'weights': dict(zip(self.assets, weights)),
            'return': port_return,
            'volatility': port_vol,
            'sharpe_ratio': sharpe
        }

    def efficient_frontier(self, n_points: int = 100) -> pd.DataFrame:
        """
        Generate efficient frontier by optimizing for target returns.

        Args:
            n_points: Number of portfolios to generate along frontier

        Returns:
            DataFrame with return, volatility, and Sharpe ratio for each point
        """
        min_return = self.mean_returns.min()
        max_return = self.mean_returns.max()
        target_returns = np.linspace(min_return, max_return, n_points)

        frontier_portfolios = []

        for target_return in target_returns:
            constraints = [
                {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                {'type': 'eq', 'fun': lambda x: np.sum(self.mean_returns * x) - target_return}
            ]
            bounds = tuple((0, 1) for _ in range(self.n_assets))
            initial_guess = np.array([1 / self.n_assets] * self.n_assets)

            result = minimize(
                self._portfolio_volatility,
                initial_guess,
                method='SLSQP',
                bounds=bounds,
                constraints=constraints,
                options={'ftol': 1e-9}
            )

            if result.success:
                weights = result.x
                port_return, port_vol, sharpe = self.portfolio_stats(weights)
                frontier_portfolios.append({
                    'return': port_return,
                    'volatility': port_vol,
                    'sharpe_ratio': sharpe
                })

        return pd.DataFrame(frontier_portfolios)

    def portfolio_for_target_return(self, target_return: float) -> Dict:
        """
        Find minimum variance portfolio for a target return.

        Args:
            target_return: Target annual return

        Returns:
            Dict with weights, return, volatility, and Sharpe ratio
        """
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
            {'type': 'eq', 'fun': lambda x: np.sum(self.mean_returns * x) - target_return}
        ]
        bounds = tuple((0, 1) for _ in range(self.n_assets))
        initial_guess = np.array([1 / self.n_assets] * self.n_assets)

        result = minimize(
            self._portfolio_volatility,
            initial_guess,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )

        weights = result.x
        port_return, port_vol, sharpe = self.portfolio_stats(weights)

        return {
            'weights': dict(zip(self.assets, weights)),
            'return': port_return,
            'volatility': port_vol,
            'sharpe_ratio': sharpe
        }


class CapitalMarketLine:
    """Calculate and analyze the Capital Market Line (CML)."""

    def __init__(self, max_sharpe_portfolio: Dict, risk_free_rate: float):
        """
        Initialize CML.

        Args:
            max_sharpe_portfolio: Dict with 'return', 'volatility', 'sharpe_ratio'
            risk_free_rate: Annual risk-free rate
        """
        self.market_return = max_sharpe_portfolio['return']
        self.market_volatility = max_sharpe_portfolio['volatility']
        self.risk_free_rate = risk_free_rate
        self.sharpe_ratio = max_sharpe_portfolio['sharpe_ratio']

    def expected_return(self, portfolio_volatility: float) -> float:
        """Calculate expected return for a given volatility on the CML."""
        return self.risk_free_rate + self.sharpe_ratio * portfolio_volatility

    def required_volatility(self, target_return: float) -> float:
        """Calculate required volatility to achieve target return on the CML."""
        if target_return < self.risk_free_rate:
            return 0
        return (target_return - self.risk_free_rate) / self.sharpe_ratio


class SecurityMarketLine:
    """Calculate and analyze the Security Market Line (SML)."""

    def __init__(self, market_return: float, market_volatility: float,
                 risk_free_rate: float, asset_returns: pd.DataFrame):
        """
        Initialize SML.

        Args:
            market_return: Market portfolio annual return
            market_volatility: Market portfolio volatility
            risk_free_rate: Annual risk-free rate
            asset_returns: DataFrame with asset returns
        """
        self.market_return = market_return
        self.market_volatility = market_volatility
        self.risk_free_rate = risk_free_rate
        self.asset_returns = asset_returns
        self.market_risk_premium = market_return - risk_free_rate

    def calculate_beta(self, asset_returns: pd.Series,
                      market_returns: pd.Series) -> float:
        """
        Calculate beta for an asset relative to the market.

        Beta = Cov(Asset, Market) / Var(Market)
        """
        covariance = asset_returns.cov(market_returns)
        market_variance = market_returns.var()
        return covariance / market_variance

    def calculate_alpha(self, asset_return: float, beta: float) -> float:
        """
        Calculate alpha (Jensen's alpha).

        Alpha = Asset Return - [Risk-Free Rate + Beta * (Market Return - Risk-Free Rate)]
        """
        required_return = self.risk_free_rate + beta * self.market_risk_premium
        return asset_return - required_return

    def required_return(self, beta: float) -> float:
        """Calculate required return for an asset given its beta."""
        return self.risk_free_rate + beta * self.market_risk_premium

    def analyze_assets(self, market_proxy: pd.Series) -> pd.DataFrame:
        """
        Analyze all assets in the portfolio.

        Args:
            market_proxy: Series representing market returns (e.g., S&P 500)

        Returns:
            DataFrame with beta, alpha, expected return for each asset
        """
        analysis = []

        for asset in self.asset_returns.columns:
            asset_ret = self.asset_returns[asset]
            beta = self.calculate_beta(asset_ret, market_proxy)
            alpha = self.calculate_alpha(asset_ret.mean(), beta)
            req_return = self.required_return(beta)

            analysis.append({
                'asset': asset,
                'beta': beta,
                'alpha': alpha,
                'expected_return': asset_ret.mean(),
                'required_return': req_return,
                'valuation': 'Undervalued' if alpha > 0 else 'Overvalued'
            })

        return pd.DataFrame(analysis)
