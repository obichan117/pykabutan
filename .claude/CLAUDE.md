# pykabutan

A clean, beginner-friendly Python library for scraping kabutan.jp (Japanese stock information site). Published on PyPI (0.1.1); currently being refactored toward 0.2.0.

## Quick Start Commands

```bash
uv sync                                  # Setup
uv run pytest -m "not integration"       # Unit tests (fast, mocked)
uv run pytest tests/integration          # Integration tests (hit live kabutan.jp)
uv run ruff check . && uv run ruff format .
uv run mkdocs serve                      # Docs preview
uv run mkdocs build --strict             # Docs build check
```

## Audit Summary (2026-07-02)

Full audit performed after ~6 months without maintenance. Key results:

- **Live site verified unchanged**: every parsing assumption (table indices 5/3/2, `match="PBR"`/`"概要"`/`"株主名"`, all CSS selectors, date formats) still holds against kabutan.jp as of 2026-07-02. All 29 integration tests pass.
- **Confirmed bugs**: `similar_stocks()` drops alphanumeric codes (e.g. `277A`) due to `isdigit()` check; 404 detection via `"404" in str(e)` string match; `__version__` out of sync with pyproject.
- **`market_cap` is in 億円, not yen** — digit-concatenation of `39兆7,640億円` → `397640.0` happens to be correct in 億円. Docs claimed yen. 0.2.0 converts to yen.
- **Loss-making companies**: kabutan shows PER as `－倍` → parsed as `None` (acceptable, documented).
- **Finance page is partially paywalled** (株探プレミアム): historical profit columns unavailable; `financials()` parses only free tables and must match tables by column names, not index (25 tables, layout varies by company).
- **Docs had drifted badly**: documented `news(news_type=)` / `holders(holder_type=)` params never existed (real: `mode`, `period`); phantom `SearchResult` type; mkdocstrings directives present but plugin never configured.
- **Test suite was tautological**: fixtures written to match parsers; all risky logic (history pagination, period parsing, search parsing, stats cleaning) had zero unit coverage.

## Architecture (0.2.0 — implemented 2026-07-02)

```
src/pykabutan/
├── __init__.py        # Public API: Ticker, search_*, config, exceptions
├── ticker.py          # Ticker facade (lazy loading, caching) — no parsing
├── profile.py         # Profile dataclass
├── search.py          # search_by_industry / search_by_theme / list_industries
├── config.py          # User settings: timeout, request_delay, user_agent
├── exceptions.py      # PykabutanError, TickerNotFoundError, ScrapingError
└── _internal/
    ├── http.py        # Fetch only: request_as_human, rate limiting, get_soup/get_dfs
    ├── site.py        # ALL kabutan constants: URL patterns, table indices,
    │                  #   CSS selectors, interval/nmode maps, INDUSTRY_MAP, MARKET_MAP
    └── parsers/       # Parse only: soup/html → structured data (no I/O)
        ├── main_page.py   # profile fields, similar-stock codes
        ├── history.py     # OHLC table
        ├── news.py
        ├── finance.py     # named statements: results, forecasts, quarterly, cashflow
        ├── holders.py
        └── themes.py      # search-result rows
```

Rules encoded by this tree:
- **Fetch vs parse separation**: `http.py` does I/O and returns raw content; `parsers/` are pure functions soup→data. Never mix.
- **Single site-coupling point**: when kabutan.jp changes markup, `_internal/site.py` is the only file with constants to update.
- **Public surface = top level**: users only ever touch `ticker/profile/search/config/exceptions`.

## Design Decisions (updated in audit — these override older notes)

- **Error handling**: structural parse failures (expected table/selector missing → site changed) **raise `ScrapingError`**. Genuinely optional fields (ETF has no PER, `－倍` for loss-makers) return `None`. Invalid ticker → `TickerNotFoundError` via HTTP status-code check (not string matching). This is a breaking change → 0.2.0.
- **`financials()`**: returns dict of named DataFrames keyed `annual`, `interim`, `quarterly`, `cashflow`, `profitability`, `financial_position`, `records` — tables identified by column signature (ＲＯＥ → profitability, フリーCF → cashflow, etc.), paywalled tables excluded. Values in 百万円 as published.
- **`history()`**: period is calendar time (date-bound pagination stop, not row counting); returns ascending `DatetimeIndex` with numeric columns (yfinance convention).
- **HTTP**: single `_internal/http.py:fetch()` — pooled `requests.Session`, urllib3 `Retry` on 429/5xx, fixed UTF-8 encoding, thread-safe rate limiter (lock held while sleeping).
- **`market_cap`**: converted to yen (×1e8 from parsed 億円 value) to match documented contract.
- **Version**: single-sourced from `pyproject.toml` via `importlib.metadata` — never hardcode `__version__`.
- **API docs**: mkdocstrings-python auto-generation from docstrings. No hand-copied API pages.
- **Test fixtures**: captured real kabutan.jp HTML snapshots (stored under `tests/fixtures/`), not hand-fabricated minimal HTML.
- **Caching**: in-memory per session; profile/main-page soup cached, method calls not cached. Unchanged.
- **Rate limiting**: default 0.5s delay, configurable. Unchanged.
- **No Selenium** — lightweight requests+bs4+pandas only. Unchanged.

## Kept vs Discarded (audit outcome)

Kept: entire public API surface, flat public modules, lazy-loading design, config system, integration-test approach.
Discarded/replaced: `_scraper.py` (split into `_internal/http.py` + `site.py` + `parsers/`), silent `except Exception` swallowing, dead `ashi == "shin"` branch, vestigial `ticker._search_name`, duplicated config defaults in `_scraper.py`, hand-written API doc pages, `dist/`+`site/` local clutter (gitignored, never tracked).

## Key Files

- `src/pykabutan/ticker.py` — Ticker facade; entry point for all per-stock data
- `src/pykabutan/_internal/site.py` — every kabutan-specific constant (update here on site drift)
- `src/pykabutan/_internal/parsers/` — pure soup/html→data functions, one module per kabutan page
- `tests/fixtures/*.html` — verbatim kabutan.jp captures (2026-07-02); unit tests parse these, not fabricated HTML
- `tasks/` — task tracking (done/ holds completed tasks TASK-001..015; refactor tasks continue from TASK-016)
- `PYKABU_CODEBASE_ANALYSIS.md` — historical analysis of the predecessor `pykabu` codebase (reference only)

## Kabutan URL Reference

| Page | URL Pattern | Notes |
|------|-------------|-------|
| Main | `/stock/?code={code}` | stats `#stockinfo_i3 table`; profile `div.company_block table`; similar `dl.si_i1_dl2 a` |
| OHLC | `/stock/kabuka?code={code}&ashi={interval}&page={page}` | `table.stock_kabuka_dwm` (all intervals); ashi: day/wek/mon/yar |
| News | `/stock/news?code={code}&nmode={mode}` | `table.s_news_list`; nmode: 0=all,1=material,2=earnings,3=disclosure |
| Finance | `/stock/finance?code={code}` | `div#finance_box`, ~20 tables identified by column signature; partially paywalled |
| Holders | `/stock/holder?code={code}&tab={tab}` | `table.stock_holder_1`, MultiIndex header; date menu `div.stock_holder_title.date_menu a` |
| Industry | `/themes/?industry={code}&market={market}` | `table.stock_table` |
| Theme | `/themes/?theme={encoded}&market={market}` | `table.stock_table` |

Nonexistent ticker → HTTP 404. Ticker codes may be alphanumeric (e.g. `135A`, `285A`).

Canonical machine-readable versions of these constants live in `_internal/site.py`.
