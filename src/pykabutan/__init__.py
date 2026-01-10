"""
pykabutan - A clean, beginner-friendly Python library for scraping kabutan.jp

Usage:
    import pykabutan as pk

    ticker = pk.Ticker("7203")
    print(ticker.profile.name)      # トヨタ自動車
    print(ticker.profile.per)       # 10.5

    df = ticker.history(period="30d")
    print(df)

    results = pk.search_by_industry("電気機器")
    for t in results:
        print(t.code, t.profile.name)
"""

__version__ = "0.1.0"

from pykabutan.config import config
from pykabutan.exceptions import (
    ConfigurationError,
    PykabutanError,
    ScrapingError,
    TickerNotFoundError,
)
from pykabutan.search import list_industries, search_by_industry, search_by_theme
from pykabutan.ticker import Ticker

__all__ = [
    "__version__",
    "Ticker",
    "search_by_industry",
    "search_by_theme",
    "list_industries",
    "config",
    "PykabutanError",
    "TickerNotFoundError",
    "ScrapingError",
    "ConfigurationError",
]
