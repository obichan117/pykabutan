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
print(profile.per)            # Price-to-earnings ratio (None if loss-making)
print(profile.pbr)            # Price-to-book ratio
print(profile.market_cap)     # Market capitalization, in yen
print(profile.dividend_yield) # Dividend yield (%)
print(profile.margin_ratio)   # Margin trading ratio

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
# Default: last 30 calendar days of daily data
df = ticker.history()

# Specify period (calendar time, not row count)
df = ticker.history(period="7d")    # Last 7 days
df = ticker.history(period="30d")   # Last 30 days
df = ticker.history(period="6mo")   # Last 6 months
df = ticker.history(period="1y")    # Last year

# Specify interval
df = ticker.history(interval="day")   # Daily (default)
df = ticker.history(interval="week")  # Weekly
df = ticker.history(interval="month") # Monthly
df = ticker.history(interval="year")  # Yearly

# Explicit date range (overrides period)
df = ticker.history(start="2024-01-01", end="2024-12-31")

# Combine options
df = ticker.history(period="90d", interval="week")
```

!!! note "period is calendar time, not row count"
    `period="30d"` means "the last 30 calendar days," not "30 rows." Weekends,
    holidays, and non-trading days reduce the row count accordingly.

### DataFrame Columns

The DataFrame is indexed by an ascending `date` `DatetimeIndex`:

| Column | Type | Description |
|--------|------|-------------|
| open | float | Opening price |
| high | float | High price |
| low | float | Low price |
| close | float | Closing price |
| change | float | Price change from previous close |
| percent_change | float | Price change (%) from previous close |
| volume | int | Trading volume |

Since the index is a `DatetimeIndex`, you can slice by date directly:

```python
df.loc["2024-06"]              # every row in June 2024
df.loc["2024-01-01":"2024-03-31"]  # a date range
```

## News

Get company news:

```python
# Earnings announcements (default)
news = ticker.news()

# Filter by mode
news = ticker.news(mode="all")         # All news
news = ticker.news(mode="material")    # Material news (適時開示)
news = ticker.news(mode="earnings")    # Earnings announcements
news = ticker.news(mode="disclosure")  # Disclosures
```

### News DataFrame Columns

| Column | Description |
|--------|-------------|
| datetime | Publication date and time |
| news_type | News category label |
| title | News headline |

An empty DataFrame is returned when the stock has no news for the requested mode.

## Financials

Get financial statements from the finance page:

```python
statements = ticker.financials()

statements.keys()          # dict_keys(["annual", "interim", ...])
statements["annual"]       # full-year results + current forecast
```

`financials()` returns a `dict[str, pd.DataFrame]`. Keys are present only when
kabutan publishes that statement for the stock:

| Key | Description |
|-----|-------------|
| `annual` | Full-year results + current forecast |
| `interim` | Half-year results + forecast |
| `quarterly` | Recent quarterly results |
| `cashflow` | Operating / investing / financing / free cash flow |
| `profitability` | ROE / ROA / margin history |
| `financial_position` | Equity ratio, total assets, retained earnings |
| `records` | All-time-high results |

!!! note "Units"
    Money values are in **百万円 (millions of yen)**, as published by kabutan.
    Some historical profit data is gated behind 株探プレミアム and is excluded.

## Shareholders

Get shareholder information:

```python
# Latest reporting period (default)
df = ticker.holders()

# Previous reporting period
df = ticker.holders(period=1)
```

`period` selects the reporting period: `0` is the latest, `1` is the previous
one, and so on. The DataFrame columns are `name`, `change`, `ratio_percent`,
`shares` (plus a leading `date` column with the reporting-period label, when
available).

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
    print(f"Failed to parse {e.what} — kabutan.jp may have changed its layout")
```
