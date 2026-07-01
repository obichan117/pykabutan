# TASK-020: _internal/parsers/ + ScrapingError policy

Pure soup/html->data modules per page (main_page, history, news, finance,
holders, themes, _convert). Structural failures raise ScrapingError(what);
optional fields return None. Fragment-level pd.read_html (no full-page
re-serialization). Fixed: similar_stocks alphanumeric codes, market_cap in yen,
unicode-minus handling.

Status: done (2026-07-02)
