"""Every kabutan.jp-specific constant in one place.

When kabutan.jp changes its markup, this file is the single point of update:
URL patterns, CSS selectors, table matchers, and value mappings all live here.
Verified against the live site on 2026-07-02.
"""

BASE_URL = "https://kabutan.jp"

# kabutan serves UTF-8 and declares it; fixed to skip per-response charset detection
ENCODING = "utf-8"

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

# === URL patterns ===

URL_MAIN = BASE_URL + "/stock/?code={code}"
URL_HISTORY = BASE_URL + "/stock/kabuka?code={code}&ashi={ashi}&page={page}"
URL_NEWS = BASE_URL + "/stock/news?code={code}&nmode={nmode}"
URL_FINANCE = BASE_URL + "/stock/finance?code={code}"
URL_HOLDER = BASE_URL + "/stock/holder?code={code}&tab={tab}"
URL_SEARCH_INDUSTRY = BASE_URL + "/themes/?industry={industry_code}&market={market_code}"
URL_SEARCH_THEME = BASE_URL + "/themes/?theme={theme}&market={market_code}"

# === Value mappings (public API value -> kabutan query value) ===

# history() interval -> `ashi` query parameter
INTERVAL_MAP = {
    "day": "day",
    "1d": "day",
    "week": "wek",
    "1w": "wek",
    "month": "mon",
    "1mo": "mon",
    "year": "yar",
    "1y": "yar",
}

# news() mode -> `nmode` query parameter
NEWS_MODE_MAP = {"all": 0, "material": 1, "earnings": 2, "disclosure": 3}

# search market filter -> `market` query parameter
MARKET_MAP = {
    "all": "0",
    "Prime": "1",
    "Standard": "2",
    "Growth": "3",
    "東証Ｐ": "1",
    "東証Ｓ": "2",
    "東証Ｇ": "3",
}

# Industry name -> kabutan industry code (33 TSE sectors)
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

# === Date/number formats ===

DATE_FORMAT = "%y/%m/%d"  # e.g. 26/06/30
NEWS_DATETIME_FORMAT = "%y/%m/%d %H:%M"  # e.g. 26/05/08 13:55

# === CSS selectors (verified against live pages 2026-07-02) ===

# Main page (/stock/?code=)
SEL_NAME = "h2"  # "7203　トヨタ自動車"
SEL_MARKET = "span.market"  # "東証Ｐ"
SEL_INDUSTRY = "#stockinfo_i2 a"  # "輸送用機器"
SEL_STATS_TABLE = "#stockinfo_i3 table"  # PER / PBR / 利回り / 信用倍率 / 時価総額
SEL_PROFILE_TABLE = "div.company_block table"  # 英語社名 / 会社サイト / 概要 / テーマ
SEL_SIMILAR_LINKS = "dl.si_i1_dl2 a"  # "テーマ株・関連株" similar-stock links
SEL_ERROR_DIV = "div.error"

# Price history page (/stock/kabuka) — same class for day/week/month/year
SEL_HISTORY_TABLE = "table.stock_kabuka_dwm"

# News page (/stock/news)
SEL_NEWS_TABLE = "table.s_news_list"

# Holders page (/stock/holder)
SEL_HOLDERS_TABLE = "table.stock_holder_1"
SEL_HOLDERS_DATE_MENU = "div.stock_holder_title.date_menu a"

# Search results page (/themes/)
SEL_SEARCH_TABLE = "table.stock_table"

# Finance page (/stock/finance)
SEL_FINANCE_BOX = "div#finance_box"

# Extract a ticker code from an href like "/stock/?code=277A"
CODE_IN_HREF_RE = r"code=([0-9A-Za-z]+)"

# Safety cap on history pagination (~50 pages ≈ 6 years of daily data)
HISTORY_MAX_PAGES = 50

# === Output column names ===

HISTORY_COLUMNS = ["date", "open", "high", "low", "close", "change", "percent_change", "volume"]
NEWS_COLUMNS = ["datetime", "news_type", "title"]
HOLDERS_COLUMNS = ["name", "change", "ratio_percent", "shares"]
