"""Search functions for finding stocks on kabutan.jp."""

import urllib.parse

from pykabutan._internal import http, site
from pykabutan._internal.parsers import themes
from pykabutan.ticker import Ticker


def search_by_industry(industry: str, market: str = "all") -> list[Ticker]:
    """Search for stocks by industry.

    Args:
        industry: Industry name in Japanese (e.g., "電気機器", "輸送用機器").
                  See list_industries() for the full list.
        market: Market filter — "all", "Prime", "Standard", "Growth",
                or Japanese names like "東証Ｐ"

    Returns:
        List of Ticker objects.

    Raises:
        ValueError: For an unknown industry or market.

    Example:
        >>> tickers = search_by_industry("電気機器")
        >>> for t in tickers[:5]:
        ...     print(t.code)
    """
    if industry not in site.INDUSTRY_MAP:
        raise ValueError(f"Unknown industry: {industry!r}. Available: {list(site.INDUSTRY_MAP)}")
    url = site.URL_SEARCH_INDUSTRY.format(
        industry_code=site.INDUSTRY_MAP[industry],
        market_code=_market_code(market),
    )
    return _to_tickers(themes.parse_search_results(http.fetch(url)))


def search_by_theme(theme: str, market: str = "all") -> list[Ticker]:
    """Search for stocks by theme.

    Args:
        theme: Theme name in Japanese (e.g., "人工知能", "半導体").
               Must be in Japanese; English terms like "AI" won't match.
        market: Market filter — "all", "Prime", "Standard", "Growth"

    Returns:
        List of Ticker objects (empty for unknown themes).

    Raises:
        ValueError: For an unknown market.

    Example:
        >>> tickers = search_by_theme("半導体")
        >>> for t in tickers[:5]:
        ...     print(t.code)
    """
    url = site.URL_SEARCH_THEME.format(
        theme=urllib.parse.quote(theme),
        market_code=_market_code(market),
    )
    return _to_tickers(themes.parse_search_results(http.fetch(url)))


def list_industries() -> list[str]:
    """Get list of industry names usable with search_by_industry()."""
    return list(site.INDUSTRY_MAP)


def _market_code(market: str) -> str:
    code = site.MARKET_MAP.get(market)
    if code is None:
        raise ValueError(f"Unknown market: {market!r}. Available: {sorted(set(site.MARKET_MAP))}")
    return code


def _to_tickers(rows: list[dict]) -> list[Ticker]:
    tickers = []
    for row in rows:
        ticker = Ticker(row["code"])
        ticker._search_name = row.get("name")
        tickers.append(ticker)
    return tickers
