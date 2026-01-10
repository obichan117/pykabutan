# Ticker Guide

The `Ticker` class is the main interface for accessing stock data.

## Creating a Ticker

```python
import pykabutan as pk

# Using string code
ticker = pk.Ticker("7203")

# Using integer code
ticker = pk.Ticker(7203)
```

!!! note "Lazy Loading"
    Creating a Ticker does not make any HTTP requests. Data is fetched only when you access properties like `profile` or call methods like `history()`.

## Profile

Access company profile information:

```python
profile = ticker.profile

# Basic info
print(profile.code)     # 7203
print(profile.name)     # トヨタ自動車
print(profile.market)   # 東証Ｐ
print(profile.industry) # 輸送用機器

# Description and themes
print(profile.description)  # Company description
print(profile.themes)       # ['EV', '自動運転', ...]

# Financial metrics
print(profile.per)            # Price-to-earnings ratio
print(profile.pbr)            # Price-to-book ratio
print(profile.market_cap)     # Market capitalization
print(profile.dividend_yield) # Dividend yield
print(profile.margin_ratio)   # Profit margin

# Additional info
print(profile.website)      # Company website
print(profile.english_name) # English company name
```

### Convert to Dictionary

```python
# Using dict()
data = dict(ticker.profile)

# Using to_dict()
data = ticker.profile.to_dict()
```

## Historical Prices

Get historical OHLCV data:

```python
# Default: 30 days of daily data
df = ticker.history()

# Specify period
df = ticker.history(period="7d")   # Last 7 days
df = ticker.history(period="30d")  # Last 30 days
df = ticker.history(period="90d")  # Last 90 days

# Specify interval
df = ticker.history(interval="day")   # Daily (default)
df = ticker.history(interval="week")  # Weekly
df = ticker.history(interval="month") # Monthly

# Specify number of rows
df = ticker.history(rows=100)

# Combine options
df = ticker.history(period="90d", interval="week")
```

### DataFrame Columns

| Column | Type | Description |
|--------|------|-------------|
| date | datetime64 | Trading date |
| open | float | Opening price |
| high | float | High price |
| low | float | Low price |
| close | float | Closing price |
| volume | int | Trading volume |
| change | float | Price change |

## News

Get company news:

```python
# All news types
news = ticker.news()

# Filter by type
news = ticker.news(news_type="earnings")  # Earnings announcements
news = ticker.news(news_type="general")   # General news
news = ticker.news(news_type="disclosure") # Disclosures
```

### News DataFrame Columns

| Column | Description |
|--------|-------------|
| date | Publication date |
| time | Publication time |
| title | News headline |
| url | Link to full article |

## Financials

Get financial statements:

```python
df = ticker.financials()
```

Returns quarterly/annual financial data including revenue, profit, and other metrics.

## Shareholders

Get shareholder information:

```python
# Major shareholders (default)
df = ticker.holders()

# Specify holder type
df = ticker.holders(holder_type="major")      # Major shareholders
df = ticker.holders(holder_type="float")      # Float shareholders
df = ticker.holders(holder_type="treasury")   # Treasury stock info
```

## Similar Stocks

Find stocks similar to this one:

```python
similar = ticker.similar_stocks()

for t in similar:
    print(f"{t.code}: {t.profile.name}")
```

## Caching

Profile data is cached after the first access:

```python
ticker = pk.Ticker("7203")

# First access: makes HTTP request
profile1 = ticker.profile

# Second access: uses cache (no HTTP request)
profile2 = ticker.profile
```

### Clearing Cache

```python
# Clear cache and force refresh
ticker.refresh()

# Next access will make a new HTTP request
profile = ticker.profile
```

## Error Handling

```python
from pykabutan import TickerNotFoundError, ScrapingError

try:
    ticker = pk.Ticker("9999999")
    profile = ticker.profile
except TickerNotFoundError as e:
    print(f"Stock code not found: {e.code}")
except ScrapingError as e:
    print(f"Failed to scrape: {e.url}")
```
