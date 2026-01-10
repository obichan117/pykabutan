"""Unit tests for Ticker class with mocked HTTP."""

import pytest

import pykabutan as pk
from pykabutan.ticker import Ticker


class TestTickerInit:
    """Test Ticker initialization."""

    def test_init_stores_code(self):
        """Test that init stores the code."""
        ticker = Ticker("7203")
        assert ticker.code == "7203"

    def test_init_converts_int_to_str(self):
        """Test that int code is converted to string."""
        ticker = Ticker(7203)
        assert ticker.code == "7203"
        assert isinstance(ticker.code, str)

    def test_init_no_http_request(self, mocker):
        """Test that init doesn't make HTTP request (lazy loading)."""
        mock_get = mocker.patch("pykabutan._scraper.requests.get")

        ticker = Ticker("7203")

        mock_get.assert_not_called()

    def test_repr(self):
        """Test string representation."""
        ticker = Ticker("7203")
        assert repr(ticker) == "Ticker('7203')"


class TestTickerProfile:
    """Test Ticker.profile with mocked HTTP."""

    def test_profile_triggers_http(self, mocker, sample_main_page_html, mock_response):
        """Test that accessing profile triggers HTTP request."""
        mock_get = mocker.patch(
            "pykabutan._scraper.requests.get",
            return_value=mock_response(sample_main_page_html)
        )

        ticker = Ticker("7203")
        _ = ticker.profile

        mock_get.assert_called_once()

    def test_profile_caching(self, mocker, sample_main_page_html, mock_response):
        """Test that profile is cached."""
        mock_get = mocker.patch(
            "pykabutan._scraper.requests.get",
            return_value=mock_response(sample_main_page_html)
        )

        ticker = Ticker("7203")
        _ = ticker.profile
        _ = ticker.profile
        _ = ticker.profile

        # Should only call once due to caching
        mock_get.assert_called_once()

    def test_profile_parses_name(self, mocker, sample_main_page_html, mock_response):
        """Test that profile parses company name."""
        mocker.patch(
            "pykabutan._scraper.requests.get",
            return_value=mock_response(sample_main_page_html)
        )

        ticker = Ticker("7203")
        assert ticker.profile.name == "トヨタ自動車"

    def test_profile_parses_market(self, mocker, sample_main_page_html, mock_response):
        """Test that profile parses market."""
        mocker.patch(
            "pykabutan._scraper.requests.get",
            return_value=mock_response(sample_main_page_html)
        )

        ticker = Ticker("7203")
        assert ticker.profile.market == "東証Ｐ"

    def test_profile_parses_industry(self, mocker, sample_main_page_html, mock_response):
        """Test that profile parses industry."""
        mocker.patch(
            "pykabutan._scraper.requests.get",
            return_value=mock_response(sample_main_page_html)
        )

        ticker = Ticker("7203")
        assert ticker.profile.industry == "輸送用機器"


class TestTickerRefresh:
    """Test Ticker.refresh() method."""

    def test_refresh_clears_cache(self, mocker, sample_main_page_html, mock_response):
        """Test that refresh clears the cache."""
        mock_get = mocker.patch(
            "pykabutan._scraper.requests.get",
            return_value=mock_response(sample_main_page_html)
        )

        ticker = Ticker("7203")
        _ = ticker.profile
        ticker.refresh()
        _ = ticker.profile

        # Should call twice - once before refresh, once after
        assert mock_get.call_count == 2


class TestTickerNotFound:
    """Test Ticker with invalid code."""

    def test_404_raises_ticker_not_found(self, mocker, mock_response):
        """Test that 404 response raises TickerNotFoundError."""
        mocker.patch(
            "pykabutan._scraper.requests.get",
            return_value=mock_response("Not Found", status_code=404)
        )

        ticker = Ticker("9999999")

        with pytest.raises(pk.TickerNotFoundError):
            _ = ticker.profile


class TestTickerUrls:
    """Test Ticker URL generation."""

    def test_main_url(self):
        """Test main page URL."""
        ticker = Ticker("7203")
        assert ticker._url_main == "https://kabutan.jp/stock/?code=7203"

    def test_history_url(self):
        """Test history page URL."""
        ticker = Ticker("7203")
        url = ticker._url_history("day", 1)
        assert "code=7203" in url
        assert "ashi=day" in url
        assert "page=1" in url

    def test_news_url(self):
        """Test news page URL."""
        ticker = Ticker("7203")
        url = ticker._url_news(2)
        assert "code=7203" in url
        assert "nmode=2" in url

    def test_finance_url(self):
        """Test finance page URL."""
        ticker = Ticker("7203")
        assert "code=7203" in ticker._url_finance
        assert "finance" in ticker._url_finance

    def test_holder_url(self):
        """Test holder page URL."""
        ticker = Ticker("7203")
        url = ticker._url_holder(0)
        assert "code=7203" in url
        assert "tab=0" in url
