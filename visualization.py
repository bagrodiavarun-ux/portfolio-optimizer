"""Visualization utilities for portfolio analysis."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from portfolio import PortfolioOptimizer, CapitalMarketLine


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
