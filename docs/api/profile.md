# Profile

::: pykabutan.profile.Profile

## Class Definition

```python
@dataclass
class Profile:
    """Company profile data from kabutan.jp main page."""
```

## Fields

| Field | Type | Description |
|-------|------|-------------|
| `code` | `str` | Stock code |
| `name` | `str \| None` | Company name (Japanese) |
| `market` | `str \| None` | Market (e.g., "東証Ｐ") |
| `industry` | `str \| None` | Industry classification |
| `description` | `str \| None` | Company description |
| `themes` | `list[str] \| None` | Related themes |
| `website` | `str \| None` | Company website URL |
| `english_name` | `str \| None` | English company name |
| `per` | `float \| None` | Price-to-earnings ratio |
| `pbr` | `float \| None` | Price-to-book ratio |
| `market_cap` | `float \| None` | Market capitalization |
| `dividend_yield` | `float \| None` | Dividend yield (%) |
| `margin_ratio` | `float \| None` | Profit margin (%) |

## Usage

Access profile through a Ticker:

```python
import pykabutan as pk

ticker = pk.Ticker("7203")
profile = ticker.profile

print(profile.name)      # トヨタ自動車
print(profile.market)    # 東証Ｐ
print(profile.industry)  # 輸送用機器
print(profile.per)       # 10.5
print(profile.pbr)       # 1.2
```

## Methods

### `to_dict()`

```python
def to_dict(self) -> dict
```

Convert profile to dictionary.

**Returns:** `dict` with all profile fields

**Example:**

```python
data = profile.to_dict()
print(data["name"])  # トヨタ自動車
```

### `__iter__()`

Profile supports iteration for dict conversion:

```python
# Convert to dict using dict()
data = dict(profile)

# Iterate over fields
for name, value in profile:
    print(f"{name}: {value}")
```

## Missing Data

Fields that are not available on kabutan.jp return `None`:

```python
# ETFs may have missing fields
ticker = pk.Ticker("1306")  # TOPIX ETF
profile = ticker.profile

print(profile.description)  # None (no description for ETF)
print(profile.per)          # None (N/A for ETF)
```
