# TASK-006: Ticker Class (Core)

**Status**: todo
**Priority**: high

## Description
Create the main Ticker class with lazy loading and cached profile.

## Acceptance Criteria
- [ ] Create `ticker.py` with Ticker class
- [ ] Implement lazy loading (no HTTP on init)
- [ ] Implement `profile` property with caching
- [ ] Detect invalid ticker codes and raise `TickerNotFoundError`
- [ ] Add `code` property (always available)
- [ ] Add `refresh()` method to clear cache

## Implementation
```python
class Ticker:
    def __init__(self, code: str):
        self.code = str(code)
        self._profile_cache: Profile | None = None

    @property
    def profile(self) -> Profile:
        if self._profile_cache is None:
            self._profile_cache = self._fetch_profile()
        return self._profile_cache

    def _fetch_profile(self) -> Profile:
        # HTTP request to main page
        # Parse and return Profile
        ...

    def refresh(self) -> None:
        """Clear all cached data"""
        self._profile_cache = None
```

## Reference
Port from original:
- `KabutanStockScraper` for scraping logic
- `KabutanStock` for wrapper pattern

## Notes
- Profile is cached (same page, single HTTP request)
- Methods like history(), news() are NOT cached (separate task)
