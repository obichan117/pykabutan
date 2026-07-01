# TASK-023: Test suite rewrite

114 unit tests: parsers tested against real fixtures, facade with mocked
http.fetch (pagination stop, 404/500, caching, ValueError paths), _convert
helpers. Integration tests updated for DatetimeIndex + financials(), config
state-leak fixture added. All 30 pass live.

Status: done (2026-07-02, delegated: implementer)
