# Skill Folder: python-project-structure

## File: SKILL.md

```markdown
---
name: python-project-structure
description: Create Python project structure using UV package manager with proper folder organization, pyproject.toml, and virtual environment setup. Use when starting a new Python project, setting up UV-based projects, or organizing Python code with best practices.
---

# Python Project Structure Skill

## Purpose
Set up a professional Python project structure using UV package manager with all necessary configuration files and folder organization.

## When to Use This Skill
- Starting a new Python project
- Setting up UV-based project
- Creating console applications
- Organizing Python code with best practices
- Need proper virtual environment setup

## Instructions

### Step 1: Create Project Structure
```bash
mkdir project-name
cd project-name
mkdir -p src/project_name tests specs
```

### Step 2: Create pyproject.toml
```toml
[project]
name = "project-name"
version = "0.1.0"
description = "Project description"
requires-python = ">=3.13"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
]
```

### Step 3: Create Source Structure
```
src/project_name/
├── __init__.py
├── main.py       # Entry point
├── models.py     # Data models
├── services.py   # Business logic
├── storage.py    # Data storage
└── utils.py      # Helper functions
```

### Step 4: Create .gitignore
```
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
.pytest_cache/
.coverage
*.egg-info/
dist/
build/
```

### Step 5: Initialize UV Environment
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### Step 6: Create README.md
Include:
- Project description
- Installation instructions with UV
- Usage examples
- Development setup

### Step 7: Create CLAUDE.md
Document:
- Project structure explanation
- How to run the project
- Development commands
- Testing instructions

## Validation Checklist
- [ ] All folders created
- [ ] pyproject.toml is valid TOML
- [ ] UV can create virtual environment
- [ ] Project installs with `uv pip install -e .`
- [ ] Import works: `from project_name import main`
- [ ] .gitignore covers common Python artifacts

## Best Practices
1. Use src/ layout for better import resolution
2. Keep package name as valid Python identifier (underscores, not hyphens)
3. Separate tests from source code
4. Include type hints in all code
5. Document setup in README.md

## Common Pitfalls to Avoid
- Don't use hyphens in package folder name (use underscores)
- Don't forget __init__.py files
- Don't commit .venv/ to git
- Don't mix package name formats (stick to one style)

## Example Project Structure
```
todo-console-app/
├── .gitignore
├── pyproject.toml
├── README.md
├── CLAUDE.md
├── src/
│   └── todo_app/
│       ├── __init__.py
│       ├── main.py
│       ├── models.py
│       ├── services.py
│       ├── storage.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_storage.py
└── specs/
    ├── constitution.md
    └── features/
        └── task-crud.md
```
```

## Supporting Files

Create `examples.md` in the same folder:

```markdown
# Python Project Structure Examples

## Minimal Console App
```bash
mkdir todo-app
cd todo-app

# Create structure
mkdir -p src/todo_app tests specs

# Create pyproject.toml
cat > pyproject.toml << 'EOF'
[project]
name = "todo-app"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = []
EOF

# Initialize UV
uv venv
source .venv/bin/activate
uv pip install -e .
```

## With Dependencies
```toml
[project]
dependencies = [
    "rich>=13.0.0",  # For beautiful CLI output
    "typer>=0.9.0",  # For CLI framework
]
```

## Development Commands
```bash
# Install in editable mode
uv pip install -e .

# Install dev dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run application
python -m todo_app.main
```
```