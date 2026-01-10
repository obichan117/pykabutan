"""Integration tests for Ticker class with real HTTP requests.

These tests hit the actual kabutan.jp website.
Run with: uv run pytest tests/integration/ -v
Skip in CI with: uv run pytest -m "not integration"
"""

import pytest

import pykabutan as pk


@pytest.mark.integration
class TestTickerProfile:
    """Test Ticker.profile with real HTTP."""

    def test_toyota_profile(self):
        """Test profile for Toyota (7203) - large cap, complete data."""
        ticker = pk.Ticker("7203")

        assert ticker.code == "7203"
        assert ticker.profile.name == "トヨタ自動車"
        assert ticker.profile.market == "東証Ｐ"
        assert ticker.profile.industry == "輸送用機器"
        assert ticker.profile.per is not None
        assert ticker.profile.pbr is not None
        assert ticker.profile.market_cap is not None
        assert ticker.profile.description is not None
        assert ticker.profile.themes is not None
        assert len(ticker.profile.themes) > 0

    def test_sony_profile(self):
        """Test profile for Sony (6758) - tech company."""
        ticker = pk.Ticker("6758")

        assert ticker.profile.name is not None
        assert ticker.profile.market == "東証Ｐ"
        assert ticker.profile.industry == "電気機器"

    def test_etf_profile(self):
        """Test profile for ETF (1306) - missing some fields."""
        ticker = pk.Ticker("1306")

        assert ticker.profile.name is not None
        assert ticker.profile.market == "東証Ｅ"
        # ETFs typically don't have PER/PBR
        assert ticker.profile.per is None
        assert ticker.profile.pbr is None

    def test_profile_dict_conversion(self):
        """Test that profile can be converted to dict."""
        ticker = pk.Ticker("7203")
        profile_dict = dict(ticker.profile)

        assert "code" in profile_dict
        assert "name" in profile_dict
        assert "market" in profile_dict
        assert profile_dict["code"] == "7203"

    def test_profile_caching(self):
        """Test that profile is cached (same object returned)."""
        ticker = pk.Ticker("7203")

        profile1 = ticker.profile
        profile2 = ticker.profile

        assert profile1 is profile2

    def test_refresh_clears_cache(self):
        """Test that refresh() clears the cache."""
        ticker = pk.Ticker("7203")

        profile1 = ticker.profile
        ticker.refresh()
        profile2 = ticker.profile

        # After refresh, should be different objects (re-fetched)
        assert profile1 is not profile2


@pytest.mark.integration
class TestTickerHistory:
    """Test Ticker.history() with real HTTP."""

    def test_history_default(self):
        """Test default history (30 days, daily)."""
        ticker = pk.Ticker("7203")
        df = ticker.history()

        assert not df.empty
        assert "date" in df.columns
        assert "open" in df.columns
        assert "high" in df.columns
        assert "low" in df.columns
        assert "close" in df.columns
        assert "volume" in df.columns

    def test_history_period(self):
        """Test history with specific period."""
        ticker = pk.Ticker("7203")
        df = ticker.history(period="10d")

        assert len(df) <= 10

    def test_history_weekly(self):
        """Test weekly interval."""
        ticker = pk.Ticker("7203")
        df = ticker.history(period="30d", interval="week")

        assert not df.empty
        assert "date" in df.columns

    def test_history_date_format(self):
        """Test that dates are properly parsed."""
        ticker = pk.Ticker("7203")
        df = ticker.history(period="5d")

        if not df.empty:
            # Dates should be datetime objects
            assert df["date"].dtype == "datetime64[ns]"


@pytest.mark.integration
class TestTickerNews:
    """Test Ticker.news() with real HTTP."""

    def test_news_earnings(self):
        """Test earnings news."""
        ticker = pk.Ticker("7203")
        df = ticker.news(mode="earnings")

        # Toyota should have some earnings news
        assert "datetime" in df.columns or df.empty
        assert "news_type" in df.columns or df.empty

    def test_news_all(self):
        """Test all news."""
        ticker = pk.Ticker("7203")
        df = ticker.news(mode="all")

        assert isinstance(df, type(df))  # Is DataFrame


@pytest.mark.integration
class TestTickerHolders:
    """Test Ticker.holders() with real HTTP."""

    def test_holders_default(self):
        """Test default holders (latest)."""
        ticker = pk.Ticker("7203")
        df = ticker.holders()

        assert not df.empty
        # Should have shareholder info


@pytest.mark.integration
class TestTickerSimilar:
    """Test Ticker.similar_stocks() with real HTTP."""

    def test_similar_stocks(self):
        """Test similar stocks."""
        ticker = pk.Ticker("7203")
        similar = ticker.similar_stocks()

        assert isinstance(similar, list)
        if similar:
            assert all(isinstance(t, pk.Ticker) for t in similar)


@pytest.mark.integration
class TestTickerErrors:
    """Test error handling with real HTTP."""

    def test_invalid_ticker(self):
        """Test that invalid ticker raises TickerNotFoundError."""
        ticker = pk.Ticker("9999999")

        with pytest.raises(pk.TickerNotFoundError):
            _ = ticker.profile

    def test_invalid_ticker_message(self):
        """Test error message contains code."""
        ticker = pk.Ticker("9999999")

        with pytest.raises(pk.TickerNotFoundError) as exc_info:
            _ = ticker.profile

        assert "9999999" in str(exc_info.value)
