# Ruff Quick Reference for CloudZero Developers

## Essential Ruff Commands

### Basic Usage
```bash
# Check code for issues
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code (like Black)
ruff format .

# Check formatting without changing
ruff format --check .
```

### Targeted Checks
```bash
# Check specific file
ruff check path/to/file.py

# Check specific directory
ruff check src/

# Check with specific rules
ruff check --select E,F,I .

# Ignore specific rules
ruff check --ignore E501 .
```

### Advanced Options
```bash
# Show detailed explanations
ruff check --show-fixes .

# Show source code for errors
ruff check --show-source .

# Generate baseline (ignore existing violations)
ruff check --fix --unsafe-fixes .

# Watch mode (re-run on file changes)
ruff check --watch .
```

## Configuration in pyproject.toml

### CloudZero Standard Configuration
```toml
[tool.ruff]
target-version = "py312"
line-length = 120
indent-width = 4

[tool.ruff.lint]
select = [
    "E", "W", "F", "I", "C", "B", 
    "PIE", "PGH004", "PLE", "PLW", 
    "PLR1714", "T100"
]
ignore = [
    "E402", "E501", "B005", "B904", 
    "C901", "C408"
]

[tool.ruff.format]
quote-style = "double"
line-ending = "auto"
```

## Rule Categories

### Core Rules
- **E** - pycodestyle errors (PEP 8)
- **W** - pycodestyle warnings  
- **F** - Pyflakes (undefined names, unused imports)
- **I** - isort (import sorting)

### CloudZero Required Rules
- **C** - flake8-comprehensions (simplify comprehensions)
- **B** - flake8-bugbear (likely bugs and design problems)
- **PIE** - flake8-pie (miscellaneous lints)
- **PGH004** - Use specific codes with noqa
- **PLE** - Pylint errors
- **PLW** - Pylint warnings
- **T100** - Debugger calls (no breakpoints in code)

### Additional Quality Rules
- **D** - pydocstyle (docstring conventions)
- **UP** - pyupgrade (upgrade syntax for newer Python)
- **RUF** - Ruff-specific rules
- **S** - flake8-bandit (security issues)
- **SIM** - flake8-simplify (simplify code)

## Common Fixes

### Import Sorting (I)
```python
# Before
import os
from typing import List
import sys
from .models import User

# After (ruff format)
import os
import sys
from typing import List

from .models import User
```

### Remove Unused Imports (F401)
```python
# Before
import os  # unused
import sys

# After
import sys
```

### Simplify Comprehensions (C4)
```python
# Before
[x for x in items]
dict([(k, v) for k, v in pairs])

# After
list(items)
dict(pairs)
```

## Ignoring Rules

### Inline (single line)
```python
long_string = "very long string"  # noqa: E501
```

### Inline (specific rule)
```python
eval(user_input)  # noqa: S307
```

### File-level
```python
# ruff: noqa: E501
# Entire file ignores line-length rule
```

### Per-file in config
```toml
[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101"]  # Allow assert in tests
"__init__.py" = ["F401"]  # Allow unused imports
```

## Integration with VS Code

### settings.json
```json
{
    "ruff.path": ["ruff"],
    "ruff.lint.enable": true,
    "ruff.format.enable": true,
    "editor.formatOnSave": true,
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff"
    }
}
```

### Keyboard Shortcuts
- Format document: `Shift+Alt+F`
- Fix all auto-fixable issues: `Ctrl+Shift+P` → "Ruff: Fix all"

## Pre-commit Hook

### .pre-commit-config.yaml
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.3
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## CI/CD Integration

### GitHub Actions
```yaml
- name: Lint with Ruff
  run: |
    uv run ruff check .
    uv run ruff format --check .
```

## Common CloudZero Patterns

### Copyright Headers
```python
# Copyright (c) CloudZero - ALL RIGHTS RESERVED
# Unauthorized copying of this file is prohibited.
# Direct questions to legal@cloudzero.com
```

### Docstring Style (Google)
```python
def process_data(input_data: dict) -> dict:
    """Process input data according to rules.
    
    Args:
        input_data: Dictionary containing raw data
        
    Returns:
        Processed data dictionary
        
    Raises:
        ValueError: If input_data is invalid
    """
```

## Performance Tips

1. **Ruff is fast** - 10-100x faster than traditional linters
2. **Use --fix liberally** - Most fixes are safe
3. **Cache is automatic** - Subsequent runs are faster
4. **Watch mode** - Great for development

## Troubleshooting

### See all available rules
```bash
ruff rule --all
```

### Explain specific rule
```bash
ruff rule E501
ruff rule PIE790
```

### Debug configuration
```bash
ruff check --show-settings
```

### Generate config from existing code
```bash
ruff check --select ALL --statistics
```

## Migration from Other Tools

### From Black + isort + flake8
```bash
# Remove old tools
uv remove black isort flake8 flake8-*

# Add ruff
uv add --dev ruff

# Run ruff with all fixes
ruff check --fix .
ruff format .
```

### Equivalent Rules
- Black → `ruff format`
- isort → rule category `I`
- flake8 → rule categories `E`, `W`, `F`
- pylint → rule categories `PL*`
- bandit → rule category `S`

## Best Practices

1. **Run before commits** - Use pre-commit or git hooks
2. **Fix automatically** - Use `--fix` flag
3. **Be specific with noqa** - Always specify rule codes
4. **Configure per-project** - Adjust rules for project needs
5. **Stay updated** - Ruff adds new rules regularly