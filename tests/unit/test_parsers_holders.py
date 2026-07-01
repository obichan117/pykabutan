"""Unit tests for pykabutan._internal.parsers.holders using real fixtures."""

import pandas as pd
import pytest

from pykabutan._internal.parsers import holders
from pykabutan.exceptions import ScrapingError

from ..conftest import load_fixture


class TestParsePage:
    def setup_method(self):
        self.df = holders.parse_page(load_fixture("holder_7203_tab0.html"), period=0)

    def test_columns(self):
        assert list(self.df.columns) == ["date", "name", "change", "ratio_percent", "shares"]

    def test_row_count(self):
        assert len(self.df) == 12

    def test_ratio_percent_is_numeric(self):
        assert pd.api.types.is_numeric_dtype(self.df["ratio_percent"])

    def test_first_row_date(self):
        assert self.df.iloc[0]["date"] == "26.03"


def test_missing_table_raises_scraping_error():
    with pytest.raises(ScrapingError):
        holders.parse_page("<html><body></body></html>")
