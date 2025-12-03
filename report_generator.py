"""
Generate comprehensive portfolio analysis reports.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from portfolio import PortfolioOptimizer, CapitalMarketLine, SecurityMarketLine


class PortfolioReport:
    """Generate formatted portfolio analysis reports."""

    def __init__(self, optimizer: PortfolioOptimizer, portfolio_name: str = "Portfolio Analysis"):
        """
        Initialize report generator.

        Args:
            optimizer: PortfolioOptimizer instance with loaded data
            portfolio_name: Name of the portfolio being analyzed
        """
        self.optimizer = optimizer
        self.portfolio_name = portfolio_name
        self.timestamp = datetime.now()

    def _section_header(self, title: str) -> str:
        """Format section header."""
        return f"\n{'=' * 80}\n{title}\n{'=' * 80}\n"

    def _subsection_header(self, title: str) -> str:
        """Format subsection header."""
        return f"\n{title}\n{'-' * len(title)}\n"

    def asset_statistics(self) -> str:
        """Generate asset statistics section."""
        output = self._section_header("1. ASSET STATISTICS")

        stats = pd.DataFrame({
            'Annual Return': self.optimizer.mean_returns * 252,
            'Annual Volatility': self.optimizer.std_devs * np.sqrt(252),
            'Monthly Return': self.optimizer.mean_returns,
            'Monthly Volatility': self.optimizer.std_devs,
        })

        output += stats.to_string()
        output += "\n"

        return output

    def correlation_analysis(self) -> str:
        """Generate correlation matrix."""
        output = self._section_header("2. CORRELATION MATRIX")

        output += self.optimizer.correlation_matrix.to_string()
        output += "\n"

        # Summary statistics
        output += self._subsection_header("Correlation Summary")
        output += f"Highest Correlation: {self.optimizer.correlation_matrix.values[np.triu_indices_from(self.optimizer.correlation_matrix.values, k=1)].max():.4f}\n"
        output += f"Lowest Correlation: {self.optimizer.correlation_matrix.values[np.triu_indices_from(self.optimizer.correlation_matrix.values, k=1)].min():.4f}\n"

        return output

    def covariance_analysis(self) -> str:
        """Generate covariance matrix."""
        output = self._section_header("3. COVARIANCE MATRIX (Annual)")

        # Annualize covariance
        annual_cov = self.optimizer.cov_matrix * 252

        output += annual_cov.to_string()
        output += "\n"

        return output

    def optimal_portfolios(self) -> str:
        """Generate optimal portfolio recommendations."""
        output = self._section_header("4. OPTIMAL PORTFOLIOS")

        max_sharpe = self.optimizer.max_sharpe_portfolio()
        min_var = self.optimizer.min_variance_portfolio()

        # Max Sharpe Portfolio
        output += self._subsection_header("A. Maximum Sharpe Ratio Portfolio (Best Risk-Adjusted Returns)")

        output += "Allocation:\n"
        weights_series = pd.Series(max_sharpe['weights']).sort_values(ascending=False)
        for asset, weight in weights_series.items():
            if weight > 0.001:
                output += f"  {asset:12s}: {weight:7.2%}\n"

        output += f"\nExpected Annual Return:     {max_sharpe['return'] * 252:7.2%}\n"
        output += f"Expected Annual Volatility: {max_sharpe['volatility'] * np.sqrt(252):7.2%}\n"
        output += f"Sharpe Ratio (Annual):      {max_sharpe['sharpe_ratio'] * np.sqrt(252):7.4f}\n"

        # Min Variance Portfolio
        output += self._subsection_header("B. Minimum Variance Portfolio (Lowest Risk)")

        output += "Allocation:\n"
        weights_series = pd.Series(min_var['weights']).sort_values(ascending=False)
        for asset, weight in weights_series.items():
            if weight > 0.001:
                output += f"  {asset:12s}: {weight:7.2%}\n"

        output += f"\nExpected Annual Return:     {min_var['return'] * 252:7.2%}\n"
        output += f"Expected Annual Volatility: {min_var['volatility'] * np.sqrt(252):7.2%}\n"
        output += f"Sharpe Ratio (Annual):      {min_var['sharpe_ratio'] * np.sqrt(252):7.4f}\n"

        return output

    def capital_market_line(self) -> str:
        """Generate Capital Market Line analysis."""
        output = self._section_header("5. CAPITAL MARKET LINE (CML) ANALYSIS")

        max_sharpe = self.optimizer.max_sharpe_portfolio()
        cml = CapitalMarketLine(max_sharpe, self.optimizer.annual_risk_free_rate)

        output += f"Risk-Free Rate:             {self.optimizer.annual_risk_free_rate:7.2%} (annual)\n"
        output += f"Market Portfolio Return:    {cml.market_return_annual:7.2%} (annual)\n"
        output += f"Market Portfolio Volatility: {cml.market_volatility_annual:7.2%} (annual)\n"
        output += f"Sharpe Ratio (Market):      {cml.sharpe_ratio_annual:7.4f}\n"

        output += self._subsection_header("CML Implied Returns for Different Risk Levels")

        risk_levels = [0.10, 0.15, 0.20, 0.25, 0.30]
        output += f"{'Volatility':<15} {'Expected Return':<20}\n"
        for vol in risk_levels:
            ret = cml.expected_return(vol)
            output += f"{vol:>13.1%}  {ret:>18.2%}\n"

        return output

    def efficient_frontier_summary(self) -> str:
        """Generate efficient frontier summary."""
        output = self._section_header("6. EFFICIENT FRONTIER")

        frontier = self.optimizer.efficient_frontier(n_points=20)

        output += "Portfolio Points on Efficient Frontier:\n"
        output += f"{'Return':<15} {'Volatility':<15} {'Sharpe Ratio':<15}\n"

        for idx in range(0, len(frontier), len(frontier) // 5):
            row = frontier.iloc[idx]
            output += f"{row['return']*252:>13.2%}  {row['volatility']*np.sqrt(252):>13.2%}  {row['sharpe_ratio']*np.sqrt(252):>13.4f}\n"

        return output

    def key_insights(self) -> str:
        """Generate key insights and recommendations."""
        output = self._section_header("7. KEY INSIGHTS & RECOMMENDATIONS")

        max_sharpe = self.optimizer.max_sharpe_portfolio()
        min_var = self.optimizer.min_variance_portfolio()

        output += "• Diversification Analysis:\n"
        output += f"  - Number of assets: {len(self.optimizer.assets)}\n"
        output += f"  - Average correlation: {self.optimizer.correlation_matrix.values[np.triu_indices_from(self.optimizer.correlation_matrix.values, k=1)].mean():.4f}\n"

        output += "\n• Risk-Return Profile:\n"
        # Only show Sharpe ratio comparison if both are positive
        max_sharpe_annual = max_sharpe['sharpe_ratio'] * np.sqrt(252)
        min_var_annual = min_var['sharpe_ratio'] * np.sqrt(252)
        if min_var_annual > 0 and max_sharpe_annual > min_var_annual:
            output += f"  - Max Sharpe portfolio offers {max_sharpe_annual/min_var_annual:.2f}x better risk-adjusted returns\n"
        elif max_sharpe_annual > 0:
            output += f"  - Max Sharpe portfolio Sharpe ratio: {max_sharpe_annual:.4f}\n"
            output += f"  - Min Variance portfolio Sharpe ratio: {min_var_annual:.4f}\n"
        output += f"  - Risk difference: {(max_sharpe['volatility'] - min_var['volatility'])*np.sqrt(252):.2%}\n"

        output += "\n• Recommendation:\n"
        # Use annualized Sharpe ratio (>1.0 is generally considered good)
        max_sharpe_annual = max_sharpe['sharpe_ratio'] * np.sqrt(252)
        if max_sharpe_annual > 1.0:
            output += "  ✓ Strong risk-adjusted returns available in this portfolio\n"
        elif max_sharpe_annual > 0.5:
            output += "  ⚠ Moderate risk-adjusted returns; consider diversification\n"
        else:
            output += "  ✗ Poor risk-adjusted returns; portfolio may not be suitable\n"

        return output

    def generate_full_report(self) -> str:
        """Generate complete portfolio report."""
        report = ""

        # Header
        report += f"\n{'PORTFOLIO ANALYSIS REPORT':^80}\n"
        report += f"{self.portfolio_name:^80}\n"
        report += f"{self.timestamp.strftime('%B %d, %Y at %H:%M:%S'):^80}\n"

        # Sections
        report += self.asset_statistics()
        report += self.correlation_analysis()
        report += self.covariance_analysis()
        report += self.optimal_portfolios()
        report += self.capital_market_line()
        report += self.efficient_frontier_summary()
        report += self.key_insights()

        # Footer
        report += self._section_header("END OF REPORT")
        report += "This report is generated automatically from market data.\n"
        report += "Past performance is not indicative of future results.\n"

        return report

    def save_report(self, filename: str = None) -> str:
        """
        Generate and save report to file.

        Args:
            filename: Output filename (default: portfolio_report_TIMESTAMP.txt)

        Returns:
            Path to saved report
        """
        if filename is None:
            timestamp = self.timestamp.strftime("%Y%m%d_%H%M%S")
            filename = f"portfolio_report_{timestamp}.txt"

        report = self.generate_full_report()

        with open(filename, 'w') as f:
            f.write(report)

        print(f"\n✓ Report saved to: {filename}")
        return filename

    def print_report(self):
        """Print report to console."""
        report = self.generate_full_report()
        print(report)


if __name__ == '__main__':
    from example_data import simple_two_asset_example

    # Example usage
    returns = simple_two_asset_example()
    optimizer = PortfolioOptimizer(returns, risk_free_rate=0.025/252)

    report = PortfolioReport(optimizer, portfolio_name="Example Two-Asset Portfolio")
    report.print_report()
    report.save_report()
