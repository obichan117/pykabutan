# TASK-010: Ticker.holders() Method

**Status**: todo
**Priority**: medium

## Description
Implement the holders() method for shareholder information.

## Acceptance Criteria
- [ ] Implement `holders(period)` method
- [ ] Return DataFrame with shareholder info
- [ ] Support historical periods (tab parameter)
- [ ] Handle missing data

## API
```python
df = ticker.holders()           # Latest
df = ticker.holders(period=0)   # Latest
df = ticker.holders(period=1)   # Previous period (6 months ago)
```

## DataFrame Columns
```
date, shareholder_name, shares, ratio(%)
```

## Reference
Port from: `KabutanStockScraper.get_holders_df()`

URL: `https://kabutan.jp/stock/holder?code={code}&tab={period}`

## Notes
- NOT cached
- Kabutan shows ~4 periods (every 6 months)
- Consider adding `all_holders()` to get all periods
