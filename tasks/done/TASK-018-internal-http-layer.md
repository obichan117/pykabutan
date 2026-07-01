# TASK-018: _internal/http.py fetch layer

Single fetch(url)->str entry point: pooled requests.Session, urllib3 Retry
(3x, backoff, 429/5xx), fixed UTF-8 encoding, thread-safe rate limiter
(lock held while sleeping). Config defaults single-sourced; _scraper.py deleted.

Status: done (2026-07-02)
