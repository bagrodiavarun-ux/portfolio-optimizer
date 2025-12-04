"""
Enhanced report generator with embedded visualizations.
Generates both text and HTML reports with charts.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from portfolio import PortfolioOptimizer, CapitalMarketLine
from visualization import generate_all_charts


class EnhancedPortfolioReport:
    """Generate portfolio reports with embedded visualizations."""

    def __init__(self, optimizer: PortfolioOptimizer, returns: pd.DataFrame,
                 portfolio_name: str = "Portfolio Analysis"):
        """
        Initialize enhanced report generator.

        Args:
            optimizer: PortfolioOptimizer instance with loaded data
            returns: DataFrame with asset returns
            portfolio_name: Name of the portfolio being analyzed
        """
        self.optimizer = optimizer
        self.returns = returns
        self.portfolio_name = portfolio_name
        self.timestamp = datetime.now()

        # Generate all charts
        print("📊 Generating visualizations...")
        self.charts = generate_all_charts(optimizer, returns)

    def _section_header(self, title: str) -> str:
        """Format section header for text report."""
        return f"\n{'=' * 80}\n{title}\n{'=' * 80}\n"

    def _subsection_header(self, title: str) -> str:
        """Format subsection header for text report."""
        return f"\n{title}\n{'-' * len(title)}\n"

    def _html_header(self) -> str:
        """Generate HTML header with styling."""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.portfolio_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 50px;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }}
        .header {{
            text-align: center;
            margin-bottom: 50px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px;
            border-radius: 10px;
            color: white;
        }}
        .header h1 {{
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 15px;
            letter-spacing: -0.5px;
        }}
        .header p {{
            color: rgba(255, 255, 255, 0.95);
            font-size: 16px;
            margin: 8px 0;
        }}
        .section {{
            margin-bottom: 50px;
        }}
        .section-title {{
            font-size: 26px;
            font-weight: 700;
            color: #2c3e50;
            border-left: 6px solid #667eea;
            padding-left: 20px;
            margin-bottom: 30px;
            margin-top: 40px;
            letter-spacing: -0.3px;
        }}
        .subsection-title {{
            font-size: 18px;
            font-weight: 600;
            color: #34495e;
            margin-top: 25px;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid #ecf0f1;
        }}
        .chart-container {{
            margin: 30px 0;
            text-align: center;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
            transition: all 0.3s ease;
        }}
        .chart-container h3 {{
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 18px;
            font-weight: 600;
        }}
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            background-color: #fff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }}
        th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 16px;
            text-align: left;
            font-weight: 600;
            font-size: 14px;
            letter-spacing: 0.5px;
        }}
        td {{
            padding: 14px 16px;
            border-bottom: 1px solid #ecf0f1;
            font-size: 15px;
        }}
        tr:hover {{
            background-color: #f8f9fa;
            transition: background-color 0.2s ease;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        .highlight {{
            background: linear-gradient(135deg, #fff5f7 0%, #fff9e6 100%);
            padding: 20px;
            border-left: 5px solid #f39c12;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(243, 156, 18, 0.1);
        }}
        .highlight strong {{
            color: #2c3e50;
        }}
        .metric {{
            display: inline-block;
            background: linear-gradient(135deg, #e0e7ff 0%, #f3e7ff 100%);
            padding: 12px 24px;
            margin: 8px;
            border-radius: 6px;
            font-weight: 600;
            color: #2c3e50;
            font-size: 15px;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
            border: 1px solid rgba(102, 126, 234, 0.2);
            transition: all 0.3s ease;
        }}
        .metric:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(102, 126, 234, 0.25);
        }}
        .positive {{
            color: #27ae60;
            font-weight: 700;
        }}
        .negative {{
            color: #e74c3c;
            font-weight: 700;
        }}
        .neutral {{
            color: #3498db;
            font-weight: 700;
        }}
        footer {{
            margin-top: 60px;
            padding-top: 30px;
            border-top: 2px solid #ecf0f1;
            color: #7f8c8d;
            font-size: 13px;
            text-align: center;
            line-height: 1.8;
        }}
        .recommendation {{
            background: linear-gradient(135deg, #d5f4e6 0%, #e8f8f0 100%);
            padding: 20px;
            border-left: 5px solid #27ae60;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(39, 174, 96, 0.1);
        }}
        .recommendation strong {{
            color: #2c3e50;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Portfolio Analysis Report</h1>
            <p><strong>{self.portfolio_name}</strong></p>
            <p>{self.timestamp.strftime('%B %d, %Y at %H:%M:%S')}</p>
        </div>
"""

    def _html_footer(self) -> str:
        """Generate HTML footer."""
        return """
        <footer>
            <p>This report is generated automatically from live market data.</p>
            <p>Past performance is not indicative of future results.</p>
            <p>Disclaimer: This is an educational tool only. Consult a financial advisor before investing.</p>
        </footer>
    </div>
</body>
</html>
"""

    def generate_html_report(self) -> str:
        """Generate comprehensive HTML report with embedded charts."""
        report = self._html_header()

        # Asset Statistics Section
        report += '<div class="section">'
        report += '<div class="section-title">1. Asset Statistics</div>'

        stats = pd.DataFrame({
            'Annual Return': self.optimizer.mean_returns * 252,
            'Annual Volatility': self.optimizer.std_devs * np.sqrt(252),
        })

        report += '<table><tr><th>Asset</th><th>Annual Return</th><th>Annual Volatility</th></tr>'
        for asset in stats.index:
            ret = stats.loc[asset, 'Annual Return']
            vol = stats.loc[asset, 'Annual Volatility']
            report += f'<tr><td><strong>{asset}</strong></td><td class="positive">{ret:.2%}</td><td>{vol:.2%}</td></tr>'
        report += '</table>'
        report += '</div>'

        # Optimal Portfolios Section
        report += '<div class="section">'
        report += '<div class="section-title">2. Optimal Portfolios</div>'

        max_sharpe = self.optimizer.max_sharpe_portfolio()
        min_var = self.optimizer.min_variance_portfolio()

        report += '<div class="subsection-title">A. Maximum Sharpe Ratio Portfolio</div>'
        report += f'<div class="metric">Return: <span class="positive">{max_sharpe["return"]*252:.2%}</span></div>'
        report += f'<div class="metric">Volatility: {max_sharpe["volatility"]*np.sqrt(252):.2%}</div>'
        report += f'<div class="metric">Sharpe Ratio: <span class="positive">{max_sharpe["sharpe_ratio"]*np.sqrt(252):.4f}</span></div>'

        report += '<table><tr><th>Asset</th><th>Allocation</th></tr>'
        for asset, weight in sorted(max_sharpe['weights'].items(), key=lambda x: x[1], reverse=True):
            if weight > 0.001:
                report += f'<tr><td>{asset}</td><td>{weight:.2%}</td></tr>'
        report += '</table>'

        report += '<div class="subsection-title">B. Minimum Variance Portfolio</div>'
        report += f'<div class="metric">Return: {min_var["return"]*252:.2%}</div>'
        report += f'<div class="metric">Volatility: {min_var["volatility"]*np.sqrt(252):.2%}</div>'
        report += f'<div class="metric">Sharpe Ratio: {min_var["sharpe_ratio"]*np.sqrt(252):.4f}</div>'

        report += '<table><tr><th>Asset</th><th>Allocation</th></tr>'
        for asset, weight in sorted(min_var['weights'].items(), key=lambda x: x[1], reverse=True):
            if weight > 0.001:
                report += f'<tr><td>{asset}</td><td>{weight:.2%}</td></tr>'
        report += '</table>'
        report += '</div>'

        # Capital Market Line Section
        report += '<div class="section">'
        report += '<div class="section-title">3. Capital Market Line (CML) Analysis</div>'

        cml = CapitalMarketLine(max_sharpe, self.optimizer.annual_risk_free_rate)
        report += f'<div class="metric">Risk-Free Rate: {cml.risk_free_rate_annual:.2%}</div>'
        report += f'<div class="metric">Market Return: {cml.market_return_annual:.2%}</div>'
        report += f'<div class="metric">Market Volatility: {cml.market_volatility_annual:.2%}</div>'
        report += f'<div class="metric">Sharpe Ratio: {cml.sharpe_ratio_annual:.4f}</div>'

        report += '<div class="subsection-title">Expected Returns at Different Risk Levels</div>'
        report += '<table><tr><th>Volatility</th><th>Expected Return</th></tr>'
        for vol in [0.10, 0.15, 0.20, 0.25, 0.30]:
            ret = cml.expected_return(vol)
            report += f'<tr><td>{vol:.0%}</td><td class="positive">{ret:.2%}</td></tr>'
        report += '</table>'
        report += '</div>'

        # Charts Section
        report += '<div class="section">'
        report += '<div class="section-title">4. Visualizations</div>'

        chart_titles = {
            'efficient_frontier': 'Efficient Frontier & Capital Market Line',
            'correlation_heatmap': 'Asset Correlation Matrix',
            'risk_return_scatter': 'Risk-Return Profile',
            'sharpe_comparison': 'Sharpe Ratio Comparison',
            'cumulative_returns': 'Cumulative Returns Over Time',
            'allocation_comparison': 'Portfolio Allocation Comparison'
        }

        for chart_key, chart_title in chart_titles.items():
            if chart_key in self.charts:
                report += f'<div class="chart-container">'
                report += f'<h3>{chart_title}</h3>'
                report += f'<img src="data:image/png;base64,{self.charts[chart_key]}" alt="{chart_title}">'
                report += f'</div>'

        report += '</div>'

        # Key Insights Section
        report += '<div class="section">'
        report += '<div class="section-title">5. Key Insights & Recommendations</div>'

        max_sharpe_annual = max_sharpe['sharpe_ratio'] * np.sqrt(252)
        min_var_annual = min_var['sharpe_ratio'] * np.sqrt(252)
        avg_corr = self.optimizer.correlation_matrix.values[np.triu_indices_from(self.optimizer.correlation_matrix.values, k=1)].mean()

        report += f'<div class="highlight">'
        report += f'<strong>Diversification:</strong> {len(self.optimizer.assets)} assets with average correlation of {avg_corr:.4f}<br>'
        report += f'<strong>Risk-Adjusted Returns:</strong> Max Sharpe ({max_sharpe_annual:.4f}) vs Min Variance ({min_var_annual:.4f})<br>'
        report += f'<strong>Risk Reduction:</strong> {(max_sharpe["volatility"] - min_var["volatility"])*np.sqrt(252):.2%} lower volatility in min variance portfolio'
        report += f'</div>'

        if max_sharpe_annual > 1.0:
            recommendation = 'Strong risk-adjusted returns available'
            color = 'positive'
        elif max_sharpe_annual > 0.5:
            recommendation = 'Moderate risk-adjusted returns; consider diversification'
            color = 'neutral'
        else:
            recommendation = 'Poor risk-adjusted returns; portfolio may not be suitable'
            color = 'negative'

        report += f'<div class="recommendation">'
        report += f'<strong>✓ Recommendation:</strong> <span class="{color}">{recommendation}</span>'
        report += f'</div>'

        report += '</div>'

        report += self._html_footer()
        return report

    def generate_text_report(self) -> str:
        """Generate text report with chart descriptions."""
        from report_generator import PortfolioReport

        # Use the existing text report generator
        text_reporter = PortfolioReport(self.optimizer, self.portfolio_name)
        text_report = text_reporter.generate_full_report()

        # Add chart generation info
        text_report += self._section_header("8. VISUALIZATIONS GENERATED")
        text_report += "The following charts have been generated and embedded in the HTML report:\n"
        text_report += "  ✓ Efficient Frontier with Capital Market Line\n"
        text_report += "  ✓ Asset Correlation Matrix Heatmap\n"
        text_report += "  ✓ Risk-Return Scatter Plot\n"
        text_report += "  ✓ Sharpe Ratio Comparison Chart\n"
        text_report += "  ✓ Cumulative Returns Over Time\n"
        text_report += "  ✓ Portfolio Allocation Comparison\n"

        return text_report

    def save_html_report(self, filename: str = None) -> str:
        """
        Generate and save HTML report.

        Args:
            filename: Output filename (default: portfolio_report_TIMESTAMP.html)

        Returns:
            Path to saved report
        """
        if filename is None:
            timestamp = self.timestamp.strftime("%Y%m%d_%H%M%S")
            filename = f"portfolio_report_{timestamp}.html"

        report = self.generate_html_report()

        with open(filename, 'w') as f:
            f.write(report)

        print(f"✓ HTML report saved to: {filename}")
        return filename

    def save_text_report(self, filename: str = None) -> str:
        """
        Generate and save text report.

        Args:
            filename: Output filename (default: portfolio_report_TIMESTAMP.txt)

        Returns:
            Path to saved report
        """
        if filename is None:
            timestamp = self.timestamp.strftime("%Y%m%d_%H%M%S")
            filename = f"portfolio_report_{timestamp}_text.txt"

        report = self.generate_text_report()

        with open(filename, 'w') as f:
            f.write(report)

        print(f"✓ Text report saved to: {filename}")
        return filename

    def save_both_reports(self) -> tuple:
        """
        Generate and save both HTML and text reports.

        Returns:
            Tuple of (html_filename, text_filename)
        """
        timestamp = self.timestamp.strftime("%Y%m%d_%H%M%S")
        html_file = f"portfolio_report_{timestamp}.html"
        text_file = f"portfolio_report_{timestamp}.txt"

        self.save_html_report(html_file)
        self.save_text_report(text_file)

        return html_file, text_file


if __name__ == '__main__':
    from data_fetcher_yfinance import YahooFinanceAPI, get_current_risk_free_rate

    # Example usage
    rf = get_current_risk_free_rate()
    api = YahooFinanceAPI()
    returns = api.get_returns_dataframe(['AAPL', 'MSFT', 'GOOGL'], period='2y')

    if returns is not None:
        optimizer = PortfolioOptimizer(returns, rf)
        enhanced_report = EnhancedPortfolioReport(optimizer, returns, "Example Portfolio")

        # Save both reports
        html_file, text_file = enhanced_report.save_both_reports()
        print(f"\n✓ Reports generated:")
        print(f"  HTML: {html_file}")
        print(f"  Text: {text_file}")
