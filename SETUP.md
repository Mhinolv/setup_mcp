# Python Development Setup with uv

This guide will help you set up a Python development environment using uv, a fast Python package manager and project manager.

## Prerequisites

- A Unix-like system (macOS, Linux, or WSL on Windows)
- Internet connection for downloading uv and packages

## Step 1: Install uv

### Option A: Using the official installer (Recommended)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Option B: Using Homebrew (macOS)
```bash
brew install uv
```

### Option C: Using pip
```bash
pip install uv
```

After installation, restart your terminal or run:
```bash
source ~/.bashrc  # or ~/.zshrc depending on your shell
```

Verify the installation:
```bash
uv --version
```

## Step 2: Initialize a New uv Project

Create a new project directory and initialize it:
```bash
mkdir my-python-project
cd my-python-project
uv init
```

This creates:
- `pyproject.toml` - Project configuration and dependencies
- `src/` - Source code directory
- `README.md` - Project documentation
- `.python-version` - Python version specification

## Step 3: Create a Virtual Environment

uv automatically manages virtual environments, but you can explicitly create one:

```bash
# Create a virtual environment with the latest Python version
uv venv

# Or specify a Python version
uv venv --python 3.11
```

The virtual environment is created in `.venv/` directory.

## Step 4: Activate the Virtual Environment

```bash
# On macOS/Linux
source .venv/bin/activate

# On Windows
.venv\Scripts\activate
```

You should see `(.venv)` in your terminal prompt indicating the virtual environment is active.

## Step 5: Install Dependencies from uv.lock

If you have an existing project with a `uv.lock` file (like this one), install all dependencies:

```bash
# Install all dependencies specified in uv.lock
uv sync

# Or if you want to install from pyproject.toml
uv install
```

This will:
- Create a virtual environment if it doesn't exist
- Install all dependencies with exact versions from `uv.lock`
- Ensure reproducible builds across different machines

## Step 6: Adding New Dependencies

Add new packages to your project:

```bash
# Add a runtime dependency
uv add requests

# Add a development dependency
uv add --dev pytest

# Add a dependency with version constraint
uv add "django>=4.0,<5.0"
```

## Step 7: Running Python Code

Run Python scripts using uv:

```bash
# Run a Python file
uv run python main.py

# Run a module
uv run python -m my_module

# Run with specific Python version
uv run --python 3.11 python main.py
```

## Common uv Commands

| Command | Description |
|---------|-------------|
| `uv init` | Initialize a new project |
| `uv add <package>` | Add a dependency |
| `uv remove <package>` | Remove a dependency |
| `uv sync` | Install dependencies from lock file |
| `uv lock` | Generate/update the lock file |
| `uv run <command>` | Run a command in the project environment |
| `uv venv` | Create a virtual environment |
| `uv pip install <package>` | Install package with pip-like interface |

## Troubleshooting

### uv command not found
- Ensure uv is installed and in your PATH
- Restart your terminal after installation
- Check if `~/.local/bin` is in your PATH

### Permission errors
- Don't use `sudo` with uv commands
- Make sure you have write permissions in the project directory

### Python version issues
- Use `uv python list` to see available Python versions
- Use `uv python install 3.11` to install a specific Python version

## Next Steps

1. Start coding in the `src/` directory
2. Add your dependencies with `uv add`
3. Run tests with `uv run pytest` (if you've added pytest)
4. Use `uv sync` to keep dependencies in sync across your team