# Ticker

::: pykabutan.Ticker

## Class Definition

```python
class Ticker:
    """Represents a stock ticker on kabutan.jp."""
```

## Constructor

### `Ticker(code)`

Create a new Ticker instance.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `code` | `str` or `int` | Stock code (e.g., "7203" or 7203) |

**Example:**

```python
import pykabutan as pk

ticker = pk.Ticker("7203")
ticker = pk.Ticker(7203)  # Also accepts int
```

## Properties

### `code`

```python
@property
def code(self) -> str
```

The stock code as a string.

### `profile`

```python
@property
def profile(self) -> Profile
```

Company profile information. See [Profile](profile.md) for details.

**Returns:** `Profile` object

**Raises:** `TickerNotFoundError` if the stock code doesn't exist

## Methods

### `history()`

```python
def history(
    self,
    period: str = "30d",
    interval: str = "day",
    rows: int | None = None
) -> pd.DataFrame
```

Get historical price data.

**Parameters:**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `period` | `str` | `"30d"` | Time period: "7d", "30d", "90d", etc. |
| `interval` | `str` | `"day"` | Data interval: "day", "week", "month" |
| `rows` | `int` or `None` | `None` | Number of rows to return |

**Returns:** `pandas.DataFrame` with columns:

- `date`: Trading date
- `open`: Opening price
- `high`: High price
- `low`: Low price
- `close`: Closing price
- `volume`: Trading volume
- `change`: Price change

**Example:**

```python
df = ticker.history(period="30d")
df = ticker.history(interval="week")
df = ticker.history(rows=100)
```

---

### `news()`

```python
def news(self, news_type: str = "all") -> pd.DataFrame
```

Get company news.

**Parameters:**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `news_type` | `str` | `"all"` | Type: "all", "earnings", "general", "disclosure" |

**Returns:** `pandas.DataFrame` with news articles

---

### `financials()`

```python
def financials(self) -> pd.DataFrame
```

Get financial statements.

**Returns:** `pandas.DataFrame` with financial data

---

### `holders()`

```python
def holders(self, holder_type: str = "major") -> pd.DataFrame
```

Get shareholder information.

**Parameters:**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `holder_type` | `str` | `"major"` | Type: "major", "float", "treasury" |

**Returns:** `pandas.DataFrame` with shareholder data

---

### `similar_stocks()`

```python
def similar_stocks(self) -> list[SearchResult]
```

Get similar stocks.

**Returns:** List of `SearchResult` named tuples

---

### `refresh()`

```python
def refresh(self) -> None
```

Clear cached data. Next property access will fetch fresh data.

**Example:**

```python
ticker.refresh()
profile = ticker.profile  # Fresh data
```
