# TASK-011: Ticker.similar_stocks() Method

**Status**: todo
**Priority**: low

## Description
Implement the similar_stocks() method to get related stocks.

## Acceptance Criteria
- [ ] Implement `similar_stocks()` method
- [ ] Return list of Ticker objects
- [ ] Ticker objects should have basic info cached from page

## API
```python
similar = ticker.similar_stocks()
# Returns: [Ticker("7203"), Ticker("7267"), ...]

for t in similar:
    print(t.code, t.profile.name)
```

## Reference
Port from: `KabutanStockScraper.get_similar_stocks()`

Data comes from main page sidebar.

## Notes
- Returns Ticker objects (not just codes)
- Basic info might be available without extra HTTP request
