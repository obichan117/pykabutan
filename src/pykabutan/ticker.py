"""Ticker class for accessing stock data from kabutan.jp."""

import pandas as pd
import requests
from bs4 import BeautifulSoup

from pykabutan._internal import http, site
from pykabutan._internal.parsers import finance, history, holders, main_page, make_soup, news
from pykabutan.exceptions import TickerNotFoundError
from pykabutan.profile import Profile


class Ticker:
    """Stock ticker for kabutan.jp data.

    Provides lazy-loaded access to stock information, price history,
    news, financials, and shareholder data.

    Example:
        >>> ticker = Ticker("7203")
        >>> print(ticker.profile.name)  # トヨタ自動車
        >>> df = ticker.history(period="30d")
    """

    def __init__(self, code: str):
        """Initialize ticker with stock code.

        Args:
            code: Stock code (e.g., "7203" for Toyota, "135A" for newer listings)

        Note:
            No HTTP request is made until data is accessed (lazy loading).
        """
        self.code = str(code)
        self._search_name: str | None = None  # company name from search results, if any
        self._profile_cache: Profile | None = None
        self._soup_cache: BeautifulSoup | None = None

    def __repr__(self) -> str:
        return f"Ticker('{self.code}')"

    # === Cached main page ===

    @property
    def _soup(self) -> BeautifulSoup:
        """Fetch and cache the parsed main page."""
        if self._soup_cache is None:
            try:
                html = http.fetch(site.URL_MAIN.format(code=self.code))
            except requests.HTTPError as e:
                if e.response is not None and e.response.status_code == 404:
                    raise TickerNotFoundError(self.code) from e
                raise
            soup = make_soup(html)
            if not main_page.is_stock_page(soup):
                raise TickerNotFoundError(self.code)
            self._soup_cache = soup
        return self._soup_cache

    @property
    def profile(self) -> Profile:
        """Stock profile information (lazy loaded, cached).

        Returns:
            Profile object with name, market, industry, stats, etc.

        Raises:
            TickerNotFoundError: If the code doesn't exist on kabutan.jp.
            ScrapingError: If the page structure changed and can't be parsed.
        """
        if self._profile_cache is None:
            self._profile_cache = main_page.parse_profile(self._soup, self.code)
        return self._profile_cache

    def refresh(self) -> None:
        """Clear cached data to force a fresh fetch on next access."""
        self._profile_cache = None
        self._soup_cache = None

    # === Per-page data (not cached) ===

    def history(
        self,
        period: str | None = "30d",
        interval: str = "day",
        start: str | None = None,
        end: str | None = None,
    ) -> pd.DataFrame:
        """Get price history (OHLC data).

        Args:
            period: Calendar period back from today (e.g. "30d", "6mo", "1y").
                    Ignored if start is provided.
            interval: Data interval — "day", "week", "month", "year"
                      (or "1d", "1w", "1mo", "1y")
            start: Start date (YYYY-MM-DD)
            end: End date (YYYY-MM-DD)

        Returns:
            DataFrame indexed by ascending date with numeric columns:
            open, high, low, close, change, percent_change, volume.

        Raises:
            ValueError: For an unknown interval or unparseable period.
            ScrapingError: If the price table can't be located/parsed.
        """
        ashi = site.INTERVAL_MAP.get(interval)
        if ashi is None:
            raise ValueError(
                f"Unknown interval: {interval!r}. Available: {sorted(set(site.INTERVAL_MAP))}"
            )

        if start is not None:
            start_bound = pd.to_datetime(start)
        else:
            start_bound = pd.Timestamp.today().normalize() - _period_to_timedelta(period)
        end_bound = pd.to_datetime(end) if end is not None else None

        pages: list[pd.DataFrame] = []
        prev_oldest = None
        for page in range(1, site.HISTORY_MAX_PAGES + 1):
            html = http.fetch(site.URL_HISTORY.format(code=self.code, ashi=ashi, page=page))
            df = history.parse_page(html)
            if df.empty:
                break
            oldest = df["date"].min()
            # kabutan re-serves the last page for out-of-range page numbers
            if prev_oldest is not None and oldest >= prev_oldest:
                break
            pages.append(df)
            prev_oldest = oldest
            if oldest < start_bound:
                break

        if not pages:
            empty = pd.DataFrame(columns=site.HISTORY_COLUMNS[1:])
            empty.index = pd.DatetimeIndex([], name="date")
            return empty

        result = pd.concat(pages, ignore_index=True)
        result = result[result["date"] >= start_bound]
        if end_bound is not None:
            result = result[result["date"] <= end_bound]
        return result.sort_values("date").set_index("date")

    def news(self, mode: str = "earnings") -> pd.DataFrame:
        """Get stock news.

        Args:
            mode: News type — "all", "material", "earnings", "disclosure"

        Returns:
            DataFrame with columns: datetime, news_type, title.
            Empty when the stock has no news for the mode.

        Raises:
            ValueError: For an unknown mode.
        """
        nmode = site.NEWS_MODE_MAP.get(mode)
        if nmode is None:
            raise ValueError(
                f"Unknown news mode: {mode!r}. Available: {sorted(site.NEWS_MODE_MAP)}"
            )
        html = http.fetch(site.URL_NEWS.format(code=self.code, nmode=nmode))
        return news.parse_page(html)

    def financials(self) -> dict[str, pd.DataFrame]:
        """Get financial statements from the finance page.

        Returns:
            Dict of DataFrames keyed by statement (present when kabutan
            publishes them): "annual", "interim", "quarterly", "cashflow",
            "profitability", "financial_position", "records".
            Money values are in 百万円 (millions of yen) as published.

        Raises:
            ScrapingError: If no statement tables can be located.
        """
        html = http.fetch(site.URL_FINANCE.format(code=self.code))
        return finance.parse_page(html)

    def holders(self, period: int = 0) -> pd.DataFrame:
        """Get shareholder information.

        Args:
            period: Reporting period (0=latest, 1=previous, ...)

        Returns:
            DataFrame with columns: date, name, change, ratio_percent, shares.

        Raises:
            ScrapingError: If the shareholders table can't be located.
        """
        html = http.fetch(site.URL_HOLDER.format(code=self.code, tab=period))
        return holders.parse_page(html, period)

    def similar_stocks(self) -> list["Ticker"]:
        """Get similar stocks listed on the main page.

        Returns:
            List of Ticker objects (empty if the section is absent).
        """
        return [Ticker(code) for code in main_page.parse_similar_codes(self._soup)]


def _period_to_timedelta(period: str | None) -> pd.Timedelta:
    """Convert a period string ("30d", "2w", "6mo", "1y") to a calendar span."""
    if not period:
        return pd.Timedelta(days=30)
    p = period.lower().strip()
    try:
        if p.endswith("mo"):
            return pd.Timedelta(days=int(p[:-2]) * 30)
        if p.endswith("y"):
            return pd.Timedelta(days=int(p[:-1]) * 365)
        if p.endswith("w"):
            return pd.Timedelta(days=int(p[:-1]) * 7)
        if p.endswith("m"):
            return pd.Timedelta(days=int(p[:-1]) * 30)
        if p.endswith("d"):
            return pd.Timedelta(days=int(p[:-1]))
        return pd.Timedelta(days=int(p))
    except ValueError:
        raise ValueError(
            f"Invalid period: {period!r}. Use forms like '30d', '2w', '6mo', '1y'."
        ) from None
