"""Search functions for finding stocks on kabutan.jp."""

import urllib.parse
from collections import defaultdict

from pykabutan._scraper import get_dfs


# Industry name to code mapping
INDUSTRY_MAP = {
    "水産・農林業": 1,
    "鉱業": 2,
    "建設業": 3,
    "食料品": 4,
    "繊維製品": 5,
    "パルプ・紙": 6,
    "化学": 7,
    "医薬品": 8,
    "石油・石炭": 9,
    "ゴム製品": 10,
    "ガラス・土石": 11,
    "鉄鋼": 12,
    "非鉄金属": 13,
    "金属製品": 14,
    "機械": 15,
    "電気機器": 16,
    "輸送用機器": 17,
    "精密機器": 18,
    "その他製品": 19,
    "電気・ガス": 20,
    "陸運業": 21,
    "海運業": 22,
    "空運業": 23,
    "倉庫・運輸": 24,
    "情報・通信業": 25,
    "卸売業": 26,
    "小売業": 27,
    "銀行業": 28,
    "証券・商品": 29,
    "保険業": 30,
    "その他金融業": 31,
    "不動産業": 32,
    "サービス業": 33,
}

# Market name to code mapping
MARKET_MAP = defaultdict(lambda: 0, {"東証Ｐ": "1", "東証Ｓ": "2", "東証Ｇ": "3", "Prime": "1", "Standard": "2", "Growth": "3"})


def _get_search_url_industry(industry_code: int, market_code: str) -> str:
    """Get URL for industry search."""
    return f"https://kabutan.jp/themes/?industry={industry_code}&market={market_code}"


def _get_search_url_theme(theme: str, market_code: str) -> str:
    """Get URL for theme search."""
    theme_encoded = urllib.parse.quote(theme)
    return f"https://kabutan.jp/themes/?theme={theme_encoded}&market={market_code}"


def _parse_search_results(url: str) -> list:
    """Parse search results and return list of Ticker objects with cached data."""
    from pykabutan.ticker import Ticker

    try:
        tables = get_dfs(url)
        if len(tables) < 3:
            return []

        # Search results table is usually at index 2
        df = tables[2]

        tickers = []

        # Try to find code column
        code_col = None
        name_col = None

        for col in df.columns:
            col_str = str(col).lower()
            if "コード" in col_str or "code" in col_str:
                code_col = col
            elif "銘柄" in col_str or "name" in col_str:
                name_col = col

        # If no code column found, try first column
        if code_col is None:
            code_col = df.columns[0]
        if name_col is None and len(df.columns) > 1:
            name_col = df.columns[1]

        for _, row in df.iterrows():
            try:
                code_val = row[code_col]

                # Extract code - handle both int and string formats
                code = None
                if isinstance(code_val, (int, float)):
                    code = str(int(code_val))
                elif isinstance(code_val, str):
                    # Extract digits from string (handles "135A" format)
                    code = code_val.strip()
                    if not code:
                        continue

                if code:
                    ticker = Ticker(code)
                    # Store name if available
                    if name_col and name_col in row:
                        ticker._search_name = row[name_col]
                    tickers.append(ticker)

            except Exception:
                continue

        return tickers

    except Exception:
        return []


def search_by_industry(industry: str, market: str = "all") -> list:
    """Search for stocks by industry.

    Args:
        industry: Industry name in Japanese (e.g., "電気機器", "輸送用機器")
        market: Market filter - "all", "Prime", "Standard", "Growth",
                or Japanese names like "東証Ｐ"

    Returns:
        List of Ticker objects. Basic info may be cached from search results.

    Example:
        >>> tickers = search_by_industry("電気機器")
        >>> for t in tickers[:5]:
        ...     print(t.code)

    Available industries:
        水産・農林業, 鉱業, 建設業, 食料品, 繊維製品, パルプ・紙, 化学, 医薬品,
        石油・石炭, ゴム製品, ガラス・土石, 鉄鋼, 非鉄金属, 金属製品, 機械,
        電気機器, 輸送用機器, 精密機器, その他製品, 電気・ガス, 陸運業, 海運業,
        空運業, 倉庫・運輸, 情報・通信業, 卸売業, 小売業, 銀行業, 証券・商品,
        保険業, その他金融業, 不動産業, サービス業
    """
    if industry not in INDUSTRY_MAP:
        raise ValueError(f"Unknown industry: {industry}. Available: {list(INDUSTRY_MAP.keys())}")

    industry_code = INDUSTRY_MAP[industry]
    market_code = MARKET_MAP[market]
    url = _get_search_url_industry(industry_code, market_code)
    return _parse_search_results(url)


def search_by_theme(theme: str, market: str = "all") -> list:
    """Search for stocks by theme.

    Args:
        theme: Theme name in Japanese (e.g., "人工知能", "半導体", "電気自動車関連")
               Note: Must be in Japanese. English terms like "AI" won't work.
        market: Market filter - "all", "Prime", "Standard", "Growth"

    Returns:
        List of Ticker objects. Basic info may be cached from search results.

    Example:
        >>> tickers = search_by_theme("人工知能")  # AI
        >>> for t in tickers[:5]:
        ...     print(t.code)

        >>> tickers = search_by_theme("半導体")  # Semiconductor
    """
    market_code = MARKET_MAP[market]
    url = _get_search_url_theme(theme, market_code)
    return _parse_search_results(url)


def list_industries() -> list[str]:
    """Get list of available industry names.

    Returns:
        List of industry names that can be used with search_by_industry().
    """
    return list(INDUSTRY_MAP.keys())
