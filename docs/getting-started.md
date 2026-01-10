# Getting Started

## Try it Online

No installation needed - try pykabutan directly in Google Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/obichan117/pykabutan/blob/main/examples/quickstart.ipynb)

## Installation

Install pykabutan using pip:

```bash
pip install pykabutan
```

Or with uv:

```bash
uv add pykabutan
```

## Basic Usage

### Import the library

```python
import pykabutan as pk
```

### Get stock information

Create a `Ticker` object with a stock code:

```python
ticker = pk.Ticker("7203")  # Toyota Motor Corporation
```

Access the company profile:

```python
profile = ticker.profile

print(profile.name)      # トヨタ自動車
print(profile.market)    # 東証Ｐ
print(profile.industry)  # 輸送用機器
print(profile.per)       # Price-to-earnings ratio
print(profile.pbr)       # Price-to-book ratio
```

### Get historical prices

```python
# Last 30 days
df = ticker.history(period="30d")

# Last 90 days, weekly data
df = ticker.history(period="90d", interval="week")

# Specific number of rows
df = ticker.history(rows=100)
```

The returned DataFrame contains:

| Column | Description |
|--------|-------------|
| date | Trading date |
| open | Opening price |
| high | High price |
| low | Low price |
| close | Closing price |
| volume | Trading volume |
| change | Price change from previous day |

### Search for stocks

Search by industry:

```python
# Get all electronics companies
results = pk.search_by_industry("電気機器")

for ticker in results[:5]:
    print(f"{ticker.code}: {ticker.name}")
```

Search by theme:

```python
# Search for AI-related stocks (use Japanese terms)
results = pk.search_by_theme("人工知能")
```

List available industries:

```python
industries = pk.list_industries()
print(industries)
```

## Configuration

Configure request behavior:

```python
# Set timeout (seconds)
pk.config.timeout = 60

# Set delay between requests (seconds)
pk.config.request_delay = 1.0

# Reset to defaults
pk.config.reset()
```

## Error Handling

```python
from pykabutan import TickerNotFoundError

try:
    ticker = pk.Ticker("9999999")
    profile = ticker.profile
except TickerNotFoundError as e:
    print(f"Ticker not found: {e.code}")
```

## Next Steps

- [Ticker Guide](guide/ticker.md) - Detailed ticker usage
- [Search Guide](guide/search.md) - Advanced search options
- [API Reference](api/ticker.md) - Complete API documentation
