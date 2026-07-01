"""Parser for the price history page (/stock/kabuka)."""

import pandas as pd

from pykabutan._internal import site
from pykabutan._internal.parsers import make_soup
from pykabutan._internal.parsers._convert import coerce_numeric, require, table_to_df
from pykabutan.exceptions import ScrapingError

_WHAT = "price history table"

# Everything except the date is a number
_NUMERIC_COLUMNS = site.HISTORY_COLUMNS[1:]


def parse_page(html: str) -> pd.DataFrame:
    """Parse one kabuka page into an OHLC DataFrame (page order: newest first).

    Columns: date (datetime64), open, high, low, close, change,
    percent_change, volume (all numeric).
    """
    soup = make_soup(html)
    node = require(soup.select_one(site.SEL_HISTORY_TABLE), _WHAT)
    df = table_to_df(node, _WHAT)
    if df.shape[1] != len(site.HISTORY_COLUMNS):
        raise ScrapingError(
            _WHAT,
            f"Price history table has {df.shape[1]} columns, "
            f"expected {len(site.HISTORY_COLUMNS)}; kabutan.jp layout may have changed.",
        )
    df.columns = site.HISTORY_COLUMNS
    df["date"] = pd.to_datetime(df["date"], format=site.DATE_FORMAT, errors="coerce")
    df = df.dropna(subset=["date"])
    return coerce_numeric(df, _NUMERIC_COLUMNS)
