# TASK-007: Ticker.history() Method

**Status**: todo
**Priority**: high

## Description
Implement the history() method for price data (yfinance style).

## Acceptance Criteria
- [ ] Implement `history(period, interval, start, end)` method
- [ ] Support period strings: "30d", "1y", etc.
- [ ] Support interval: "day", "week", "month", "year" (and aliases)
- [ ] Support date range: start/end parameters
- [ ] Return pandas DataFrame with OHLC columns
- [ ] Handle pagination for long date ranges

## API
```python
# Period-based
ticker.history(period="30d")                    # Last 30 days, daily
ticker.history(period="1y", interval="week")   # Last year, weekly

# Date range
ticker.history(start="2024-01-01", end="2024-12-31")
```

## DataFrame Columns
```
date, open, high, low, close, volume, change, percent_change
```

## Interval Mapping
| pykabutan | kabutan ashi |
|-----------|--------------|
| day, 1d   | day          |
| week, 1w  | wek          |
| month, 1mo| mon          |
| year, 1y  | yar          |

## Reference
Port from: `KabutanStockScraper.get_ohlc_df()`

## Notes
- NOT cached (always fresh data)
- Handle pagination internally (kabutan pages results)
- Parse Japanese date format
