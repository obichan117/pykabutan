"""Ticker class for accessing stock data from kabutan.jp."""

import re

import pandas as pd
from bs4 import BeautifulSoup

from pykabutan._scraper import get_df_from_soup, get_dfs, get_soup
from pykabutan.exceptions import ScrapingError, TickerNotFoundError
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

    _BASE_URL = "https://kabutan.jp/stock"

    def __init__(self, code: str):
        """Initialize ticker with stock code.

        Args:
            code: Stock code (e.g., "7203" for Toyota)

        Note:
            No HTTP request is made until data is accessed (lazy loading).
        """
        self.code = str(code)
        self._profile_cache: Profile | None = None
        self._soup_cache: BeautifulSoup | None = None

    def __repr__(self) -> str:
        return f"Ticker('{self.code}')"

    # === URLs ===

    @property
    def _url_main(self) -> str:
        return f"{self._BASE_URL}/?code={self.code}"

    def _url_history(self, ashi: str, page: int) -> str:
        return f"{self._BASE_URL}/kabuka?code={self.code}&ashi={ashi}&page={page}"

    def _url_news(self, nmode: int) -> str:
        return f"{self._BASE_URL}/news?code={self.code}&nmode={nmode}"

    @property
    def _url_finance(self) -> str:
        return f"{self._BASE_URL}/finance?code={self.code}"

    def _url_holder(self, tab: int) -> str:
        return f"{self._BASE_URL}/holder?code={self.code}&tab={tab}"

    # === Cached soup ===

    @property
    def _soup(self) -> BeautifulSoup:
        """Get cached soup for main page."""
        if self._soup_cache is None:
            try:
                self._soup_cache = get_soup(self._url_main)
            except Exception as e:
                # Check if it's a 404 error
                if "404" in str(e):
                    raise TickerNotFoundError(self.code)
                raise
            self._validate_ticker()
        return self._soup_cache

    def _validate_ticker(self):
        """Check if ticker exists on kabutan."""
        # If ticker doesn't exist, kabutan shows error message
        if self._soup_cache is None:
            return
        error_div = self._soup_cache.find("div", class_="error")
        if error_div:
            raise TickerNotFoundError(self.code)
        # Also check if h2 exists (company name header)
        if not self._soup_cache.find("h2"):
            raise TickerNotFoundError(self.code)

    # === Profile (cached) ===

    @property
    def profile(self) -> Profile:
        """Stock profile information (lazy loaded, cached).

        Returns:
            Profile object with name, market, industry, stats, etc.
        """
        if self._profile_cache is None:
            self._profile_cache = self._fetch_profile()
        return self._profile_cache

    def _fetch_profile(self) -> Profile:
        """Fetch and parse profile from main page."""
        soup = self._soup

        # Parse basic info
        name = self._parse_name(soup)
        market = self._parse_market(soup)
        industry = self._parse_industry(soup)

        # Parse profile table (description, themes, etc.)
        profile_dict = self._parse_profile_table(soup)
        description = profile_dict.get("概要")
        themes = profile_dict.get("テーマ", "").split() if profile_dict.get("テーマ") else None
        website = profile_dict.get("会社サイト")
        english_name = profile_dict.get("英語社名")

        # Parse stats table (PER, PBR, etc.)
        stats = self._parse_stats(soup)

        return Profile(
            code=self.code,
            name=name,
            market=market,
            industry=industry,
            description=description,
            themes=themes,
            website=website,
            english_name=english_name,
            per=stats.get("per"),
            pbr=stats.get("pbr"),
            market_cap=stats.get("market_cap"),
            dividend_yield=stats.get("dividend_yield"),
            margin_ratio=stats.get("margin_ratio"),
        )

    def _parse_name(self, soup: BeautifulSoup) -> str | None:
        """Parse company name from h2 tag."""
        try:
            h2 = soup.find("h2")
            if h2:
                return h2.text.split()[-1]
        except Exception:
            pass
        return None

    def _parse_market(self, soup: BeautifulSoup) -> str | None:
        """Parse market name (東証P, etc.)."""
        try:
            span = soup.find("span", class_="market")
            if span:
                return span.text
        except Exception:
            pass
        return None

    def _parse_industry(self, soup: BeautifulSoup) -> str | None:
        """Parse industry name."""
        try:
            div = soup.find("div", id="stockinfo_i2")
            if div:
                a = div.find("a")
                if a:
                    return a.text
        except Exception:
            pass
        return None

    def _parse_profile_table(self, soup: BeautifulSoup) -> dict:
        """Parse profile table (概要, テーマ, etc.)."""
        try:
            df = get_df_from_soup(soup, search_word="概要", index_col=0)
            return df.T.dropna(axis=1).to_dict(orient="records")[0]
        except Exception:
            return {}

    def _parse_stats(self, soup: BeautifulSoup) -> dict:
        """Parse stats table (PER, PBR, market cap, etc.)."""
        try:
            df = get_df_from_soup(soup, search_word="PBR")
            df = self._remove_japanese_chars(df)
            cols = ["per", "pbr", "dividend_yield", "margin_ratio"]
            df.columns = cols
            data = df.iloc[0, :].to_dict()

            # Market cap is in the last row, last column
            data["market_cap"] = df.iloc[-1, -1] if len(df) > 1 else None

            # Convert to float
            return {k: self._to_float(v) for k, v in data.items()}
        except Exception:
            return {}

    @staticmethod
    def _remove_japanese_chars(df: pd.DataFrame) -> pd.DataFrame:
        """Remove Japanese characters from DataFrame cells."""
        pattern = r"[^a-zA-Z0-9.]"

        def clean(cell):
            if isinstance(cell, str):
                return re.sub(pattern, "", cell)
            return cell

        return df.map(clean)

    @staticmethod
    def _to_float(value) -> float | None:
        """Convert value to float, return None if fails."""
        if value is None or value == "":
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    # === Methods (not cached) ===

    def refresh(self) -> None:
        """Clear cached data to force fresh fetch on next access."""
        self._profile_cache = None
        self._soup_cache = None

    def history(
        self,
        period: str | None = "30d",
        interval: str = "day",
        start: str | None = None,
        end: str | None = None,
    ) -> pd.DataFrame:
        """Get price history (OHLC data).

        Args:
            period: Time period (e.g., "30d", "1y"). Ignored if start/end provided.
            interval: Data interval - "day", "week", "month", "year"
                     (or "1d", "1w", "1mo", "1y")
            start: Start date (YYYY-MM-DD format)
            end: End date (YYYY-MM-DD format)

        Returns:
            DataFrame with columns: date, open, high, low, close, volume,
                                   change, percent_change
        """
        # Map interval aliases
        interval_map = {
            "day": "day",
            "1d": "day",
            "week": "wek",
            "1w": "wek",
            "month": "mon",
            "1mo": "mon",
            "year": "yar",
            "1y": "yar",
        }
        ashi = interval_map.get(interval, "day")

        # Parse period to determine number of rows to fetch
        if start and end:
            # Date range mode - fetch more and filter
            max_rows = 3650  # ~10 years
        else:
            max_rows = self._parse_period(period)

        return self._fetch_history(ashi, max_rows, start, end)

    def _parse_period(self, period: str | None) -> int:
        """Parse period string to number of days/rows."""
        if not period:
            return 30

        period = period.lower()
        if period.endswith("d"):
            return int(period[:-1])
        elif period.endswith("w"):
            return int(period[:-1]) * 7
        elif period.endswith("mo"):
            return int(period[:-2]) * 30
        elif period.endswith("m"):
            return int(period[:-1]) * 30
        elif period.endswith("y"):
            return int(period[:-1]) * 365
        else:
            return int(period)

    def _fetch_history(
        self,
        ashi: str,
        max_rows: int,
        start: str | None = None,
        end: str | None = None,
    ) -> pd.DataFrame:
        """Fetch price history with pagination."""
        page = 1
        dfs = []
        total_rows = 0
        max_pages = 50  # Safety limit

        while total_rows < max_rows and page <= max_pages:
            url = self._url_history(ashi, page)
            try:
                tables = get_dfs(url)
                # Price table is usually at index 5
                if len(tables) > 5:
                    df = tables[5]
                    if df.empty:
                        break
                    dfs.append(df)
                    total_rows += len(df)
                    page += 1
                else:
                    break
            except Exception:
                break

        if not dfs:
            return pd.DataFrame()

        result = pd.concat(dfs, ignore_index=True)

        # Set column names based on interval type
        if ashi == "shin":  # Margin trading data
            cols = ["date", "close", "percent_change", "vwap", "volume", "short", "long", "margin_ratio"]
        else:
            cols = ["date", "open", "high", "low", "close", "change", "percent_change", "volume"]

        if len(result.columns) >= len(cols):
            result.columns = cols[: len(result.columns)]

        # Parse date column (format: YY/MM/DD)
        if "date" in result.columns:
            result["date"] = pd.to_datetime(result["date"], format="%y/%m/%d", errors="coerce")

        # Filter by date range if specified
        if start and "date" in result.columns:
            result = result[result["date"] >= pd.to_datetime(start)]
        if end and "date" in result.columns:
            result = result[result["date"] <= pd.to_datetime(end)]

        return result.head(max_rows)

    def news(self, mode: str = "earnings") -> pd.DataFrame:
        """Get stock news.

        Args:
            mode: News type - "all", "material", "earnings", "disclosure"

        Returns:
            DataFrame with columns: datetime, news_type, title
        """
        mode_map = {"all": 0, "material": 1, "earnings": 2, "disclosure": 3}
        nmode = mode_map.get(mode, 2)

        try:
            tables = get_dfs(self._url_news(nmode))
            if len(tables) > 3:
                df = tables[3]
                if df.shape[1] >= 3:
                    df.columns = ["datetime", "news_type", "title"][: df.shape[1]]
                    if "datetime" in df.columns:
                        df["datetime"] = pd.to_datetime(df["datetime"], format="%y/%m/%d %H:%M", errors="coerce")
                    return df
        except Exception:
            pass

        return pd.DataFrame(columns=["datetime", "news_type", "title"])

    def financials(self) -> dict[str, pd.DataFrame]:
        """Get financial statements.

        Returns:
            Dictionary of DataFrames with various financial tables.
        """
        try:
            dfs = get_dfs(self._url_finance)
            return {"tables": dfs}
        except Exception:
            return {}

    def holders(self, period: int = 0) -> pd.DataFrame:
        """Get shareholder information.

        Args:
            period: Historical period (0=latest, 1=previous, etc.)

        Returns:
            DataFrame with shareholder information.
        """
        try:
            soup = get_soup(self._url_holder(period))
            df = get_df_from_soup(soup, search_word="株主名")
            df.columns = df.columns.droplevel(0)

            # Get date from page
            links = soup.find("div", class_="stock_holder_title date_menu")
            if links:
                link_tags = links.find_all("a")
                if len(link_tags) > period:
                    date = link_tags[period].text
                    df.insert(0, "date", date)

            return df
        except Exception:
            return pd.DataFrame()

    def similar_stocks(self) -> list["Ticker"]:
        """Get similar stocks.

        Returns:
            List of Ticker objects for similar companies.
        """
        try:
            soup = self._soup
            dl = soup.find("dl", class_="si_i1_dl2")
            if dl:
                tags = dl.find_all("a")
                codes = []
                for tag in tags:
                    href = tag.get("href", "")
                    if href:
                        # Extract code from URL
                        code = href[-4:] if len(href) >= 4 else None
                        if code and code.isdigit():
                            codes.append(code)
                return [Ticker(code) for code in codes]
        except Exception:
            pass
        return []
