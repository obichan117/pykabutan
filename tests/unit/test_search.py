"""Unit tests for search functions, with pykabutan._internal.http.fetch mocked."""

import pytest

import pykabutan as pk
from pykabutan._internal import site

from ..conftest import load_fixture


class TestSearchByIndustryValidation:
    def test_unknown_industry_raises_value_error(self):
        with pytest.raises(ValueError):
            pk.search_by_industry("nonexistent")

    def test_unknown_market_raises_value_error(self):
        with pytest.raises(ValueError):
            pk.search_by_industry("電気機器", market="bogus")


class TestSearchByIndustry:
    def test_returns_tickers_from_fixture(self, mocker):
        mocker.patch(
            "pykabutan._internal.http.fetch",
            return_value=load_fixture("themes_industry16.html"),
        )

        results = pk.search_by_industry("電気機器")

        assert len(results) == 15
        assert results[0].code == "285A"
        assert results[0]._search_name == "キオクシア"


class TestListIndustries:
    def test_returns_33_industries_including_electronics(self):
        industries = pk.list_industries()

        assert len(industries) == 33
        assert "電気機器" in industries


class TestMarketMap:
    def test_market_map_is_a_plain_dict(self):
        assert type(site.MARKET_MAP) is dict
        assert not hasattr(site.MARKET_MAP, "default_factory")
