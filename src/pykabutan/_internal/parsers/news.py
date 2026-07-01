"""Parser for the news page (/stock/news)."""

import pandas as pd

from pykabutan._internal import site
from pykabutan._internal.parsers import make_soup
from pykabutan._internal.parsers._convert import table_to_df


def parse_page(html: str) -> pd.DataFrame:
    """Parse a news page into a DataFrame with datetime/news_type/title.

    A missing news table means the stock has no news for the requested
    mode, so this returns an empty DataFrame rather than raising.
    """
    soup = make_soup(html)
    node = soup.select_one(site.SEL_NEWS_TABLE)
    if node is None:
        return _empty()
    df = table_to_df(node, "news table")
    if df.shape[1] < len(site.NEWS_COLUMNS):
        return _empty()
    df = df.iloc[:, : len(site.NEWS_COLUMNS)]
    df.columns = site.NEWS_COLUMNS
    # kabutan separates date and time with a non-breaking space
    raw = df["datetime"].astype(str).str.replace("\xa0", " ", regex=False)
    df["datetime"] = pd.to_datetime(raw, format=site.NEWS_DATETIME_FORMAT, errors="coerce")
    return df


def _empty() -> pd.DataFrame:
    return pd.DataFrame(columns=site.NEWS_COLUMNS)
