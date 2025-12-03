# Contributing to Portfolio Optimizer

Thanks for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## Getting Started

### 1. Fork the Repository
```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/yourusername/portfolio-optimizer.git
cd portfolio-optimizer
```

### 2. Set Up Development Environment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development tools
pip install pytest black flake8
```

### 3. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## Development Guidelines

### Code Style
- Follow PEP 8
- Use type hints for all functions
- Keep functions focused and under 50 lines when possible
- Write descriptive variable names

### Docstrings
All functions must have docstrings:
```python
def calculate_returns(prices: List[float]) -> np.ndarray:
    """
    Calculate daily returns from closing prices.

    Args:
        prices: List of closing prices

    Returns:
        numpy array of daily returns
    """
```

### Testing
- Write tests for new functionality
- Run existing tests before submitting PR
- Aim for >80% code coverage
```bash
pytest tests/
```

### Mathematical Correctness
- Verify all financial formulas against real market data
- Include manual benchmark calculations for critical functions
- Document any assumptions or limitations

## Types of Contributions

### Bug Fixes
- Include a clear description of the bug
- Add test case that reproduces the issue
- Reference any related issues

### New Features
- Discuss in an issue first (before major implementation)
- Keep changes focused and atomic
- Update documentation and examples
- Add comprehensive tests

### Documentation
- Improve README clarity
- Add usage examples
- Clarify complex concepts
- Fix typos and grammar

### Optimization
- Benchmark before/after performance
- Document performance gains
- Ensure correctness is not sacrificed for speed

## Submitting Changes

### 1. Commit Message Format
```
[Type] Brief description (50 chars or less)

More detailed explanation if needed (wrap at 72 chars).
Include the why, not just what changed.

Fixes #issue-number (if applicable)
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation updates
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `perf`: Performance improvements

### 2. Example Good Commit
```
fix: correct risk-free rate scaling from annual to daily

The risk-free rate was being applied as an annual rate to daily returns,
causing Sharpe ratios to be severely negative. Now converts annual rate to
daily (divide by 252) before using in calculations. Verified with manual
calculations against real market data.

Fixes #15
```

### 3. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

Then open a PR on GitHub with:
- Clear title describing the change
- Description of what changed and why
- Reference to any related issues
- Mention if it's a breaking change

## Pull Request Checklist

- [ ] Code follows PEP 8 style guidelines
- [ ] All docstrings and comments added
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] README/documentation updated if needed
- [ ] No debugging prints or commented code left
- [ ] Commit messages are clear and descriptive

## Areas We're Looking For Help

### High Priority
- [ ] Black-Litterman model implementation
- [ ] Portfolio backtesting engine
- [ ] Monte Carlo simulations
- [ ] Risk constraints (sector limits, max weights)
- [ ] Factor-based risk models

### Medium Priority
- [ ] Web dashboard (Streamlit or Dash)
- [ ] Performance optimizations
- [ ] Support for international equities
- [ ] Enhanced visualization options
- [ ] Extended documentation

### Low Priority
- [ ] Additional example datasets
- [ ] Alternative data sources
- [ ] Educational materials
- [ ] Community features

## Questions?

- Check existing issues first
- Open a new issue for bugs or features
- Use discussions for questions
- Check documentation

## Recognition

Contributors will be recognized in:
- Project README (Contributors section)
- Release notes for relevant versions
- This CONTRIBUTING.md file

Thank you for contributing to Portfolio Optimizer! 🚀
