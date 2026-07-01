# Changelog

## 0.2.0 (2026-07-02)

Full audit + structural refactor after six months without maintenance. Live
kabutan.jp structure verified page-by-page; all parsing now targets stable
CSS classes captured as real-HTML test fixtures.

### Breaking changes

- **Parsing failures now raise `ScrapingError`** instead of silently returning
  `None` / empty data. If kabutan.jp changes its layout you'll know immediately.
  Genuinely optional fields (ETFs without PER, loss-makers shown as `－倍`)
  still return `None`.
- **`history()` returns an ascending `DatetimeIndex`** (yfinance convention)
  with numeric dtypes, instead of a descending `date` column of strings.
  Enables `df.loc["2026-06"]` slicing.
- **`history(period=...)` now means calendar time.** Previously `"1y"` fetched
  365 *rows* (≈1.5 years of trading days; ≈7 years at `interval="week"`).
- **`Profile.market_cap` is now in yen** as documented (was silently 億円 —
  off by 10⁸).
- **`financials()` is implemented properly**: returns named statements
  (`annual`, `interim`, `quarterly`, `cashflow`, `profitability`,
  `financial_position`, `records`) instead of a raw dump of every page table.
  Values are in 百万円 as published by kabutan.
- **Invalid arguments raise `ValueError`** (`news(mode=...)`, `history(interval=...)`,
  unknown market/industry in search) instead of being silently coerced to defaults.
- **`ConfigurationError` removed** (was never raised).
- `ScrapingError.url` replaced by `ScrapingError.what` (names the element that
  failed to parse).
- `holders()` returns English column names: `date`, `name`, `change`,
  `ratio_percent`, `shares`.

### Fixed

- `similar_stocks()` no longer drops alphanumeric ticker codes (e.g. `277A`).
- 404 detection uses the HTTP status code instead of matching the string
  `"404"` anywhere in the error message.
- `__version__` is single-sourced from package metadata (was hardcoded and
  out of sync with pyproject).
- One transient 5xx during history pagination no longer silently truncates
  results — requests retry (3 attempts, backoff) before failing loudly.

### Improved

- Connection reuse via a pooled `requests.Session` and fixed UTF-8 decoding
  (no per-request TLS handshake or charset detection) — noticeably faster
  multi-page `history()` fetches.
- Thread-safe rate limiter.
- Internals restructured: `_internal/http.py` (fetch), `_internal/site.py`
  (every kabutan-specific constant in one file), `_internal/parsers/` (pure
  parsing) — a kabutan layout change is now a one-file fix.
- Unit tests parse real captured kabutan.jp HTML instead of fabricated markup.
- API reference docs auto-generate from docstrings (mkdocstrings).

## 0.1.1 (2026-01-10)

- Fix API examples to use `t.profile.name` instead of `t.name`.

## 0.1.0 (2026-01-10)

- Initial release.
