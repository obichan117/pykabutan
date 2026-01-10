"""Profile dataclass for stock information from kabutan main page."""

from dataclasses import dataclass, fields


@dataclass
class Profile:
    """Stock profile information from kabutan.jp main page.

    All fields except code are optional and may be None for ETFs or
    stocks with incomplete data.

    Attributes:
        code: Stock code (e.g., "7203")
        name: Company name in Japanese
        market: Market name (東証P, 東証S, 東証G, etc.)
        industry: Industry sector name
        description: Company description
        themes: List of theme tags
        website: Company website URL
        english_name: Company name in English
        per: Price-to-Earnings Ratio
        pbr: Price-to-Book Ratio
        market_cap: Market capitalization in yen
        dividend_yield: Dividend yield percentage
        margin_ratio: Margin trading ratio
    """

    code: str
    name: str | None = None
    market: str | None = None
    industry: str | None = None
    description: str | None = None
    themes: list[str] | None = None
    website: str | None = None
    english_name: str | None = None
    per: float | None = None
    pbr: float | None = None
    market_cap: float | None = None
    dividend_yield: float | None = None
    margin_ratio: float | None = None

    def __iter__(self):
        """Enable dict(profile) conversion."""
        for field in fields(self):
            yield field.name, getattr(self, field.name)

    def to_dict(self) -> dict:
        """Convert profile to dictionary."""
        return dict(self)
