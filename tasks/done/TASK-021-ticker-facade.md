# TASK-021: Thin Ticker facade + search rewrite

Ticker keeps lazy-loading/caching/URL wiring only. Calendar-date pagination
stop for history() (ascending DatetimeIndex, numeric dtypes). 404 via
HTTPError.response.status_code. ValueError on unknown interval/mode/market.
__version__ single-sourced via importlib.metadata. ConfigurationError removed.

Status: done (2026-07-02)
