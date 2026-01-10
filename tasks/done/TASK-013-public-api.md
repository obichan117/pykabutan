# TASK-013: Public API (\_\_init\_\_.py)

**Status**: todo
**Priority**: high

## Description
Set up the public API exports in `__init__.py`.

## Acceptance Criteria
- [ ] Export `Ticker` class
- [ ] Export `search_by_industry` function
- [ ] Export `search_by_theme` function
- [ ] Export `config` object
- [ ] Export exceptions
- [ ] Add `__version__`
- [ ] Add `__all__` for explicit exports

## Public API
```python
# __init__.py
from pykabutan.ticker import Ticker
from pykabutan.search import search_by_industry, search_by_theme
from pykabutan.config import config
from pykabutan.exceptions import (
    PykabutanError,
    TickerNotFoundError,
    ScrapingError,
    ConfigurationError,
)

__version__ = "0.1.0"

__all__ = [
    "Ticker",
    "search_by_industry",
    "search_by_theme",
    "config",
    "PykabutanError",
    "TickerNotFoundError",
    "ScrapingError",
    "ConfigurationError",
]
```

## Usage
```python
import pykabutan as pk

ticker = pk.Ticker("7203")
results = pk.search_by_industry("電気機器")
pk.config.timeout = 60
```

## Notes
- Only export what users need
- Keep internal modules private (`_scraper.py`)
