# TASK-002: Internal Scraper Module

**Status**: todo
**Priority**: high

## Description
Create the internal `_scraper.py` module that handles HTTP requests and HTML parsing. This is hidden from users.

## Acceptance Criteria
- [ ] Create `_scraper.py` with base scraping utilities
- [ ] Implement `request_as_human()` with proper User-Agent
- [ ] Implement `get_soup()` for BeautifulSoup parsing
- [ ] Implement `get_dfs()` for pandas table extraction
- [ ] Add request timeout handling
- [ ] Add rate limiting (configurable delay between requests)

## Reference
Port from original pykabu codebase `core/scraper.py`.

Only port `BaseScraper` functionality (no Selenium).

## Key Functions
```python
def request_as_human(url: str, timeout: int) -> requests.Response
def get_soup(url: str) -> BeautifulSoup
def get_dfs(url: str) -> list[pd.DataFrame]
def get_df_from_soup(soup: BeautifulSoup, search_word: str) -> pd.DataFrame
```

## Notes
- Use `_` prefix to indicate internal module
- Configurable timeout and delay
- Proper encoding handling (`r.encoding = r.apparent_encoding`)
