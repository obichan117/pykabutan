# pykabutan

A Python library for scraping Japanese stock data from [kabutan.jp](https://kabutan.jp).

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/obichan117/pykabutan/blob/main/examples/quickstart.ipynb)

## Features

- **Ticker data**: Company profiles, historical prices, news, financials, shareholders
- **Search**: Find stocks by industry or theme
- **yfinance-style API**: Familiar interface for Python developers
- **Lazy loading**: HTTP requests only when data is accessed
- **Built-in rate limiting**: Respectful scraping with configurable delays

## Quick Example

```python
import pykabutan as pk

# Get stock data
ticker = pk.Ticker("7203")  # Toyota
print(ticker.profile.name)   # トヨタ自動車
print(ticker.profile.market) # 東証Ｐ

# Get historical prices
df = ticker.history(period="30d")
print(df.head())

# Search by industry
results = pk.search_by_industry("電気機器")
print(f"Found {len(results)} stocks")
```

## Installation

```bash
pip install pykabutan
```

Or with uv:

```bash
uv add pykabutan
```

## Requirements

- Python 3.10+
- requests
- beautifulsoup4
- pandas
- lxml

## License

MIT
