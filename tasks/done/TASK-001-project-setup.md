# TASK-001: Project Setup

**Status**: in-progress
**Priority**: high

## Description
Initialize the Python project with pyproject.toml, directory structure, and basic configuration using uv.

## Acceptance Criteria
- [ ] Create `pyproject.toml` with uv configuration
- [ ] Set up `src/pykabutan/` package structure
- [ ] Create `__init__.py` with public API exports
- [ ] Add dependencies: requests, beautifulsoup4, pandas, lxml
- [ ] Add dev dependencies: pytest, ruff, mypy
- [ ] Verify `uv sync` works

## File Structure
```
pykabutan/
├── src/
│   └── pykabutan/
│       └── __init__.py
├── tests/
│   ├── integration/
│   └── unit/
├── pyproject.toml
└── README.md
```

## Notes
- Python >=3.10
- No Selenium dependency
- Use uv for package management
- Follow modern Python packaging standards
