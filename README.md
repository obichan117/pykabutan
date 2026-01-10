# pykabutan

A clean, beginner-friendly Python library for scraping [kabutan.jp](https://kabutan.jp) (Japanese stock information site).

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/obichan117/pykabutan/blob/main/examples/quickstart.ipynb)
[![Documentation](https://img.shields.io/badge/docs-mkdocs-blue)](https://obichan117.github.io/pykabutan/)

## Installation

```bash
pip install pykabutan
```

## Quick Start

```python
import pykabutan as pk

# Get stock information
ticker = pk.Ticker("7203")  # Toyota
print(ticker.profile.name)      # トヨタ自動車
print(ticker.profile.market)    # 東証P
print(ticker.profile.per)       # 10.5

# Get price history (yfinance-style)
df = ticker.history(period="30d")
print(df)

# Search by industry
results = pk.search_by_industry("電気機器")
for t in results:
    print(t.code, t.name)

# Search by theme
results = pk.search_by_theme("AI")
```

## Features

- Simple, yfinance-style API
- Lazy loading for performance
- Works out of the box with sensible defaults
- No Selenium dependency (lightweight)

## Development

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Run integration tests (real HTTP)
uv run pytest -m integration

# Format code
uv run ruff format .

# Lint
uv run ruff check .
```

## License

MIT
