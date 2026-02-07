# Development Guide

## Prerequisites

- Python 3.12 or newer
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver

## Setup

### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Create Virtual Environment

```bash
uv venv --python 3.12
source .venv/bin/activate
```

### Install Dependencies

```bash
# Install project in editable mode with all dependencies
uv pip install -e .

# Install development dependencies
uv pip install -e ".[dev]"
```

## Development Workflow

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/common/test_cli.py

# Run with coverage
uv run pytest --cov=uca
```

### Linting

```bash
# Check code style
ruff check .

# Auto-fix issues
ruff check . --fix

# Format code
ruff format .
```

### Building

```bash
# Build distribution packages
uv run python -m build
```

## Configuration

### Ruff Configuration

The project uses Ruff for linting with the following configuration:
- Line length: 120 characters
- Target Python version: 3.12
- Enabled rules: E, F, I, W, C, B, D, and more (see pyproject.toml)

### Test Configuration

Tests use pytest with:
- Coverage reporting enabled
- Doctest modules included
- Environment variables set for AWS mocking
- Custom markers: slow, unit, performance, sns

## CI/CD

GitHub Actions workflows are configured to:
- Run tests on Python 3.10, 3.11, and 3.12
- Use uv for fast dependency installation
- Run Ruff for linting
- Publish to PyPI on release

## Tips

- Always use `uv` instead of `pip` for package management
- Run `ruff check` before committing
- Keep dependencies in `pyproject.toml` up to date
- Use `uv lock` to create reproducible builds