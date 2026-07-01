"""Parser for the shareholders page (/stock/holder)."""

import pandas as pd

from pykabutan._internal import site
from pykabutan._internal.parsers import make_soup
from pykabutan._internal.parsers._convert import coerce_numeric, require, table_to_df

_WHAT = "shareholders table"


def parse_page(html: str, period: int = 0) -> pd.DataFrame:
    """Parse a holders page into a DataFrame.

    Columns: date (reporting period label, when available), name, change,
    ratio_percent, shares.
    """
    soup = make_soup(html)
    node = require(soup.select_one(site.SEL_HOLDERS_TABLE), _WHAT)
    df = table_to_df(node, _WHAT)

    # Header is a 2-level MultiIndex (株主名 / 持ち株); flatten it
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(0)
    if df.shape[1] == len(site.HOLDERS_COLUMNS):
        df.columns = site.HOLDERS_COLUMNS
    df = coerce_numeric(df, ["ratio_percent", "shares"])

    # Reporting period label from the date menu (optional)
    links = soup.select(site.SEL_HOLDERS_DATE_MENU)
    if len(links) > period:
        df.insert(0, "date", links[period].get_text(strip=True))
    return df
