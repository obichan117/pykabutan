"""Unit tests for the Ticker facade, with pykabutan._internal.http.fetch mocked."""

import pandas as pd
import pytest
import requests

import pykabutan as pk
from pykabutan.ticker import Ticker

from ..conftest import load_fixture


class TestLazyLoading:
    def test_construction_makes_no_http_request(self, mocker):
        mock_fetch = mocker.patch("pykabutan._internal.http.fetch")

        Ticker("7203")

        mock_fetch.assert_not_called()

    def test_repr(self):
        assert repr(Ticker("7203")) == "Ticker('7203')"


class TestProfileCaching:
    def test_profile_triggers_one_fetch(self, mocker):
        mock_fetch = mocker.patch(
            "pykabutan._internal.http.fetch",
            return_value=load_fixture("main_7203.html"),
        )
        ticker = Ticker("7203")

        _ = ticker.profile

        mock_fetch.assert_called_once()

    def test_second_access_is_cached(self, mocker):
        mock_fetch = mocker.patch(
            "pykabutan._internal.http.fetch",
            return_value=load_fixture("main_7203.html"),
        )
        ticker = Ticker("7203")

        _ = ticker.profile
        _ = ticker.profile

        assert mock_fetch.call_count == 1

    def test_refresh_forces_refetch(self, mocker):
        mock_fetch = mocker.patch(
            "pykabutan._internal.http.fetch",
            return_value=load_fixture("main_7203.html"),
        )
        ticker = Ticker("7203")

        _ = ticker.profile
        ticker.refresh()
        _ = ticker.profile

        assert mock_fetch.call_count == 2


class TestTickerNotFound:
    def test_http_404_raises_ticker_not_found(self, mocker):
        response = mocker.Mock(status_code=404)
        mocker.patch(
            "pykabutan._internal.http.fetch",
            side_effect=requests.HTTPError(response=response),
        )
        ticker = Ticker("9999999")

        with pytest.raises(pk.TickerNotFoundError):
            _ = ticker.profile

    def test_http_500_propagates(self, mocker):
        response = mocker.Mock(status_code=500)
        mocker.patch(
            "pykabutan._internal.http.fetch",
            side_effect=requests.HTTPError(response=response),
        )
        ticker = Ticker("7203")

        with pytest.raises(requests.HTTPError):
            _ = ticker.profile

    def test_not_found_page_content_raises_ticker_not_found(self, mocker):
        mocker.patch(
            "pykabutan._internal.http.fetch",
            return_value=load_fixture("main_notfound_99999.html"),
        )
        ticker = Ticker("99999")

        with pytest.raises(pk.TickerNotFoundError):
            _ = ticker.profile


class TestHistory:
    def test_pagination_stops_on_repeated_oldest_date(self, mocker):
        mock_fetch = mocker.patch(
            "pykabutan._internal.http.fetch",
            side_effect=[
                load_fixture("kabuka_7203_day_p1.html"),
                load_fixture("kabuka_7203_day_p2.html"),
                load_fixture("kabuka_7203_day_p1.html"),
            ],
        )
        ticker = Ticker("7203")

        df = ticker.history(period="1y", interval="day")

        # Must not loop forever: the third (repeated) page ends pagination.
        assert mock_fetch.call_count == 3
        assert isinstance(df.index, pd.DatetimeIndex)
        assert df.index.name == "date"
        assert df.index.is_monotonic_increasing
        assert list(df.columns) == [
            "open",
            "high",
            "low",
            "close",
            "change",
            "percent_change",
            "volume",
        ]

    def test_short_period_stops_after_one_page(self, mocker):
        mock_fetch = mocker.patch(
            "pykabutan._internal.http.fetch",
            return_value=load_fixture("kabuka_7203_day_p1.html"),
        )
        ticker = Ticker("7203")

        ticker.history(period="10d")

        assert mock_fetch.call_count == 1

    def test_unknown_interval_raises_value_error(self):
        ticker = Ticker("7203")
        with pytest.raises(ValueError):
            ticker.history(interval="bogus")

    def test_unknown_period_raises_value_error(self):
        ticker = Ticker("7203")
        with pytest.raises(ValueError):
            ticker.history(period="bogus")


class TestNews:
    def test_unknown_mode_raises_value_error(self):
        ticker = Ticker("7203")
        with pytest.raises(ValueError):
            ticker.news(mode="bogus")

    def test_earnings_mode(self, mocker):
        mocker.patch(
            "pykabutan._internal.http.fetch",
            return_value=load_fixture("news_7203_nmode2.html"),
        )
        ticker = Ticker("7203")

        df = ticker.news(mode="earnings")

        assert len(df) == 8


class TestFinancials:
    def test_returns_dict_with_annual_key(self, mocker):
        mocker.patch(
            "pykabutan._internal.http.fetch",
            return_value=load_fixture("finance_7203.html"),
        )
        ticker = Ticker("7203")

        result = ticker.financials()

        assert "annual" in result


class TestSimilarStocks:
    def test_codes_include_alphanumeric(self, mocker):
        mocker.patch(
            "pykabutan._internal.http.fetch",
            return_value=load_fixture("main_135A.html"),
        )
        ticker = Ticker("135A")

        similar = ticker.similar_stocks()

        codes = [t.code for t in similar]
        assert "277A" in codes
