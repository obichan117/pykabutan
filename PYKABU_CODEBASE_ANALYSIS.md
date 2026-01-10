# pykabu Codebase Analysis

Source: Original pykabu codebase (private)
Analyzed: 2026-01-10

## Structure Overview

```
pykabu/
├── src/pykabu/
│   ├── core/              # Base scrapers, OHLC, market date utilities
│   ├── public_modules/    # Scrapers for public sites (kabutan, irbank, etc.)
│   ├── private_modules/   # Login-required scrapers (rakuten, monex, shikiho)
│   └── utils/             # Config and secrets
├── apps/                  # Streamlit apps
├── .notebooks/            # 20+ Jupyter experiments
└── tests/
```

---

## Potential Libraries to Extract

### 1. Earnings Calendar System
**Files:**
- `src/pykabu/public_modules/earnings_calendar.py` - Main aggregator (500+ lines)
- `src/pykabu/public_modules/sbi_calendar.py` - SBI Securities calendar
- `src/pykabu/public_modules/matsui_calendar.py` - Matsui Securities calendar
- `src/pykabu/public_modules/monex_calendar.py` - Monex Securities calendar
- `src/pykabu/public_modules/tradersweb_calendar.py` - Tradersweb calendar
- `src/pykabu/core/calendar_scraper.py` - Base calendar scraper

**Functionality:**
- Scrapes earnings announcement dates from multiple broker sites
- Merges calendars from different sources
- Appends stock data from kabutan
- Appends historical price moves around earnings
- Exports to Google Sheets and Google Calendar

**Dependencies:**
- Selenium (for SBI, Matsui)
- kabutan module (for stock info)
- Google services (for export)
- OHLC modules (for price moves)

---

### 2. OHLC Price Data
**Files:**
- `src/pykabu/public_modules/yfinance_ohlc.py` - Yahoo Finance wrapper
- `src/pykabu/public_modules/tradingview.py` - TradingView datafeed
- `src/pykabu/core/ohlc.py` - Base OHLC class
- `src/pykabu/private_modules/jquants.py` - J-Quants API

**Functionality:**
- Unified interface for fetching OHLC data from multiple sources
- Support for different intervals (1m, 5m, 1h, 1d, etc.)
- Price move calculations
- Intraday data support

**Key Classes:**
- `OHLC` (base) - Common interface
- `YahooFinanceOHLC` - yfinance wrapper
- `TradingViewOHLC` - tvDatafeed wrapper
- `JquantsOHLC` - J-Quants API wrapper

---

### 3. Google Services Integration
**Files:**
- `src/pykabu/private_modules/goog/goog_sheet.py` - Google Sheets
- `src/pykabu/private_modules/goog/goog_calendar.py` - Google Calendar
- `src/pykabu/private_modules/goog/service.py` - Service account setup

**Functionality:**
- Upload DataFrames to Google Sheets
- Create/read spreadsheets
- Create calendar events from DataFrames
- Event color coding by market type

**Key Classes:**
- `GoogleSheet` - Sheets CRUD operations
- `GoogleCalendar` - Calendar event management
- `Event`, `EventDateTime` - Event dataclasses

---

### 4. Broker Login Scrapers (Private/Authenticated)
**Files:**
- `src/pykabu/private_modules/rakuten/` - Rakuten Securities
  - `base.py` - Login handling
  - `stock.py` - Stock info
  - `shikiho.py` - Shikiho data via Rakuten
  - `ifis.py` - IFIS analyst data
  - `user.py` - User account info
- `src/pykabu/private_modules/monex/` - Monex Securities
  - `base.py` - Login handling
  - `scouter.py` - Monex stock scouter
- `src/pykabu/private_modules/shikiho/` - Shikiho Online
  - `stock.py` - Stock analysis
  - `tairyo.py` - Large volume data

**Functionality:**
- Selenium-based login to broker sites
- Scrape subscription-only data
- Shikiho (Company Handbook) analysis data
- Analyst consensus data

**Note:** Requires credentials in .env file

---

### 5. Market Utilities
**Files:**
- `src/pykabu/core/market_date.py` - JpxDate, TradingHours
- `src/pykabu/public_modules/jpx_symbols.py` - JPX symbol list
- `src/pykabu/public_modules/irbank.py` - IRBank earnings revisions

**Functionality:**
- Japanese market date handling (holidays, trading days)
- Trading hours detection (zaraba, before/after hours)
- Official JPX symbol list download
- ETF symbol list

**Key Classes:**
- `JpxDate` - Market-aware date class
- `TradingHours` - Trading session detection

---

### 6. Applications
**Files:**
- `apps/candle_screener.py` - Candlestick pattern screener
- `apps/earnings_calendar_app.py` - Earnings calendar Streamlit app
- `apps/obichan_scouter.py` - Stock scouter app

---

### 7. Jupyter Notebooks (Experiments)
**Location:** `.notebooks/`

| Notebook | Purpose |
|----------|---------|
| `kabutan.ipynb` | Kabutan scraping experiments |
| `earnings_calendar.ipynb` | Calendar aggregation tests |
| `backtest.ipynb` | Backtesting experiments |
| `screening.ipynb` | Stock screening |
| `shikiho.ipynb` | Shikiho data analysis |
| `jquants.ipynb` | J-Quants API tests |
| `tradingview.ipynb` | TradingView data tests |
| `monex_scouter.ipynb` | Monex scouter tests |
| `rakuten_shikiho.ipynb` | Rakuten Shikiho tests |
| `google_calendar.ipynb` | Google Calendar integration |
| `yahoo_comment.ipynb` | Yahoo Finance comments |
| `price_moves.ipynb` | Price movement analysis |

---

## Core Dependencies

```toml
# From pyproject.toml
requests = "^2.32.3"
bs4 = "^0.0.2"
selenium = "^4.21.0"
pandas = "^1.4.3"
lxml = "^5.2.2"
yfinance = "^0.2.40"
gspread = "^6.1.2"
jquants-api-client = "^1.6.1"
tvdatafeed = { git = "https://github.com/rongardF/tvdatafeed.git" }
webdriver-manager = "^4.0.1"
google-api-python-client = "^2.137.0"
streamlit = "^1.36.0"
```

---

## Suggested Library Breakdown

| Library | Description | Dependencies |
|---------|-------------|--------------|
| `pykabutan` | kabutan.jp scraper | requests, bs4, pandas, lxml |
| `pykabu-calendar` | Earnings calendar aggregator | selenium, pykabutan, pykabu-ohlc |
| `pykabu-ohlc` | Multi-source OHLC data | yfinance, tvdatafeed, jquants |
| `pykabu-goog` | Google Sheets/Calendar | gspread, google-api |
| `pykabu-brokers` | Authenticated broker scrapers | selenium |
| `pykabu-market` | Market utilities | pandas |

---

## Notes

- `earnings_calendar.py` is the most complex file - it ties everything together
- Broker scrapers require credentials and are private use only
- Many notebooks are one-off experiments, not production code

---

## Design Decisions (2026-01-10)

### pykabutan scope
- **Keep focused**: Only kabutan.jp scraping functionality
- **Exclude**: `JpxDate`, `jpx_symbols()`, `TradingHours` - these belong in `pykabu-market`

### Rationale for excluding market utilities from pykabutan:

**`jpx_symbols()`** - List of all JPX stocks
- Use case: Bulk operations on all stocks, filtering by market
- But: kabutan's `search.by_industry()` provides similar functionality
- Decision: Keep in separate `pykabu-market` library

**`JpxDate`** - Market-aware date handling
- Use case: Trading day detection, next/previous trading day
- But: Not needed for basic kabutan scraping
- Decision: Keep in separate `pykabu-market` library (useful for calendar/scheduling)

**`TradingHours`** - Trading session detection
- Use case: Detect if time is during market hours (zaraba)
- But: Only needed for earnings calendar features
- Decision: Keep in separate `pykabu-market` library

---

## pykabutan Final Design

See `.claude/CLAUDE.md` for full specification.

### Summary

```python
import pykabutan as pk

ticker = pk.Ticker("7203")
ticker.profile.name           # Lazy loaded, cached
ticker.profile.per
ticker.history(period="30d")  # yfinance style
ticker.news(mode="earnings")
ticker.financials()
ticker.holders()

pk.search_by_industry("電気機器")
pk.search_by_theme("AI")
```

### Key Decisions
- `Ticker` class (yfinance convention)
- `profile` contains all main page data (page-based caching)
- `history()` method (yfinance style)
- Top-level `search_by_*` functions
- Lazy loading, in-memory cache
- No Selenium (lightweight)
- Hybrid error handling (None for missing, exceptions for errors)
