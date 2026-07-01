"""Unit tests for pykabutan._internal.parsers.news using real fixtures."""

import pandas as pd

from pykabutan._internal import site
from pykabutan._internal.parsers import news

from ..conftest import load_fixture


class TestParsePageEarnings:
    def setup_method(self):
        self.df = news.parse_page(load_fixture("news_7203_nmode2.html"))

    def test_row_count(self):
        assert len(self.df) == 8

    def test_columns(self):
        assert list(self.df.columns) == ["datetime", "news_type", "title"]

    def test_datetime_dtype(self):
        assert self.df["datetime"].dtype == "datetime64[ns]"

    def test_first_datetime(self):
        assert self.df.iloc[0]["datetime"] == pd.Timestamp("2026-05-08 13:55")


def test_all_news_mode_row_count():
    df = news.parse_page(load_fixture("news_7203_nmode0.html"))
    assert len(df) == 15


def test_missing_table_returns_empty_dataframe():
    df = news.parse_page("<html><body></body></html>")
    assert df.empty
    assert list(df.columns) == site.NEWS_COLUMNS
