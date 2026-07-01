"""Unit tests for pykabutan._internal.parsers.finance using real fixtures."""

import pytest

from pykabutan._internal.parsers import finance
from pykabutan.exceptions import ScrapingError

from ..conftest import load_fixture


class TestParsePage:
    def setup_method(self):
        self.statements = finance.parse_page(load_fixture("finance_7203.html"))

    def test_keys(self):
        assert set(self.statements.keys()) == {
            "annual",
            "interim",
            "quarterly",
            "cashflow",
            "profitability",
            "financial_position",
            "records",
        }

    def test_annual_has_expected_columns(self):
        annual = self.statements["annual"]
        assert "決算期" in annual.columns
        assert "発表日" in annual.columns

    def test_annual_revenue_is_numeric(self):
        import pandas as pd

        assert pd.api.types.is_numeric_dtype(self.statements["annual"]["売上高"])

    def test_annual_has_no_all_nan_rows(self):
        annual = self.statements["annual"]
        assert not annual.isna().all(axis=1).any()

    def test_cashflow_has_free_cf_column(self):
        assert "フリーCF" in self.statements["cashflow"].columns


def test_missing_finance_box_raises_scraping_error():
    with pytest.raises(ScrapingError):
        finance.parse_page("<html><body></body></html>")
