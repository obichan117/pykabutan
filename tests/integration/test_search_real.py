"""Integration tests for search functions with real HTTP requests.

These tests hit the actual kabutan.jp website.
Run with: uv run pytest tests/integration/ -v
"""

import pytest

import pykabutan as pk


@pytest.mark.integration
class TestSearchByIndustry:
    """Test search_by_industry() with real HTTP."""

    def test_search_electronics(self):
        """Test search for electronics industry."""
        tickers = pk.search_by_industry("電気機器")

        assert isinstance(tickers, list)
        assert len(tickers) > 0
        assert all(isinstance(t, pk.Ticker) for t in tickers)

    def test_search_automotive(self):
        """Test search for automotive industry."""
        tickers = pk.search_by_industry("輸送用機器")

        assert len(tickers) > 0

    def test_search_returns_tickers(self):
        """Test that search returns Ticker objects."""
        tickers = pk.search_by_industry("電気機器")

        if tickers:
            # Should be able to access profile
            first = tickers[0]
            assert hasattr(first, "code")
            assert hasattr(first, "profile")

    def test_search_invalid_industry(self):
        """Test that invalid industry raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            pk.search_by_industry("invalid_industry")

        assert "Unknown industry" in str(exc_info.value)

    def test_search_with_market_filter(self):
        """Test search with market filter."""
        tickers_all = pk.search_by_industry("電気機器", market="all")
        tickers_prime = pk.search_by_industry("電気機器", market="Prime")

        # Prime should be subset of all (or equal)
        assert len(tickers_prime) <= len(tickers_all)


@pytest.mark.integration
class TestSearchByTheme:
    """Test search_by_theme() with real HTTP."""

    def test_search_ai_theme(self):
        """Test search for AI theme (人工知能)."""
        tickers = pk.search_by_theme("人工知能")

        assert isinstance(tickers, list)
        assert len(tickers) > 0

    def test_search_semiconductor_theme(self):
        """Test search for semiconductor theme (半導体)."""
        tickers = pk.search_by_theme("半導体")

        assert len(tickers) > 0

    def test_search_ev_theme(self):
        """Test search for EV theme."""
        tickers = pk.search_by_theme("電気自動車関連")

        assert isinstance(tickers, list)


@pytest.mark.integration
class TestListIndustries:
    """Test list_industries() function."""

    def test_list_industries(self):
        """Test that list_industries returns all industries."""
        industries = pk.list_industries()

        assert isinstance(industries, list)
        assert len(industries) == 33  # Japan has 33 industry sectors
        assert "電気機器" in industries
        assert "輸送用機器" in industries
        assert "銀行業" in industries
