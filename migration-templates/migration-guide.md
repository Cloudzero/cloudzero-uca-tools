# Migration Guide: UV and Ruff for CloudZero UCA Tools

## Overview

This guide provides step-by-step instructions for migrating the CloudZero UCA Tools project from pip/hatch to UV for package management and enhancing Ruff configuration for better code quality.

## UV Migration Steps

### 1. Install UV

```bash
# Install UV globally (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv
```

### 2. Initialize UV Project

Since we already have a `pyproject.toml`, we'll update it rather than creating a new one:

```bash
# Create UV configuration without overwriting existing files
uv init --no-readme --python 3.12

# This creates uv.lock but preserves existing pyproject.toml
```

### 3. Update pyproject.toml

Key changes needed:

1. **Move dev dependencies** from `[tool.rye]` to `[tool.uv]`
2. **Update Python version** to 3.12 (per CLAUDE.md requirements)
3. **Replace requests with httpx** (per CLAUDE.md requirements)
4. **Add required libraries** (pydantic, humanize, etc.)

### 4. Migrate Dependencies

```bash
# Add existing dependencies to UV
uv add -r requirements.txt

# Add dev dependencies
uv add --dev pytest coverage pytest-cov pytest-mock pytest-env ruff

# Add new required dependencies
uv add httpx pydantic humanize

# Remove requests (replaced by httpx)
uv remove requests
```

### 5. Create Lock File

```bash
# UV automatically creates uv.lock when adding dependencies
# To manually update the lock file:
uv lock
```

### 6. Export Requirements (if needed for CI/CD)

```bash
# Export production requirements
uv export --no-hashes --format requirements-txt > requirements.txt

# Export all requirements including dev
uv export --no-hashes --format requirements-txt --dev > requirements-dev.txt
```

### 7. Update Scripts and CI/CD

Replace pip commands with UV:

```bash
# Old: pip install -r requirements.txt
# New:
uv sync

# Old: pip install -e .
# New:
uv sync --dev

# Running commands in UV environment
uv run pytest
uv run uca --help
```

## Ruff Configuration Enhancement

### 1. Current State Analysis

The project already has Ruff configured with:
- Line length: 120 ✓
- Target Python: 3.9 (needs update to 3.12)
- Basic rule sets enabled

### 2. Enhanced Configuration

Add to `[tool.ruff.lint]` select:

```toml
# Additional rules per CLAUDE.md
"C",      # flake8-comprehensions
"PIE",    # flake8-pie  
"PGH004", # pygrep-hooks
"PLE",    # pylint error
"PLW",    # pylint warning
"PLR1714",# pylint refactor
"T100",   # flake8-debugger
```

Update ignore list per CLAUDE.md:
```toml
ignore = [
    "E402", "E501", "B005", "B904", "C901", "C408",
    # Keep existing ignores
    "D200", "D211", "D212", "D100", "D104", "D400", "D415", "D417"
]
```

### 3. Running Ruff

```bash
# Check code
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

## Migration Checklist

- [ ] Install UV
- [ ] Backup current pyproject.toml
- [ ] Update pyproject.toml with UV configuration
- [ ] Migrate dependencies using `uv add`
- [ ] Replace requests with httpx in code
- [ ] Add pydantic and humanize dependencies
- [ ] Update Python version to 3.12
- [ ] Generate uv.lock file
- [ ] Update Ruff configuration
- [ ] Run Ruff to check/fix existing code
- [ ] Update CI/CD pipelines to use UV
- [ ] Update developer documentation
- [ ] Remove old dependency files (after verification)

## Common Issues and Solutions

### Issue: Dependency conflicts
**Solution**: Use `uv lock --refresh` to regenerate lock file

### Issue: Missing dependencies in production
**Solution**: Ensure all dependencies are in `[project.dependencies]`, not just dev-dependencies

### Issue: CI/CD failures
**Solution**: Export requirements.txt using `uv export` for compatibility

### Issue: Ruff conflicts with existing code style
**Solution**: Use `--fix` flag or add specific ignores to per-file-ignores

## Benefits After Migration

1. **Faster dependency resolution** - UV is 10-100x faster than pip
2. **Deterministic builds** - uv.lock ensures exact same versions
3. **Better Python version management** - UV handles Python installations
4. **Unified linting/formatting** - Ruff replaces multiple tools
5. **Improved code quality** - Enhanced rule sets catch more issues
6. **Simplified developer experience** - Single tool for package management

## Rollback Plan

If issues arise:

1. Keep backup of original pyproject.toml
2. Requirements.txt files are preserved via `uv export`
3. Can continue using pip with exported requirements
4. Ruff changes can be reverted via git

## Resources

- [UV Documentation](https://docs.astral.sh/uv/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Python Packaging Guide](https://packaging.python.org/en/latest/)
- [CloudZero Developer Guidelines](./CLAUDE.md)