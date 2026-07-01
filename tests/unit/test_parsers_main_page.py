"""Unit tests for pykabutan._internal.parsers.main_page using real fixtures."""

import pytest

from pykabutan._internal.parsers import main_page, make_soup
from pykabutan.exceptions import ScrapingError

from ..conftest import load_fixture


class TestParseProfileToyota:
    """main_7203.html: a large-cap stock with complete data."""

    def setup_method(self):
        self.soup = make_soup(load_fixture("main_7203.html"))
        self.profile = main_page.parse_profile(self.soup, "7203")

    def test_name(self):
        assert self.profile.name == "トヨタ自動車"

    def test_market(self):
        assert self.profile.market == "東証Ｐ"

    def test_industry(self):
        assert self.profile.industry == "輸送用機器"

    def test_per(self):
        assert self.profile.per == 10.8

    def test_pbr(self):
        assert self.profile.pbr == 0.81

    def test_market_cap(self):
        assert self.profile.market_cap == 39764000000000.0

    def test_dividend_yield(self):
        assert self.profile.dividend_yield == 3.67

    def test_margin_ratio(self):
        assert self.profile.margin_ratio == 10.18

    def test_english_name(self):
        assert self.profile.english_name == "TOYOTA MOTOR CORPORATION"

    def test_themes(self):
        assert isinstance(self.profile.themes, list)
        assert "自動車" in self.profile.themes

    def test_website(self):
        assert self.profile.website.startswith("https://")


class TestParseProfileLossMaker:
    """main_4755.html: PER is undisclosed (kabutan shows －倍 for loss-makers)."""

    def test_per_is_none(self):
        soup = make_soup(load_fixture("main_4755.html"))
        profile = main_page.parse_profile(soup, "4755")
        assert profile.per is None

    def test_pbr(self):
        soup = make_soup(load_fixture("main_4755.html"))
        profile = main_page.parse_profile(soup, "4755")
        assert profile.pbr == 1.77


class TestParseProfileAlphanumericCode:
    """main_135A.html: newer listings use alphanumeric codes."""

    def setup_method(self):
        self.soup = make_soup(load_fixture("main_135A.html"))

    def test_name(self):
        profile = main_page.parse_profile(self.soup, "135A")
        assert profile.name == "ヴレインＳ"

    def test_similar_codes_preserve_alphanumeric(self):
        codes = main_page.parse_similar_codes(self.soup)
        assert "277A" in codes


class TestParseProfileEtf:
    """main_1306.html: an ETF has no PER/themes but does have a name."""

    def setup_method(self):
        self.soup = make_soup(load_fixture("main_1306.html"))
        self.profile = main_page.parse_profile(self.soup, "1306")

    def test_per_is_none(self):
        assert self.profile.per is None

    def test_themes_is_none(self):
        assert self.profile.themes is None

    def test_name_is_not_none(self):
        assert self.profile.name is not None


class TestIsStockPage:
    def test_not_found_page_is_not_a_stock_page(self):
        soup = make_soup(load_fixture("main_notfound_99999.html"))
        assert main_page.is_stock_page(soup) is False

    def test_real_page_is_a_stock_page(self):
        soup = make_soup(load_fixture("main_7203.html"))
        assert main_page.is_stock_page(soup) is True


class TestParseProfileMissingStatsTable:
    def test_raises_scraping_error_naming_stats(self):
        soup = make_soup("<html><body><h2>7203 X</h2></body></html>")
        with pytest.raises(ScrapingError) as exc_info:
            main_page.parse_profile(soup, "7203")
        assert "stats" in exc_info.value.what
