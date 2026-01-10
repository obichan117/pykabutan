# Exceptions

## Exception Hierarchy

```
Exception
└── PykabutanError
    ├── TickerNotFoundError
    ├── ScrapingError
    └── ConfigurationError
```

All pykabutan exceptions inherit from `PykabutanError`, allowing you to catch all library exceptions with a single handler.

---

## PykabutanError

```python
class PykabutanError(Exception):
    """Base exception for all pykabutan errors."""
```

Base class for all pykabutan exceptions.

**Example:**

```python
from pykabutan import PykabutanError

try:
    # Any pykabutan operation
    ticker = pk.Ticker("7203")
    profile = ticker.profile
except PykabutanError as e:
    print(f"pykabutan error: {e}")
```

---

## TickerNotFoundError

```python
class TickerNotFoundError(PykabutanError):
    """Raised when a stock code doesn't exist on kabutan.jp."""

    code: str  # The invalid stock code
```

Raised when attempting to access a non-existent stock code.

**Attributes:**

| Name | Type | Description |
|------|------|-------------|
| `code` | `str` | The stock code that was not found |

**Example:**

```python
from pykabutan import TickerNotFoundError

try:
    ticker = pk.Ticker("9999999")
    profile = ticker.profile
except TickerNotFoundError as e:
    print(f"Stock code not found: {e.code}")
```

---

## ScrapingError

```python
class ScrapingError(PykabutanError):
    """Raised when scraping fails."""

    url: str  # The URL that failed
```

Raised when HTTP requests fail or HTML parsing encounters unexpected structure.

**Attributes:**

| Name | Type | Description |
|------|------|-------------|
| `url` | `str` | The URL that caused the error |

**Example:**

```python
from pykabutan import ScrapingError

try:
    results = pk.search_by_industry("電気機器")
except ScrapingError as e:
    print(f"Failed to scrape: {e.url}")
```

---

## ConfigurationError

```python
class ConfigurationError(PykabutanError):
    """Raised when configuration is invalid."""
```

Raised when invalid configuration values are provided.

**Example:**

```python
from pykabutan import ConfigurationError

try:
    pk.config.timeout = -1
except ValueError:
    # Note: Config validation raises ValueError, not ConfigurationError
    print("Invalid timeout value")
```

---

## Catching All Exceptions

```python
import pykabutan as pk
from pykabutan import (
    PykabutanError,
    TickerNotFoundError,
    ScrapingError,
)

try:
    ticker = pk.Ticker("7203")
    profile = ticker.profile
except TickerNotFoundError as e:
    # Handle missing stock specifically
    print(f"Stock {e.code} not found")
except ScrapingError as e:
    # Handle scraping failures specifically
    print(f"Scraping failed for {e.url}")
except PykabutanError as e:
    # Catch any other pykabutan errors
    print(f"Unexpected error: {e}")
```

---

## Import

```python
from pykabutan import (
    PykabutanError,
    TickerNotFoundError,
    ScrapingError,
    ConfigurationError,
)
```

Or import directly:

```python
from pykabutan.exceptions import TickerNotFoundError
```
