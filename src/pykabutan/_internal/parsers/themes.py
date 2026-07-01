"""Parser for search results pages (/themes/?industry= and /themes/?theme=)."""

from pykabutan._internal import site
from pykabutan._internal.parsers import make_soup
from pykabutan._internal.parsers._convert import table_to_df


def parse_search_results(html: str) -> list[dict]:
    """Parse a themes search page into [{"code": ..., "name": ...}, ...].

    A missing results table means the search returned nothing (e.g. an
    unknown theme), so this returns [] rather than raising.
    """
    soup = make_soup(html)
    node = soup.select_one(site.SEL_SEARCH_TABLE)
    if node is None:
        return []
    df = table_to_df(node, "search results table")

    code_col = None
    name_col = None
    for col in df.columns:
        col_str = str(col)
        if code_col is None and "コード" in col_str:
            code_col = col
        elif name_col is None and "銘柄" in col_str:
            name_col = col
    if code_col is None:
        code_col = df.columns[0]
    if name_col is None and len(df.columns) > 1:
        name_col = df.columns[1]

    results = []
    for _, row in df.iterrows():
        code = _normalize_code(row[code_col])
        if not code:
            continue
        name = row[name_col] if name_col is not None else None
        results.append({"code": code, "name": name if isinstance(name, str) else None})
    return results


def _normalize_code(value) -> str | None:
    """Ticker codes come back as ints (7203) or strings ("135A")."""
    if isinstance(value, (int, float)):
        return str(int(value)) if value == value else None
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None
