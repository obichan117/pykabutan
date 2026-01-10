# TASK-015: Documentation

**Status**: todo
**Priority**: medium

## Description
Create user documentation with MkDocs and Material theme.

## Acceptance Criteria
- [ ] Set up MkDocs with Material theme
- [ ] Write getting started guide
- [ ] Document all public API
- [ ] Add code examples
- [ ] Configure GitHub Pages deployment

## Documentation Structure
```
docs/
├── index.md              # Getting started
├── guide/
│   ├── installation.md
│   ├── quickstart.md
│   └── configuration.md
├── api/
│   ├── ticker.md
│   ├── search.md
│   └── exceptions.md
└── examples/
    ├── basic-usage.md
    └── rest-api.md
```

## Content Outline

### Getting Started
- Installation: `pip install pykabutan`
- Basic usage example
- Link to full API docs

### Ticker Class
- All properties and methods
- Code examples
- Return types

### Search Functions
- search_by_industry()
- search_by_theme()
- Industry list reference

### Configuration
- Default values
- How to customize
- Config file format

## Notes
- Follow user's preference: MkDocs + Material
- Keep examples simple and runnable
- Include REST API mapping for those building APIs
