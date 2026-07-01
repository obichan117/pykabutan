"""Unit tests for pykabutan._internal.parsers._convert helpers."""

import math

import pandas as pd
import pytest

from pykabutan._internal.parsers._convert import (
    coerce_numeric,
    parse_market_cap_yen,
    to_float_jp,
)


class TestToFloatJp:
    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("10.8倍", 10.8),
            ("3.67％", 3.67),
            ("1,234", 1234.0),
            ("－倍", None),
            ("", None),
            (None, None),
            ("−5.2", -5.2),  # unicode minus (U+2212)
        ],
    )
    def test_values(self, value, expected):
        assert to_float_jp(value) == expected

    def test_nan_returns_none(self):
        assert to_float_jp(float("nan")) is None


class TestParseMarketCapYen:
    def test_cho_and_oku(self):
        assert parse_market_cap_yen("39兆7,640億円") == 39.764e12

    def test_oku_only(self):
        assert parse_market_cap_yen("457億円") == 45.7e9

    def test_unparseable_text(self):
        assert parse_market_cap_yen("abc") is None

    def test_none(self):
        assert parse_market_cap_yen(None) is None


class TestCoerceNumeric:
    def test_coerces_commas_minus_and_dash(self):
        df = pd.DataFrame({"a": ["1,234", "−2", "－"]})
        result = coerce_numeric(df, ["a"])
        assert result["a"].iloc[0] == 1234.0
        assert result["a"].iloc[1] == -2.0
        assert math.isnan(result["a"].iloc[2])
