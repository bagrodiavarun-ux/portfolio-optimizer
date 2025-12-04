"""Visualization utilities for portfolio analysis."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from portfolio import PortfolioOptimizer, CapitalMarketLine
from io import BytesIO
import base64


def plot_efficient_frontier(optimizer: PortfolioOptimizer,
                            save_path: str = None,
                            figsize: tuple = (12, 8)):
    """
    Plot the efficient frontier with individual assets and optimal portfolios.

    Args:
        optimizer: PortfolioOptimizer instance
        save_path: Optional path to save figure
        figsize: Figure size tuple
    """
    # Generate frontier
    frontier = optimizer.efficient_frontier(n_points=50)

    # Get optimal portfolios
    max_sharpe = optimizer.max_sharpe_portfolio()
    min_var = optimizer.min_variance_portfolio()

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Plot frontier
    ax.plot(
        frontier['volatility'] * np.sqrt(252) * 100,
        frontier['return'] * 252 * 100,
        'b-', linewidth=2.5, label='Efficient Frontier'
    )

    # Plot individual assets
    for asset in optimizer.assets:
        annual_return = optimizer.mean_returns[asset] * 252 * 100
        annual_std = optimizer.std_devs[asset] * np.sqrt(252) * 100
        ax.scatter(annual_std, annual_return, s=150, alpha=0.7, label=asset)

    # Plot max Sharpe portfolio
    ax.scatter(
        max_sharpe['volatility'] * np.sqrt(252) * 100,
        max_sharpe['return'] * 252 * 100,
        marker='*', s=1000, color='green',
        label='Max Sharpe Ratio', zorder=5, edgecolors='darkgreen', linewidth=2
    )

    # Plot min variance portfolio
    ax.scatter(
        min_var['volatility'] * np.sqrt(252) * 100,
        min_var['return'] * 252 * 100,
        marker='s', s=200, color='orange',
        label='Min Variance', zorder=5, edgecolors='darkorange', linewidth=2
    )

    # Plot CML
    cml = CapitalMarketLine(max_sharpe, optimizer.risk_free_rate)
    cml_x = np.linspace(0, frontier['volatility'].max() * np.sqrt(252) * 100, 100)
    cml_y = cml.expected_return(cml_x / (np.sqrt(252) * 100)) * 252 * 100
    ax.plot(cml_x, cml_y, 'r--', linewidth=2, label='Capital Market Line')

    # Plot risk-free asset
    ax.scatter(0, optimizer.risk_free_rate * 252 * 100, marker='o', s=200,
               color='red', label='Risk-Free Asset', zorder=5, edgecolors='darkred', linewidth=2)

    ax.set_xlabel('Volatility (Annual %)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Expected Return (Annual %)', fontsize=12, fontweight='bold')
    ax.set_title('Efficient Frontier and Capital Market Line', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_correlation_heatmap(returns: pd.DataFrame, save_path: str = None):
    """
    Plot correlation matrix heatmap.

    Args:
        returns: DataFrame with asset returns
        save_path: Optional path to save figure
    """
    import matplotlib.pyplot as plt
    import numpy as np

    corr = returns.corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)

    ax.set_xticks(np.arange(len(corr.columns)))
    ax.set_yticks(np.arange(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha='right')
    ax.set_yticklabels(corr.columns)

    # Add correlation values
    for i in range(len(corr)):
        for j in range(len(corr)):
            text = ax.text(j, i, f'{corr.iloc[i, j]:.2f}',
                          ha="center", va="center", color="black", fontsize=10)

    ax.set_title('Asset Correlation Matrix', fontsize=14, fontweight='bold')
    plt.colorbar(im, ax=ax, label='Correlation Coefficient')

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_portfolio_weights(portfolio_dict: dict, title: str = "Portfolio Weights",
                          save_path: str = None):
    """
    Plot portfolio allocation as pie chart.

    Args:
        portfolio_dict: Dictionary of weights from optimizer
        title: Chart title
        save_path: Optional path to save figure
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    weights = portfolio_dict['weights']
    assets = list(weights.keys())
    allocations = [weights[a] for a in assets]

    # Filter out zero weights
    non_zero = [(a, w) for a, w in zip(assets, allocations) if w > 0.001]
    assets, allocations = zip(*non_zero) if non_zero else ([], [])

    colors = plt.cm.Set3(np.linspace(0, 1, len(assets)))
    wedges, texts, autotexts = ax.pie(
        allocations, labels=assets, autopct='%1.1f%%',
        colors=colors, startangle=90, textprops={'fontsize': 11}
    )

    ax.set_title(
        f"{title}\nReturn: {portfolio_dict['return']*252:.2%} | "
        f"Volatility: {portfolio_dict['volatility']*np.sqrt(252):.2%} | "
        f"Sharpe: {portfolio_dict['sharpe_ratio']:.4f}",
        fontsize=12, fontweight='bold'
    )

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_asset_returns_distribution(returns: pd.DataFrame, save_path: str = None):
    """
    Plot distribution of daily returns for each asset.

    Args:
        returns: DataFrame with asset returns
        save_path: Optional path to save figure
    """
    fig, axes = plt.subplots(1, len(returns.columns), figsize=(14, 4))
    if len(returns.columns) == 1:
        axes = [axes]

    for idx, asset in enumerate(returns.columns):
        axes[idx].hist(returns[asset] * 100, bins=50, alpha=0.7, color='steelblue', edgecolor='black')
        axes[idx].set_title(f'{asset} Daily Returns Distribution', fontweight='bold')
        axes[idx].set_xlabel('Daily Return (%)')
        axes[idx].set_ylabel('Frequency')
        axes[idx].grid(True, alpha=0.3)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_cumulative_returns(returns: pd.DataFrame, save_path: str = None):
    """
    Plot cumulative returns over time for each asset.

    Args:
        returns: DataFrame with asset returns
        save_path: Optional path to save figure
    """
    cumulative = (1 + returns).cumprod()

    fig, ax = plt.subplots(figsize=(12, 6))
    for asset in cumulative.columns:
        ax.plot(cumulative.index, cumulative[asset], label=asset, linewidth=2, alpha=0.8)

    ax.set_title('Cumulative Returns Over Time', fontsize=14, fontweight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Cumulative Return (Growth of $1)', fontsize=12)
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_risk_return_scatter(optimizer: PortfolioOptimizer, save_path: str = None):
    """
    Plot risk vs return scatter plot for individual assets.

    Args:
        optimizer: PortfolioOptimizer instance
        save_path: Optional path to save figure
    """
    fig, ax = plt.subplots(figsize=(10, 7))

    annual_returns = optimizer.mean_returns * 252 * 100
    annual_vols = optimizer.std_devs * np.sqrt(252) * 100

    colors = plt.cm.Set3(np.linspace(0, 1, len(optimizer.assets)))
    for idx, asset in enumerate(optimizer.assets):
        ax.scatter(annual_vols[asset], annual_returns[asset], s=300, alpha=0.7,
                  label=asset, color=colors[idx], edgecolors='black', linewidth=2)

    ax.set_xlabel('Annual Volatility (%)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Annual Return (%)', fontsize=12, fontweight='bold')
    ax.set_title('Individual Asset Risk-Return Profile', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_sharpe_ratio_comparison(optimizer: PortfolioOptimizer, save_path: str = None):
    """
    Plot Sharpe ratio for each asset and optimal portfolios.

    Args:
        optimizer: PortfolioOptimizer instance
        save_path: Optional path to save figure
    """
    # Calculate Sharpe ratios for individual assets
    asset_returns = optimizer.mean_returns * 252
    asset_vols = optimizer.std_devs * np.sqrt(252)
    asset_sharpes = (asset_returns - optimizer.annual_risk_free_rate) / asset_vols

    # Get optimal portfolios
    max_sharpe = optimizer.max_sharpe_portfolio()
    min_var = optimizer.min_variance_portfolio()
    max_sharpe_annual = max_sharpe['sharpe_ratio'] * np.sqrt(252)
    min_var_annual = min_var['sharpe_ratio'] * np.sqrt(252)

    # Prepare data
    labels = list(optimizer.assets) + ['Max Sharpe', 'Min Variance']
    values = list(asset_sharpes.values) + [max_sharpe_annual, min_var_annual]
    colors_list = ['steelblue'] * len(optimizer.assets) + ['green', 'orange']

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(labels, values, color=colors_list, alpha=0.7, edgecolor='black', linewidth=2)

    # Add value labels on bars
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{val:.3f}', ha='center', va='bottom', fontweight='bold')

    ax.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
    ax.set_ylabel('Sharpe Ratio (Annual)', fontsize=12, fontweight='bold')
    ax.set_title('Sharpe Ratio Comparison: Individual Assets vs Portfolios', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_allocation_comparison(optimizer: PortfolioOptimizer, save_path: str = None):
    """
    Compare allocations of Max Sharpe and Min Variance portfolios side by side.

    Args:
        optimizer: PortfolioOptimizer instance
        save_path: Optional path to save figure
    """
    max_sharpe = optimizer.max_sharpe_portfolio()
    min_var = optimizer.min_variance_portfolio()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    # Max Sharpe allocation
    weights_ms = [max_sharpe['weights'][a] for a in optimizer.assets]
    colors = plt.cm.Set3(np.linspace(0, 1, len(optimizer.assets)))
    ax1.pie(
        weights_ms, autopct='%1.1f%%', colors=colors, startangle=90,
        textprops={'fontsize': 9, 'weight': 'bold'}
    )
    ax1.set_title('Max Sharpe Portfolio\n' +
                 f"Return: {max_sharpe['return']*252:.2%} | " +
                 f"Vol: {max_sharpe['volatility']*np.sqrt(252):.2%}",
                fontsize=11, fontweight='bold', pad=20)
    ax1.legend(optimizer.assets, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)

    # Min Variance allocation
    weights_mv = [min_var['weights'][a] for a in optimizer.assets]
    ax2.pie(
        weights_mv, autopct='%1.1f%%', colors=colors, startangle=90,
        textprops={'fontsize': 9, 'weight': 'bold'}
    )
    ax2.set_title('Min Variance Portfolio\n' +
                 f"Return: {min_var['return']*252:.2%} | " +
                 f"Vol: {min_var['volatility']*np.sqrt(252):.2%}",
                fontsize=11, fontweight='bold', pad=20)
    ax2.legend(optimizer.assets, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def fig_to_base64(fig) -> str:
    """
    Convert matplotlib figure to base64 string for embedding in reports.

    Args:
        fig: Matplotlib figure object

    Returns:
        Base64 encoded image string
    """
    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    buffer.close()
    plt.close(fig)
    return image_base64


def generate_all_charts(optimizer: PortfolioOptimizer, returns: pd.DataFrame) -> dict:
    """
    Generate all visualization charts and return as base64 encoded strings.

    Args:
        optimizer: PortfolioOptimizer instance
        returns: DataFrame with asset returns

    Returns:
        Dictionary mapping chart names to base64 encoded images
    """
    charts = {}

    # 1. Efficient Frontier
    frontier = optimizer.efficient_frontier(n_points=50)
    max_sharpe = optimizer.max_sharpe_portfolio()
    min_var = optimizer.min_variance_portfolio()

    # Handle edge case: empty frontier
    if frontier.empty:
        print("⚠ Warning: Could not generate efficient frontier - using minimal visualization")
        frontier = pd.DataFrame({'volatility': [0], 'return': [0], 'sharpe_ratio': [0]})

    fig, ax = plt.subplots(figsize=(12, 8))

    # Safely plot frontier with validation
    frontier_vol = frontier['volatility'] * np.sqrt(252) * 100
    frontier_ret = frontier['return'] * 252 * 100
    # Handle extreme values
    if frontier_vol.max() > 0:
        ax.plot(frontier_vol, frontier_ret,
               'b-', linewidth=2.5, label='Efficient Frontier')
    else:
        print("⚠ Warning: Frontier volatility is zero - skipping frontier line")

    for asset in optimizer.assets:
        annual_return = optimizer.mean_returns[asset] * 252 * 100
        annual_std = optimizer.std_devs[asset] * np.sqrt(252) * 100
        ax.scatter(annual_std, annual_return, s=150, alpha=0.7, label=asset)

    ax.scatter(max_sharpe['volatility'] * np.sqrt(252) * 100,
              max_sharpe['return'] * 252 * 100,
              marker='*', s=1000, color='green',
              label='Max Sharpe Ratio', zorder=5, edgecolors='darkgreen', linewidth=2)

    ax.scatter(min_var['volatility'] * np.sqrt(252) * 100,
              min_var['return'] * 252 * 100,
              marker='s', s=200, color='orange',
              label='Min Variance', zorder=5, edgecolors='darkorange', linewidth=2)

    cml = CapitalMarketLine(max_sharpe, optimizer.annual_risk_free_rate)
    # CML calculation: keep in decimal format to avoid double conversions
    cml_x = np.linspace(0, frontier['volatility'].max() * np.sqrt(252), 100)
    cml_y = np.array([cml.expected_return(vol) for vol in cml_x])
    # Convert to percentage for display
    cml_x_pct = cml_x * 100
    cml_y_pct = cml_y * 100
    ax.plot(cml_x_pct, cml_y_pct, 'r--', linewidth=2, label='Capital Market Line')

    ax.scatter(0, optimizer.annual_risk_free_rate * 252 * 100, marker='o', s=200,
              color='red', label='Risk-Free Asset', zorder=5, edgecolors='darkred', linewidth=2)

    ax.set_xlabel('Volatility (Annual %)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Expected Return (Annual %)', fontsize=12, fontweight='bold')
    ax.set_title('Efficient Frontier and Capital Market Line', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    charts['efficient_frontier'] = fig_to_base64(fig)

    # 2. Correlation Heatmap
    corr = returns.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)

    ax.set_xticks(np.arange(len(corr.columns)))
    ax.set_yticks(np.arange(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha='right')
    ax.set_yticklabels(corr.columns)

    for i in range(len(corr)):
        for j in range(len(corr)):
            ax.text(j, i, f'{corr.iloc[i, j]:.2f}',
                   ha="center", va="center", color="black", fontsize=10)

    ax.set_title('Asset Correlation Matrix', fontsize=14, fontweight='bold')
    plt.colorbar(im, ax=ax, label='Correlation Coefficient')
    charts['correlation_heatmap'] = fig_to_base64(fig)

    # 3. Risk-Return Scatter
    fig, ax = plt.subplots(figsize=(10, 7))
    annual_returns = optimizer.mean_returns * 252 * 100
    annual_vols = optimizer.std_devs * np.sqrt(252) * 100
    colors = plt.cm.Set3(np.linspace(0, 1, len(optimizer.assets)))

    for idx, asset in enumerate(optimizer.assets):
        ax.scatter(annual_vols[asset], annual_returns[asset], s=300, alpha=0.7,
                  label=asset, color=colors[idx], edgecolors='black', linewidth=2)

    ax.set_xlabel('Annual Volatility (%)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Annual Return (%)', fontsize=12, fontweight='bold')
    ax.set_title('Individual Asset Risk-Return Profile', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    charts['risk_return_scatter'] = fig_to_base64(fig)

    # 4. Sharpe Ratio Comparison
    asset_sharpes = (optimizer.mean_returns * 252 - optimizer.annual_risk_free_rate) / (optimizer.std_devs * np.sqrt(252))
    max_sharpe_annual = max_sharpe['sharpe_ratio'] * np.sqrt(252)
    min_var_annual = min_var['sharpe_ratio'] * np.sqrt(252)

    labels = list(optimizer.assets) + ['Max Sharpe', 'Min Variance']
    values = list(asset_sharpes.values) + [max_sharpe_annual, min_var_annual]
    colors_list = ['steelblue'] * len(optimizer.assets) + ['green', 'orange']

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(labels, values, color=colors_list, alpha=0.7, edgecolor='black', linewidth=2)

    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{val:.3f}', ha='center', va='bottom', fontweight='bold')

    ax.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
    ax.set_ylabel('Sharpe Ratio (Annual)', fontsize=12, fontweight='bold')
    ax.set_title('Sharpe Ratio Comparison', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    charts['sharpe_comparison'] = fig_to_base64(fig)

    # 5. Cumulative Returns
    cumulative = (1 + returns).cumprod()
    fig, ax = plt.subplots(figsize=(12, 6))

    for asset in cumulative.columns:
        ax.plot(cumulative.index, cumulative[asset], label=asset, linewidth=2, alpha=0.8)

    ax.set_title('Cumulative Returns Over Time', fontsize=14, fontweight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Cumulative Return (Growth of $1)', fontsize=12)
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    charts['cumulative_returns'] = fig_to_base64(fig)

    # 6. Allocation Comparison
    weights_ms = [max_sharpe['weights'][a] for a in optimizer.assets]
    weights_mv = [min_var['weights'][a] for a in optimizer.assets]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    colors = plt.cm.Set3(np.linspace(0, 1, len(optimizer.assets)))

    # Max Sharpe Portfolio - use legend instead of labels
    ax1.pie(
        weights_ms, autopct='%1.1f%%', colors=colors, startangle=90,
        textprops={'fontsize': 9, 'weight': 'bold'}
    )
    ax1.set_title('Max Sharpe Portfolio', fontsize=12, fontweight='bold', pad=20)
    ax1.legend(optimizer.assets, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)

    # Min Variance Portfolio - use legend instead of labels
    ax2.pie(
        weights_mv, autopct='%1.1f%%', colors=colors, startangle=90,
        textprops={'fontsize': 9, 'weight': 'bold'}
    )
    ax2.set_title('Min Variance Portfolio', fontsize=12, fontweight='bold', pad=20)
    ax2.legend(optimizer.assets, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)

    plt.tight_layout()
    charts['allocation_comparison'] = fig_to_base64(fig)

    # 7. Security Market Line (using S&P 500 as market proxy)
    try:
        import yfinance as yf
        # Fetch S&P 500 data for the same period as the portfolio stocks
        sp500_data = yf.download('^GSPC', start=returns.index[0], end=returns.index[-1],
                                  progress=False, auto_adjust=True)
        if not sp500_data.empty and len(sp500_data) > 1:
            sp500_returns = sp500_data['Close'].pct_change().dropna()
            # Align with portfolio returns
            sp500_returns = sp500_returns.loc[returns.index]

            from portfolio import SecurityMarketLine

            max_sharpe = optimizer.max_sharpe_portfolio()
            sml = SecurityMarketLine(
                market_return=sp500_returns.mean() * 252,
                market_volatility=sp500_returns.std() * np.sqrt(252),
                risk_free_rate=optimizer.annual_risk_free_rate,
                asset_returns=returns
            )

            analysis = sml.analyze_assets(sp500_returns)

            fig, ax = plt.subplots(figsize=(12, 8))

            # Plot individual assets
            colors = plt.cm.Set3(np.linspace(0, 1, len(optimizer.assets)))
            for idx, (_, row) in enumerate(analysis.iterrows()):
                color = 'green' if row['alpha'] > 0 else 'red'
                ax.scatter(row['beta'], row['expected_return'] * 252,
                          s=300, alpha=0.7, label=row['asset'],
                          color=color, edgecolors='black', linewidth=2)
                ax.annotate(row['asset'], (row['beta'], row['expected_return'] * 252),
                           xytext=(5, 5), textcoords='offset points', fontsize=10, fontweight='bold')

            # Plot SML line
            beta_range = np.linspace(0, max(analysis['beta'].max(), 2), 100)
            sml_returns = np.array([sml.required_return(b) for b in beta_range])

            ax.plot(beta_range, sml_returns, 'b--', linewidth=2.5, label='Security Market Line')

            # Plot risk-free asset
            ax.scatter(0, optimizer.annual_risk_free_rate, marker='o', s=400,
                      color='gold', label='Risk-Free Asset', edgecolors='darkgoldenrod', linewidth=2, zorder=5)

            # Plot market portfolio (S&P 500)
            market_return = sp500_returns.mean() * 252
            ax.scatter(1, market_return, marker='D', s=400,
                      color='purple', label='Market (S&P 500)', edgecolors='darkviolet', linewidth=2, zorder=5)

            ax.set_xlabel('Beta (Market Risk)', fontsize=12, fontweight='bold')
            ax.set_ylabel('Expected Annual Return', fontsize=12, fontweight='bold')
            ax.set_title('Security Market Line (CAPM) - S&P 500 as Market Proxy', fontsize=14, fontweight='bold')
            ax.legend(loc='best', fontsize=10)
            ax.grid(True, alpha=0.3)
            ax.axhline(y=optimizer.annual_risk_free_rate, color='gold', linestyle=':', alpha=0.5)

            charts['security_market_line'] = fig_to_base64(fig)
    except Exception as e:
        print(f"⚠ Could not generate Security Market Line chart: {str(e)[:50]}")

    return charts


if __name__ == '__main__':
    from example_data import simple_two_asset_example

    # Example usage
    returns = simple_two_asset_example()
    optimizer = PortfolioOptimizer(returns, risk_free_rate=0.025/252)

    print("Generating efficient frontier plot...")
    plot_efficient_frontier(optimizer, save_path='efficient_frontier.png')

    print("Generating correlation heatmap...")
    plot_correlation_heatmap(returns, save_path='correlation_matrix.png')

    max_sharpe = optimizer.max_sharpe_portfolio()
    print("Generating portfolio weights chart...")
    plot_portfolio_weights(max_sharpe, title="Optimal Portfolio (Max Sharpe)",
                          save_path='portfolio_weights.png')
