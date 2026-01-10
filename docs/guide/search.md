# Search Guide

pykabutan provides functions to search for stocks by industry or theme.

## Search by Industry

Find stocks in a specific industry:

```python
import pykabutan as pk

# Search electronics industry
results = pk.search_by_industry("電気機器")

print(f"Found {len(results)} stocks")
for ticker in results[:5]:
    print(f"{ticker.code}: {ticker.name}")
```

### Available Industries

Japan has 33 standard industry classifications. List them with:

```python
industries = pk.list_industries()
for industry in industries:
    print(industry)
```

Common industries include:

| Japanese | English |
|----------|---------|
| 電気機器 | Electronics |
| 輸送用機器 | Transportation Equipment |
| 情報・通信業 | Information & Communication |
| 銀行業 | Banking |
| 医薬品 | Pharmaceuticals |
| 小売業 | Retail |
| サービス業 | Services |
| 化学 | Chemicals |
| 機械 | Machinery |
| 建設業 | Construction |

### Filter by Market

```python
# Prime market only
results = pk.search_by_industry("電気機器", market="Prime")

# Standard market only
results = pk.search_by_industry("電気機器", market="Standard")

# Growth market only
results = pk.search_by_industry("電気機器", market="Growth")
```

Market options:

| Value | Description |
|-------|-------------|
| `"Prime"` or `"東証Ｐ"` | Tokyo Stock Exchange Prime |
| `"Standard"` or `"東証Ｓ"` | Tokyo Stock Exchange Standard |
| `"Growth"` or `"東証Ｇ"` | Tokyo Stock Exchange Growth |

## Search by Theme

Find stocks related to a specific theme or keyword:

```python
# Search for AI-related stocks
results = pk.search_by_theme("人工知能")

# Search for EV-related stocks
results = pk.search_by_theme("EV")

# Search for semiconductor stocks
results = pk.search_by_theme("半導体")
```

!!! warning "Use Japanese Terms"
    Theme search works best with Japanese terms. While some English terms like "EV" work, Japanese terms like "人工知能" (AI) or "半導体" (semiconductor) yield better results.

### Filter by Market

```python
# Prime market only
results = pk.search_by_theme("人工知能", market="Prime")
```

## Return Value

Both search functions return a list of `SearchResult` named tuples:

```python
results = pk.search_by_industry("電気機器")

for result in results:
    print(result.code)   # Stock code
    print(result.name)   # Company name
    print(result.market) # Market (if available)
```

### Create Ticker from Result

```python
results = pk.search_by_industry("電気機器")

# Get the first result as a Ticker
first = results[0]
ticker = pk.Ticker(first.code)

# Access full profile
print(ticker.profile.name)
print(ticker.profile.per)
```

## Error Handling

```python
# Invalid industry raises ValueError
try:
    results = pk.search_by_industry("invalid_industry")
except ValueError as e:
    print(e)
    # "Unknown industry: invalid_industry. Available: ..."
```

## Rate Limiting

Search functions respect the configured rate limit:

```python
# Increase delay between requests if needed
pk.config.request_delay = 1.0

# Then perform searches
results1 = pk.search_by_industry("電気機器")
results2 = pk.search_by_industry("銀行業")  # Waits 1 second before request
```
