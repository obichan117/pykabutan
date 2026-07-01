"""Shared conversion helpers for parsers: table fragments and Japanese number formats."""

import re
from io import StringIO

import pandas as pd

from pykabutan.exceptions import ScrapingError


def require(node, what: str):
    """Return node, or raise ScrapingError naming the missing element."""
    if node is None:
        raise ScrapingError(what)
    return node


def table_to_df(table_node, what: str, **kwargs) -> pd.DataFrame:
    """Parse a single <table> element (not a whole page) into a DataFrame."""
    try:
        return pd.read_html(StringIO(str(table_node)), **kwargs)[0]
    except (ValueError, IndexError) as e:
        raise ScrapingError(what, f"Failed to parse {what}: {e}") from e


def to_float_jp(value) -> float | None:
    """Extract a float from kabutan-formatted text.

    "10.8倍" -> 10.8, "3.67％" -> 3.67, "1,234" -> 1234.0.
    "－倍" (kabutan's no-data marker), None, NaN and empty -> None.
    """
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return None if value != value else float(value)  # NaN -> None
    text = str(value).replace(",", "").replace("−", "-")
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    return float(match.group()) if match else None


def parse_market_cap_yen(value) -> float | None:
    """Parse "39兆7,640億円" style market cap into yen (39.764e12)."""
    if not isinstance(value, str):
        return None
    text = value.replace(",", "")
    total = 0.0
    cho = re.search(r"(\d+(?:\.\d+)?)\s*兆", text)
    oku = re.search(r"(\d+(?:\.\d+)?)\s*億", text)
    if cho:
        total += float(cho.group(1)) * 1e12
    if oku:
        total += float(oku.group(1)) * 1e8
    return total or None


def coerce_numeric(df: pd.DataFrame, columns) -> pd.DataFrame:
    """Coerce the given columns to numeric in place, handling commas,
    unicode minus, and kabutan's "－" no-data marker (becomes NaN)."""
    for col in columns:
        if col in df.columns and df[col].dtype == object:
            cleaned = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace("−", "-", regex=False)
                .str.replace("％", "", regex=False)
                .str.strip()
            )
            df[col] = pd.to_numeric(cleaned, errors="coerce")
    return df
