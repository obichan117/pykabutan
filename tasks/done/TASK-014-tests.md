# TASK-014: Test Suite

**Status**: todo
**Priority**: high

## Description
Create comprehensive test suite with mocked HTTP responses.

## Acceptance Criteria
- [ ] Set up pytest configuration
- [ ] Create test fixtures with sample HTML responses
- [ ] Test Ticker class initialization
- [ ] Test profile lazy loading and caching
- [ ] Test history() with various parameters
- [ ] Test news(), financials(), holders()
- [ ] Test search functions
- [ ] Test error handling (invalid codes, network errors)
- [ ] Test configuration

## Test Structure
```
tests/
├── __init__.py
├── conftest.py          # Fixtures, mocks
├── fixtures/            # Sample HTML files
│   ├── main_page.html
│   ├── history_page.html
│   └── ...
├── test_ticker.py
├── test_profile.py
├── test_history.py
├── test_search.py
├── test_config.py
└── test_exceptions.py
```

## Key Tests
```python
def test_ticker_lazy_loading():
    """Ticker init should not make HTTP request"""

def test_profile_caching():
    """Second access should use cache, not HTTP"""

def test_invalid_ticker_raises():
    """Invalid code should raise TickerNotFoundError"""

def test_history_period_parsing():
    """'30d', '1y' should parse correctly"""

def test_search_returns_tickers():
    """Search should return list of Ticker objects"""
```

## Notes
- Use pytest-mock or responses library for HTTP mocking
- Save real HTML samples for fixtures
- Test both success and error cases
