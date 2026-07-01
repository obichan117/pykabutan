"""Parsers for the stock main page (/stock/?code=...): profile and similar stocks."""

import re

from bs4 import BeautifulSoup

from pykabutan._internal import site
from pykabutan._internal.parsers._convert import (
    parse_market_cap_yen,
    require,
    table_to_df,
    to_float_jp,
)
from pykabutan.exceptions import ScrapingError
from pykabutan.profile import Profile


def is_stock_page(soup: BeautifulSoup) -> bool:
    """True if the page looks like a real stock page (not an error page)."""
    if soup.select_one(site.SEL_ERROR_DIV) is not None:
        return False
    return soup.select_one(site.SEL_NAME) is not None


def parse_profile(soup: BeautifulSoup, code: str) -> Profile:
    """Parse the main page into a Profile.

    Structural elements (name header, stats table) raise ScrapingError when
    missing; genuinely optional data (ETFs have no PER, description, ...)
    comes back as None.
    """
    h2 = require(soup.select_one(site.SEL_NAME), "company name header")
    name = h2.get_text().split()[-1] if h2.get_text().split() else None

    market_span = soup.select_one(site.SEL_MARKET)
    market = market_span.get_text(strip=True) if market_span else None

    industry_a = soup.select_one(site.SEL_INDUSTRY)
    industry = industry_a.get_text(strip=True) if industry_a else None

    stats = _parse_stats(soup)
    profile_table = _parse_profile_table(soup)

    themes_text = profile_table.get("テーマ")
    return Profile(
        code=code,
        name=name,
        market=market,
        industry=industry,
        description=profile_table.get("概要"),
        themes=themes_text.split() if themes_text else None,
        website=profile_table.get("会社サイト"),
        english_name=profile_table.get("英語社名"),
        per=stats.get("per"),
        pbr=stats.get("pbr"),
        market_cap=stats.get("market_cap"),
        dividend_yield=stats.get("dividend_yield"),
        margin_ratio=stats.get("margin_ratio"),
    )


def parse_similar_codes(soup: BeautifulSoup) -> list[str]:
    """Extract similar-stock ticker codes (optional page section: missing -> [])."""
    codes = []
    for a in soup.select(site.SEL_SIMILAR_LINKS):
        match = re.search(site.CODE_IN_HREF_RE, a.get("href", ""))
        if match:
            codes.append(match.group(1))
    return codes


def _parse_stats(soup: BeautifulSoup) -> dict:
    """Parse the PER/PBR/利回り/信用倍率/時価総額 table."""
    node = require(soup.select_one(site.SEL_STATS_TABLE), "stats table (PER/PBR)")
    df = table_to_df(node, "stats table (PER/PBR)")
    if df.shape[1] < 4:
        raise ScrapingError(
            "stats table (PER/PBR)",
            f"Stats table has unexpected shape {df.shape}; kabutan.jp layout may have changed.",
        )
    row = df.iloc[0]
    stats = {
        "per": to_float_jp(row.iloc[0]),
        "pbr": to_float_jp(row.iloc[1]),
        "dividend_yield": to_float_jp(row.iloc[2]),
        "margin_ratio": to_float_jp(row.iloc[3]),
        "market_cap": None,
    }
    if len(df) > 1:
        stats["market_cap"] = parse_market_cap_yen(str(df.iloc[-1, -1]))
    return stats


def _parse_profile_table(soup: BeautifulSoup) -> dict:
    """Parse the company profile table (概要/テーマ/会社サイト/英語社名).

    Optional: ETFs and some instruments have no company block -> {}.
    """
    node = soup.select_one(site.SEL_PROFILE_TABLE)
    if node is None:
        return {}
    df = table_to_df(node, "company profile table", index_col=0)
    result = {}
    for key, row in df.iterrows():
        if isinstance(key, str) and len(row) > 0 and isinstance(row.iloc[0], str):
            result[key.strip()] = row.iloc[0].strip()
    return result
