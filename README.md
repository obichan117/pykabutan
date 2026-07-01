# pykabutan

A clean, beginner-friendly Python library for scraping [kabutan.jp](https://kabutan.jp) (Japanese stock information site).

[![PyPI version](https://img.shields.io/pypi/v/pykabutan)](https://pypi.org/project/pykabutan/)
[![Python versions](https://img.shields.io/pypi/pyversions/pykabutan)](https://pypi.org/project/pykabutan/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/obichan117/pykabutan)
[![Documentation](https://img.shields.io/badge/docs-mkdocs-blue)](https://obichan117.github.io/pykabutan/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/obichan117/pykabutan/blob/main/examples/quickstart.ipynb)

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

# Get price history (yfinance-style), indexed by date
df = ticker.history(period="30d")
print(df)

# Get financial statements (dict of DataFrames, values in 百万円)
financials = ticker.financials()
print(financials["annual"])

# Search by industry
results = pk.search_by_industry("電気機器")
for t in results[:5]:
    print(t.code, t.profile.name)

# Search by theme (Japanese terms only)
results = pk.search_by_theme("人工知能")
```

## Features

- Simple, yfinance-style API
- Lazy loading for performance
- Works out of the box with sensible defaults
- No Selenium dependency (lightweight)

## What's New in 0.2.0

- **Real `financials()`**: parses the finance page into a dict of DataFrames
  (`annual`, `interim`, `quarterly`, `cashflow`, `profitability`,
  `financial_position`, `records`), values in 百万円 (millions of yen).
- **Calendar-accurate `history()` periods**: `period="30d"` / `"6mo"` /
  `"1y"` now mean actual calendar time, not a row count.
- **Connection reuse + retries**: HTTP requests share a pooled `requests`
  session with automatic retries on transient errors (429/500/502/503).
- **`ScrapingError`**: raised (with a `.what` attribute) when kabutan.jp's
  page structure changes and a page can't be parsed.

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
