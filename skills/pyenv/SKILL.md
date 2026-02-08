---
name: pyenv
description: "Setup Python project using local conda environment to save disk space. Use when user says 'pyenv', 'setup python', or needs to configure Python for a project. Keywords: pyenv, python, conda, venv, 环境, Python环境, 虚拟环境"
---

# Python Environment Setup

Use local conda environments instead of creating new venv/.venv to save disk space.

## Conda Base Path

```
~/dev/mcd3
```

## Workflow

1. **Detect Python version** (priority order):
   - User argument: `/pyenv 3.10`
   - `.python-version` file
   - `pyproject.toml` → `requires-python`
   - `setup.py` → `python_requires`
   - Default: Python 3.10

2. **Check available environments**:
   ```bash
   ~/dev/mcd3/bin/conda env list
   ```

   Current environments:
   - `py310` → Python 3.10
   - `openhands` → Python 3.x
   - `code-agent` → Python 3.x

3. **Activate environment**:
   ```bash
   source ~/dev/mcd3/bin/activate <env_name>
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt   # For requirements.txt
   pip install -e .                  # For pyproject.toml or setup.py
   ```

5. **Output activation command**:
   ```
   To activate in your terminal:
   source ~/dev/mcd3/bin/activate <env_name>
   ```

## Important Rules

- **NEVER** create `.venv` or use `python -m venv`
- **NEVER** use `uv venv` to create virtual environments
- **ALWAYS** prefer existing conda environments
- If conflicts occur, create NEW conda environment (not venv)

## Create New Conda Environment

```bash
~/dev/mcd3/bin/conda create -n <name> python=<version> -y
source ~/dev/mcd3/bin/activate <name>
```

## Examples

| Command | Action |
|---------|--------|
| `/pyenv` | Auto-detect version and setup |
| `/pyenv 3.10` | Use Python 3.10 environment |
| `/pyenv 3.11` | Use or create Python 3.11 environment |
