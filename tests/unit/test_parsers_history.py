"""Unit tests for pykabutan._internal.parsers.history using real fixtures."""

import pandas as pd
import pytest

from pykabutan._internal import site
from pykabutan._internal.parsers import history
from pykabutan.exceptions import ScrapingError

from ..conftest import load_fixture


class TestParsePageDaily:
    def setup_method(self):
        self.df = history.parse_page(load_fixture("kabuka_7203_day_p1.html"))

    def test_shape(self):
        assert self.df.shape == (29, 8)

    def test_columns(self):
        assert list(self.df.columns) == site.HISTORY_COLUMNS

    def test_date_dtype(self):
        assert self.df["date"].dtype == "datetime64[ns]"

    def test_open_close_are_float(self):
        assert pd.api.types.is_float_dtype(self.df["open"])
        assert pd.api.types.is_float_dtype(self.df["close"])

    def test_volume_is_numeric(self):
        assert pd.api.types.is_numeric_dtype(self.df["volume"])

    def test_first_row_date(self):
        assert self.df.iloc[0]["date"] == pd.Timestamp("2026-06-30")

    def test_first_row_close(self):
        assert self.df.iloc[0]["close"] == 2725.0


@pytest.mark.parametrize(
    "fixture_name",
    ["kabuka_7203_wek_p1.html", "kabuka_7203_yar_p1.html"],
)
def test_other_intervals_parse_with_same_columns(fixture_name):
    df = history.parse_page(load_fixture(fixture_name))
    assert list(df.columns) == site.HISTORY_COLUMNS


class TestParsePageMissingTable:
    def test_raises_scraping_error(self):
        with pytest.raises(ScrapingError):
            history.parse_page("<html><body></body></html>")
