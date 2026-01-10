# TASK-009: Ticker.financials() Method

**Status**: todo
**Priority**: medium

## Description
Implement the financials() method for financial statements.

## Acceptance Criteria
- [ ] Implement `financials()` method
- [ ] Return dict of DataFrames (multiple tables on page)
- [ ] Parse all financial tables from kabutan finance page
- [ ] Handle missing data gracefully

## API
```python
data = ticker.financials()
# Returns dict like:
# {
#     "yearly_pl": DataFrame,
#     "quarterly_pl": DataFrame,
#     "balance_sheet": DataFrame,
#     "cash_flow": DataFrame,
#     ...
# }
```

## Reference
Port from: `KabutanStockScraper.get_financials()`

URL: `https://kabutan.jp/stock/finance?code={code}`

## Notes
- NOT cached
- Finance page has many tables - decide which to include
- Consider returning raw dict of all DataFrames for flexibility
