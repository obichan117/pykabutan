"""Unit tests for custom exceptions."""

import pytest

import pykabutan as pk
from pykabutan.exceptions import PykabutanError, ScrapingError, TickerNotFoundError


class TestTickerNotFoundError:
    def test_inherits_from_base(self):
        assert issubclass(TickerNotFoundError, PykabutanError)

    def test_stores_code_and_message(self):
        error = TickerNotFoundError("7203")
        assert error.code == "7203"
        assert "7203" in str(error)


class TestScrapingError:
    def test_inherits_from_base(self):
        assert issubclass(ScrapingError, PykabutanError)

    def test_stores_what_and_helpful_message(self):
        error = ScrapingError("stats table")
        assert error.what == "stats table"
        assert "stats table" in str(error)
        assert len(str(error)) > len("stats table")


def test_configuration_error_was_removed():
    assert not hasattr(pk, "ConfigurationError")


def test_can_catch_all_with_base():
    for exc in (TickerNotFoundError("7203"), ScrapingError("stats table")):
        with pytest.raises(PykabutanError):
            raise exc
