# TASK-008: Ticker.news() Method

**Status**: todo
**Priority**: medium

## Description
Implement the news() method for stock news and earnings announcements.

## Acceptance Criteria
- [ ] Implement `news(mode)` method
- [ ] Support mode: "all", "material", "earnings", "disclosure"
- [ ] Return pandas DataFrame
- [ ] Parse datetime properly

## API
```python
ticker.news()                   # Default: earnings
ticker.news(mode="all")         # All news
ticker.news(mode="earnings")    # Earnings announcements
ticker.news(mode="disclosure")  # Disclosure info
```

## DataFrame Columns
```
datetime, news_type, title
```

## Mode Mapping
| pykabutan | kabutan nmode |
|-----------|---------------|
| all       | 0             |
| material  | 1             |
| earnings  | 2             |
| disclosure| 3             |

## Reference
Port from: `KabutanStockScraper.get_news_df()`

## Notes
- NOT cached
- Default mode is "earnings" (most common use case)
