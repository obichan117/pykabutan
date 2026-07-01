"""Unit tests for pykabutan._internal.parsers.themes using real fixtures."""

from pykabutan._internal.parsers import themes

from ..conftest import load_fixture


class TestParseSearchResults:
    def setup_method(self):
        self.results = themes.parse_search_results(load_fixture("themes_industry16.html"))

    def test_count(self):
        assert len(self.results) == 15

    def test_first_result(self):
        assert self.results[0] == {"code": "285A", "name": "キオクシア"}

    def test_alphanumeric_codes_preserved(self):
        codes = [r["code"] for r in self.results]
        assert any(not code.isdigit() for code in codes)


def test_empty_page_returns_empty_list():
    assert themes.parse_search_results("<html><body></body></html>") == []
