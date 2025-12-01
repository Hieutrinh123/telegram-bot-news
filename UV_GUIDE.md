# UV Quick Reference Guide

This project now uses [uv](https://github.com/astral-sh/uv) for fast Python package management.

## Why UV?

- **10-100x faster** than pip
- **Automatic virtual environment** management
- **Compatible** with existing pip workflows
- **Drop-in replacement** for pip commands

## Common Commands

### Installation & Setup

```bash
# Install dependencies (creates .venv automatically)
uv sync

# Add a new package
uv add package-name

# Add a specific version
uv add package-name==1.2.3

# Remove a package
uv remove package-name
```

### Running Code

```bash
# Run Python scripts
uv run python main.py
uv run python main.py --now

# Run any command in the virtual environment
uv run python crawler.py
uv run python twitter_crawler.py
```

### Updating Dependencies

```bash
# Update all dependencies
uv lock --upgrade

# Update and install
uv sync --upgrade
```

### Virtual Environment

```bash
# uv automatically creates .venv/
# To activate manually (optional):
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

## Project Files

- `pyproject.toml` - Project metadata and dependencies (replaces requirements.txt)
- `uv.lock` - Locked dependency versions (like package-lock.json)
- `.venv/` - Virtual environment (auto-created by uv)

## Migration from pip

The project still includes `requirements.txt` for compatibility, but uv uses `pyproject.toml`:

```bash
# Old way (pip)
pip install -r requirements.txt
python main.py

# New way (uv)
uv sync
uv run python main.py
```

## Troubleshooting

**"uv: command not found"**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Need to reset environment?**
```bash
rm -rf .venv
uv sync
```

**Want to use pip instead?**
- No problem! `requirements.txt` still works
- Just activate the venv and use pip normally
