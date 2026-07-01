# TASK-017: Capture real kabutan.jp HTML fixtures

15 verbatim page captures under tests/fixtures/ (main x5 incl. ETF/loss-maker/
alphanumeric/404, kabuka day/wek/yar + page2, news x2, finance, holder, themes x2).
load_fixture() helper in conftest. Unit tests parse these instead of fabricated HTML.

Status: done (2026-07-02, delegated: implementer)
