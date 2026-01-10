# TASK-005: Profile Dataclass

**Status**: todo
**Priority**: high

## Description
Create the Profile class that holds all main page data for a ticker.

## Acceptance Criteria
- [ ] Create `profile.py` with Profile class
- [ ] Include all fields from kabutan main page
- [ ] Implement `__iter__` for dict conversion: `dict(profile)`
- [ ] Return `None` for missing fields (ETFs, etc.)
- [ ] Add type hints

## Fields
```python
@dataclass
class Profile:
    code: str
    name: str | None
    market: str | None           # 東証P, 東証S, 東証G, etc.
    industry: str | None         # 輸送用機器, etc.
    description: str | None
    themes: list[str] | None
    website: str | None
    english_name: str | None
    per: float | None
    pbr: float | None
    market_cap: float | None     # in yen
    dividend_yield: float | None
    margin_ratio: float | None

    def __iter__(self):
        """Enable dict(profile) conversion"""
        ...
```

## Reference
Port from original pykabu codebase `public_modules/kabutan.py`:
- `get_basic_info()` → name, market, industry, description, themes, website, english_name
- `get_basic_stats()` → per, pbr, market_cap, dividend_yield, margin_ratio

## Notes
- Use `@dataclass` for clean implementation
- All fields optional (None) for incomplete data
