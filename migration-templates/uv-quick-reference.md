# UV Quick Reference for CloudZero Developers

## Common UV Commands

### Project Setup
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Initialize new project
uv init

# Sync dependencies (like pip install -r requirements.txt)
uv sync

# Sync with dev dependencies
uv sync --dev
```

### Dependency Management
```bash
# Add a dependency
uv add httpx

# Add a dev dependency  
uv add --dev pytest

# Add multiple dependencies
uv add httpx pydantic humanize

# Remove a dependency
uv remove requests

# Update all dependencies
uv lock --refresh

# Update specific dependency
uv add httpx --upgrade
```

### Running Commands
```bash
# Run any command in the virtual environment
uv run python script.py
uv run pytest
uv run uca --help

# Run with specific Python version
uv run --python 3.12 python script.py
```

### Virtual Environment
```bash
# UV automatically manages virtual environments
# Located in .venv by default

# Activate manually (not usually needed)
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### Lock Files
```bash
# Update lock file
uv lock

# Force refresh all dependencies
uv lock --refresh

# Check if lock file is up to date
uv lock --check
```

### Exporting Dependencies
```bash
# Export to requirements.txt format
uv export --format requirements-txt > requirements.txt

# Export without hashes (cleaner)
uv export --no-hashes --format requirements-txt > requirements.txt

# Export with dev dependencies
uv export --dev --format requirements-txt > requirements-dev.txt
```

### Python Version Management
```bash
# Install specific Python version
uv python install 3.12

# List available Python versions
uv python list

# Pin Python version for project
uv python pin 3.12
```

## UV vs Pip Command Equivalents

| pip | uv |
|-----|-----|
| `pip install package` | `uv add package` |
| `pip install -r requirements.txt` | `uv sync` |
| `pip install -e .` | `uv sync --dev` |
| `pip uninstall package` | `uv remove package` |
| `pip list` | `uv pip list` |
| `pip freeze` | `uv export` |
| `python -m venv .venv` | (automatic with uv) |
| `pip install --upgrade package` | `uv add package --upgrade` |

## Configuration in pyproject.toml

### Basic Structure
```toml
[tool.uv]
dev-dependencies = [
    "pytest>=8.2.0",
    "ruff>=0.4.3",
]

[tool.uv.python]
version = "3.12"
```

### Scripts (replacing package.json scripts)
```toml
[tool.uv.scripts]
test = "pytest"
lint = "ruff check ."
format = "ruff format ."
build = "python -m build"
```

Run scripts with:
```bash
uv run test
uv run lint
```

## Best Practices

1. **Always commit uv.lock** - Ensures reproducible builds
2. **Use uv run** - Ensures correct environment activation
3. **Prefer uv add over manual edits** - Keeps lock file in sync
4. **Regular updates** - Run `uv lock --refresh` periodically
5. **CI/CD compatibility** - Export requirements.txt for legacy systems

## Troubleshooting

### Reset environment
```bash
rm -rf .venv uv.lock
uv sync
```

### Check for conflicts
```bash
uv lock --check
```

### Verbose output for debugging
```bash
uv -v sync
uv -v add package
```

### Clear cache
```bash
uv cache clean
```

## Migration from Existing Project

```bash
# Quick migration steps
uv init --no-readme
uv add -r requirements.txt
uv add --dev -r requirements-dev.txt
uv lock
```

## Environment Variables

```bash
# UV respects standard Python env vars
export VIRTUAL_ENV=.venv
export UV_CACHE_DIR=/custom/cache/path
export UV_PYTHON=3.12
```

## Performance Tips

1. UV caches aggressively - first install is slower, subsequent are instant
2. Use `--no-cache` only when debugging
3. Lock files prevent re-resolution - faster installs
4. Parallel downloads by default

## Integration with IDEs

### VS Code
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.terminal.activateEnvironment": true
}
```

### PyCharm
- Automatically detects .venv
- Set interpreter to `.venv/bin/python`