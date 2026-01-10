# Search Functions

## search_by_industry

```python
def search_by_industry(
    industry: str,
    market: str = "all"
) -> list[Ticker]
```

Search for stocks by industry classification.

**Parameters:**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `industry` | `str` | required | Industry name (Japanese) |
| `market` | `str` | `"all"` | Market filter |

**Returns:** List of `Ticker` objects

**Raises:** `ValueError` if industry is not valid

**Example:**

```python
import pykabutan as pk

# Search electronics industry
results = pk.search_by_industry("電気機器")

# Filter by market
results = pk.search_by_industry("電気機器", market="Prime")

# Access data
for t in results[:5]:
    print(t.code, t.profile.name)
```

---

## search_by_theme

```python
def search_by_theme(
    theme: str,
    market: str = "all"
) -> list[Ticker]
```

Search for stocks by theme or keyword.

**Parameters:**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `theme` | `str` | required | Theme keyword (Japanese recommended) |
| `market` | `str` | `"all"` | Market filter |

**Returns:** List of `Ticker` objects

**Example:**

```python
import pykabutan as pk

# Search by theme (use Japanese for best results)
results = pk.search_by_theme("人工知能")
results = pk.search_by_theme("半導体")
results = pk.search_by_theme("EV")

# Access data
for t in results[:5]:
    print(t.code, t.profile.name)
```

---

## list_industries

```python
def list_industries() -> list[str]
```

Get list of all available industry names.

**Returns:** List of 33 industry names (Japanese)

**Example:**

```python
import pykabutan as pk

industries = pk.list_industries()
for industry in industries:
    print(industry)
```

---

## Working with Search Results

Search functions return `Ticker` objects:

```python
results = pk.search_by_industry("電気機器")

for t in results[:5]:
    print(t.code)           # Stock code (no HTTP request)
    print(t.profile.name)   # Company name (HTTP request)
    print(t.profile.market) # Market (cached after first access)
```

| Access | HTTP Request? | Description |
|--------|---------------|-------------|
| `t.code` | No | Stock code available immediately |
| `t.profile.*` | Yes (first access) | Profile data fetched on demand |

---

## Market Values

Valid market filter values:

| Value | Aliases | Description |
|-------|---------|-------------|
| `"all"` | `"0"` | All markets |
| `"Prime"` | `"東証Ｐ"`, `"1"` | TSE Prime |
| `"Standard"` | `"東証Ｓ"`, `"2"` | TSE Standard |
| `"Growth"` | `"東証Ｇ"`, `"3"` | TSE Growth |

---

## Industries

All 33 industry classifications:

| Industry | Industry |
|----------|----------|
| 水産・農林業 | 鉱業 |
| 建設業 | 食料品 |
| 繊維製品 | パルプ・紙 |
| 化学 | 医薬品 |
| 石油・石炭製品 | ゴム製品 |
| ガラス・土石製品 | 鉄鋼 |
| 非鉄金属 | 金属製品 |
| 機械 | 電気機器 |
| 輸送用機器 | 精密機器 |
| その他製品 | 電気・ガス業 |
| 陸運業 | 海運業 |
| 空運業 | 倉庫・運輸関連業 |
| 情報・通信業 | 卸売業 |
| 小売業 | 銀行業 |
| 証券、商品先物取引業 | 保険業 |
| その他金融業 | 不動産業 |
| サービス業 | |
