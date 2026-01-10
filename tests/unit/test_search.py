"""Unit tests for search functions."""

import pytest

import pykabutan as pk
from pykabutan.search import (
    INDUSTRY_MAP,
    MARKET_MAP,
    _get_search_url_industry,
    _get_search_url_theme,
    list_industries,
)


class TestIndustryMap:
    """Test industry mapping."""

    def test_industry_map_has_33_entries(self):
        """Test that there are 33 industries."""
        assert len(INDUSTRY_MAP) == 33

    def test_industry_map_values_are_integers(self):
        """Test that industry codes are integers."""
        for name, code in INDUSTRY_MAP.items():
            assert isinstance(code, int)
            assert 1 <= code <= 33

    def test_common_industries_exist(self):
        """Test that common industries are in the map."""
        assert "電気機器" in INDUSTRY_MAP
        assert "輸送用機器" in INDUSTRY_MAP
        assert "銀行業" in INDUSTRY_MAP
        assert "情報・通信業" in INDUSTRY_MAP


class TestMarketMap:
    """Test market mapping."""

    def test_market_map_defaults_to_zero(self):
        """Test that unknown markets default to 0 (all)."""
        assert MARKET_MAP["unknown"] == 0
        assert MARKET_MAP["all"] == 0

    def test_market_map_japanese_names(self):
        """Test Japanese market names."""
        assert MARKET_MAP["東証Ｐ"] == "1"
        assert MARKET_MAP["東証Ｓ"] == "2"
        assert MARKET_MAP["東証Ｇ"] == "3"

    def test_market_map_english_names(self):
        """Test English market names."""
        assert MARKET_MAP["Prime"] == "1"
        assert MARKET_MAP["Standard"] == "2"
        assert MARKET_MAP["Growth"] == "3"


class TestUrlGeneration:
    """Test URL generation functions."""

    def test_industry_url(self):
        """Test industry search URL."""
        url = _get_search_url_industry(16, "0")
        assert "industry=16" in url
        assert "market=0" in url
        assert "kabutan.jp/themes" in url

    def test_theme_url(self):
        """Test theme search URL."""
        url = _get_search_url_theme("AI", "0")
        assert "theme=" in url
        assert "market=0" in url
        assert "kabutan.jp/themes" in url

    def test_theme_url_encodes_japanese(self):
        """Test that Japanese themes are URL encoded."""
        url = _get_search_url_theme("人工知能", "0")
        # Should not contain raw Japanese
        assert "人工知能" not in url
        # Should be URL encoded
        assert "%E4%BA%BA%E5%B7%A5%E7%9F%A5%E8%83%BD" in url


class TestListIndustries:
    """Test list_industries function."""

    def test_returns_list(self):
        """Test that function returns a list."""
        industries = list_industries()
        assert isinstance(industries, list)

    def test_returns_33_industries(self):
        """Test that function returns 33 industries."""
        industries = list_industries()
        assert len(industries) == 33

    def test_industries_are_strings(self):
        """Test that industries are strings."""
        industries = list_industries()
        assert all(isinstance(i, str) for i in industries)


class TestSearchByIndustryValidation:
    """Test search_by_industry validation."""

    def test_invalid_industry_raises_value_error(self):
        """Test that invalid industry raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            pk.search_by_industry("invalid_industry")

        assert "Unknown industry" in str(exc_info.value)

    def test_error_message_contains_available_industries(self):
        """Test that error message mentions available industries."""
        with pytest.raises(ValueError) as exc_info:
            pk.search_by_industry("not_real")

        # Should hint at available options
        assert "Available" in str(exc_info.value)


class TestSearchByThemeValidation:
    """Test search_by_theme validation."""

    def test_empty_theme_works(self, mocker, mock_response, sample_search_html):
        """Test that empty theme returns empty list."""
        mocker.patch(
            "pykabutan._scraper.requests.get",
            return_value=mock_response(sample_search_html)
        )

        # Empty or invalid theme should not crash
        result = pk.search_by_theme("")
        assert isinstance(result, list)
