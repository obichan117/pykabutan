# pykabutan

A clean, beginner-friendly Python library for scraping kabutan.jp (Japanese stock information site).

## Project Goals

- Simple, yfinance-style API
- Works out of the box with sensible defaults
- Designed for both Python API and REST API usage
- Lazy loading for performance
- No Selenium dependency (lightweight)

## Source Reference

Refactored from original pykabu codebase.
See: `PYKABU_CODEBASE_ANALYSIS.md` for original codebase analysis.

---

## Target API Design

### Basic Usage

```python
import pykabutan as pk

# Single ticker
ticker = pk.Ticker("7203")

# Profile (from main page - cached)
ticker.profile.name           # "トヨタ自動車"
ticker.profile.market         # "東証P"
ticker.profile.industry       # "輸送用機器"
ticker.profile.description    # Company description
ticker.profile.themes         # ["EV", "自動運転", ...]
ticker.profile.website        # Company URL
ticker.profile.english_name   # "TOYOTA MOTOR CORPORATION"
ticker.profile.per            # 10.5
ticker.profile.pbr            # 1.2
ticker.profile.market_cap     # 35000000000000
ticker.profile.dividend_yield # 2.5
ticker.profile.margin_ratio   # 3.2

dict(ticker.profile)          # All fields as dict (for JSON serialization)

# Price history (yfinance style)
ticker.history(period="30d")                    # Daily, last 30 days
ticker.history(period="1y", interval="week")   # Weekly, last year
ticker.history(start="2024-01-01", end="2024-12-31")  # Date range

# Other data (separate pages - not cached)
ticker.news(mode="earnings")  # DataFrame: earnings announcements
ticker.news(mode="all")       # DataFrame: all news
ticker.financials()           # Dict of DataFrames
ticker.holders()              # DataFrame: shareholder info
ticker.similar_stocks()       # List[Ticker]: similar companies

# Search functions
tickers = pk.search_by_industry("電気機器")
tickers = pk.search_by_theme("AI")

# Search results have cached basic info from search page
for t in tickers[:5]:
    print(t.code, t.profile.name)  # HTTP request for each profile
    print(t.profile.description)  # HTTP request (detailed info)
```

### Configuration (Optional)

```python
import pykabutan as pk

# Module-level config
pk.config.timeout = 60          # Request timeout (seconds)
pk.config.request_delay = 1.0   # Delay between requests (seconds)
pk.config.user_agent = "..."    # Custom user agent

# Or via config file: ~/.pykabutan/config.json
# {
#   "timeout": 60,
#   "request_delay": 1.0
# }
```

---

## REST API Mapping

| Python | REST Endpoint | Kabutan Page |
|--------|---------------|--------------|
| `pk.Ticker("7203")` | - | - |
| `ticker.profile` | `GET /ticker/7203/profile` | `/stock/?code=7203` |
| `ticker.history()` | `GET /ticker/7203/history?period=30d` | `/stock/kabuka?code=7203` |
| `ticker.news()` | `GET /ticker/7203/news?mode=earnings` | `/stock/news?code=7203` |
| `ticker.financials()` | `GET /ticker/7203/financials` | `/stock/finance?code=7203` |
| `ticker.holders()` | `GET /ticker/7203/holders` | `/stock/holder?code=7203` |
| `pk.search_by_industry()` | `GET /search/industry/{name}` | `/themes/?industry=` |
| `pk.search_by_theme()` | `GET /search/theme/{name}` | `/themes/?theme=` |

---

## Design Decisions

### Scope
- **Included**: All kabutan.jp scraping (profile, history, news, financials, holders, search)
- **Excluded**: Screenshots (no Selenium), JpxDate, jpx_symbols, TradingHours

### Architecture
- **Lazy loading**: Data fetched only when accessed
- **High-level API only**: Scraper internals hidden from users
- **yfinance conventions**: `Ticker` class, `history()` method, familiar to Python traders

### Data Structure
- **Page-based objects**: `ticker.profile` = entire main page (natural caching boundary)
- **Methods for dynamic data**: `history()`, `news()`, `financials()`, `holders()`

### Caching
- **In-memory, per session**: Profile cached, methods not cached
- **Page-level caching**: One kabutan page = one cache entry
- **No disk cache**: Keep it simple

### Error Handling
- **Missing data**: Return `None` (expected for ETFs, etc.)
- **Invalid ticker code**: Raise `TickerNotFoundError`
- **Network errors**: Raise `ConnectionError`
- **Parsing errors**: Raise `ScrapingError`

### Rate Limiting
- **Built-in default**: ~0.5s delay between requests
- **Configurable**: `pk.config.request_delay`

### Configuration
- **Sensible defaults**: Works out of the box
- **Module-level config**: `pk.config.*`
- **File-based config**: `~/.pykabutan/config.json` (optional)

---

## Target File Structure

```
pykabutan/
├── src/
│   └── pykabutan/
│       ├── __init__.py          # Public API: Ticker, search_by_*, config
│       ├── ticker.py            # Ticker class
│       ├── profile.py           # Profile dataclass
│       ├── search.py            # search_by_industry, search_by_theme
│       ├── config.py            # Configuration management
│       ├── exceptions.py        # TickerNotFoundError, ScrapingError
│       └── _scraper.py          # Internal: HTTP requests, parsing (hidden)
├── tests/
│   ├── test_ticker.py
│   ├── test_search.py
│   └── test_config.py
├── pyproject.toml
├── README.md
└── .claude/
    └── CLAUDE.md               # This file
```

---

## Dependencies

```toml
[tool.poetry.dependencies]
python = ">=3.10,<4.0"
requests = "^2.32"
beautifulsoup4 = "^4.12"
pandas = "^2.0"
lxml = "^5.0"
```

**Note**: No Selenium. Lightweight library.

---

## Kabutan URL Reference

| Page | URL Pattern | Data |
|------|-------------|------|
| Main | `https://kabutan.jp/stock/?code={code}` | name, market, industry, description, themes, PER, PBR, etc. |
| OHLC | `https://kabutan.jp/stock/kabuka?code={code}&ashi={interval}&page={page}` | Price history |
| News | `https://kabutan.jp/stock/news?code={code}&nmode={mode}` | News (0=all, 1=material, 2=earnings, 3=disclosure) |
| Finance | `https://kabutan.jp/stock/finance?code={code}` | Financial statements |
| Holders | `https://kabutan.jp/stock/holder?code={code}&tab={tab}` | Shareholders |
| Industry | `https://kabutan.jp/themes/?industry={code}&market={market}` | Stocks by industry |
| Theme | `https://kabutan.jp/themes/?theme={encoded_theme}` | Stocks by theme |

### Interval Mapping (history)

| pykabutan | kabutan `ashi` |
|-----------|----------------|
| `"day"` / `"1d"` | `day` |
| `"week"` / `"1w"` | `wek` |
| `"month"` / `"1mo"` | `mon` |
| `"year"` / `"1y"` | `yar` |

### News Mode Mapping

| pykabutan | kabutan `nmode` |
|-----------|-----------------|
| `"all"` | `0` |
| `"material"` | `1` |
| `"earnings"` | `2` |
| `"disclosure"` | `3` |

---

## Industry Code Reference

```python
INDUSTRY_MAP = {
    "水産・農林業": 1,
    "鉱業": 2,
    "建設業": 3,
    "食料品": 4,
    "繊維製品": 5,
    "パルプ・紙": 6,
    "化学": 7,
    "医薬品": 8,
    "石油・石炭": 9,
    "ゴム製品": 10,
    "ガラス・土石": 11,
    "鉄鋼": 12,
    "非鉄金属": 13,
    "金属製品": 14,
    "機械": 15,
    "電気機器": 16,
    "輸送用機器": 17,
    "精密機器": 18,
    "その他製品": 19,
    "電気・ガス": 20,
    "陸運業": 21,
    "海運業": 22,
    "空運業": 23,
    "倉庫・運輸": 24,
    "情報・通信業": 25,
    "卸売業": 26,
    "小売業": 27,
    "銀行業": 28,
    "証券・商品": 29,
    "保険業": 30,
    "その他金融業": 31,
    "不動産業": 32,
    "サービス業": 33,
}
```

---

## Quick Start Commands

```bash
# Setup
uv sync

# Run tests
uv run pytest

# Run single test
uv run pytest tests/test_ticker.py -v

# Format code
uv run ruff format .

# Lint
uv run ruff check .

# Serve docs
uv run mkdocs serve
```

---

## Implementation Notes

1. **Start with `_scraper.py`**: Port the HTTP/parsing logic from original `kabutan.py`
2. **Build `Profile` dataclass**: All main page fields with `__iter__` for dict conversion
3. **Build `Ticker` class**: Lazy loading with cached `profile` property
4. **Add methods**: `history()`, `news()`, `financials()`, `holders()`, `similar_stocks()`
5. **Add search functions**: `search_by_industry()`, `search_by_theme()`
6. **Add config**: Module-level + file-based
7. **Add exceptions**: `TickerNotFoundError`, `ScrapingError`
8. **Write tests**: Mock HTTP responses for reliable testing
