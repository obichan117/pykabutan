# TASK-012: Search Functions

**Status**: todo
**Priority**: high

## Description
Implement top-level search functions for finding stocks by industry or theme.

## Acceptance Criteria
- [ ] Create `search.py` module
- [ ] Implement `search_by_industry(name, market)` function
- [ ] Implement `search_by_theme(name, market)` function
- [ ] Return list of Ticker objects with cached basic info
- [ ] Support market filter (all, Prime, Standard, Growth)

## API
```python
import pykabutan as pk

# Search by industry
tickers = pk.search_by_industry("電気機器")
tickers = pk.search_by_industry("電気機器", market="Prime")

# Search by theme
tickers = pk.search_by_theme("AI")
tickers = pk.search_by_theme("半導体", market="Growth")

# Results have cached basic info
for t in tickers:
    print(t.code, t.name)        # From search results (no HTTP)
    print(t.profile.description)  # HTTP request for details
```

## Industry Mapping
Use INDUSTRY_MAP from original code (33 industries).

## Market Mapping
| pykabutan | kabutan |
|-----------|---------|
| all       | 0       |
| Prime     | 1       |
| Standard  | 2       |
| Growth    | 3       |

## Reference
Port from: `KabutanMarketScraper`

URLs:
- Industry: `https://kabutan.jp/themes/?industry={code}&market={market}`
- Theme: `https://kabutan.jp/themes/?theme={encoded_name}`

## Notes
- Search results contain basic info (code, name, price, etc.)
- Cache this info in returned Ticker objects
- Full profile requires separate HTTP request
