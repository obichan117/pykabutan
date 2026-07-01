"""Parser for the finance page (/stock/finance).

The page carries ~20 tables without ids; each statement is identified by a
unique column signature (verified 2026-07-02). Historical profit columns are
株探プレミアム-gated and excluded. Money values are in 百万円 (millions of yen)
as published by kabutan.
"""

from io import StringIO

import pandas as pd

from pykabutan._internal import site
from pykabutan._internal.parsers import make_soup
from pykabutan._internal.parsers._convert import coerce_numeric, require
from pykabutan.exceptions import ScrapingError

_WHAT = "financial statement tables"

# Columns that stay text; everything else gets numeric coercion
_TEXT_COLUMNS = {"決算期", "発表日"}


def parse_page(html: str) -> dict[str, pd.DataFrame]:
    """Parse the finance page into named statements.

    Keys (present when kabutan publishes them for the stock):
        annual              — full-year results + current forecast
        interim             — half-year results + forecast
        quarterly           — recent quarterly results
        cashflow            — operating/investing/financing/free cash flow
        profitability       — ROE / ROA / margin history
        financial_position  — equity ratio, total assets, retained earnings
        records             — all-time-high results
    """
    soup = make_soup(html)
    box = require(soup.select_one(site.SEL_FINANCE_BOX), _WHAT)

    statements: dict[str, pd.DataFrame] = {}
    results_seen = 0

    for node in box.find_all("table"):
        if "arrow" in (node.get("class") or []):
            continue  # forecast-revision arrow glyphs, not data
        try:
            df = pd.read_html(StringIO(str(node)))[0]
        except (ValueError, IndexError):
            continue

        key = None
        cols = [str(c) for c in df.columns]
        joined = " ".join(cols)
        first_cell = str(df.iloc[0, 0]) if len(df) else ""

        if "ＲＯＥ" in joined:
            key = "profitability"
        elif "フリーCF" in joined:
            key = "cashflow"
        elif "純資産" in joined:
            key = "financial_position"
        elif "修正方向" in joined or "前年比" in joined or "前年 同期比" in joined:
            continue  # revision history / premium-gated growth tables
        elif first_cell == "過去最高":
            key = "records"
        elif "決算期" in joined and "発表日" in joined:
            if "損益率" in joined:
                key = "quarterly"
            else:
                results_seen += 1
                # 1st = annual, 2nd = interim, 3rd = last-FY quarters (redundant)
                key = {1: "annual", 2: "interim"}.get(results_seen)

        if key and key not in statements:
            numeric_cols = [c for c in df.columns if str(c) not in _TEXT_COLUMNS]
            df = coerce_numeric(df, numeric_cols)
            statements[key] = df.dropna(how="all").reset_index(drop=True)

    if not statements:
        raise ScrapingError(_WHAT)
    return statements
