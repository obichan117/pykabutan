"""Unit tests for custom exceptions."""

import pytest

from pykabutan.exceptions import (
    ConfigurationError,
    PykabutanError,
    ScrapingError,
    TickerNotFoundError,
)


class TestPykabutanError:
    """Test base PykabutanError."""

    def test_is_exception(self):
        """Test that it's an Exception subclass."""
        assert issubclass(PykabutanError, Exception)

    def test_can_raise(self):
        """Test that it can be raised."""
        with pytest.raises(PykabutanError):
            raise PykabutanError("test error")

    def test_message(self):
        """Test error message."""
        error = PykabutanError("test message")
        assert str(error) == "test message"


class TestTickerNotFoundError:
    """Test TickerNotFoundError."""

    def test_inherits_from_base(self):
        """Test that it inherits from PykabutanError."""
        assert issubclass(TickerNotFoundError, PykabutanError)

    def test_stores_code(self):
        """Test that it stores the code."""
        error = TickerNotFoundError("7203")
        assert error.code == "7203"

    def test_default_message(self):
        """Test default error message."""
        error = TickerNotFoundError("7203")
        assert "7203" in str(error)
        assert "not found" in str(error).lower()

    def test_custom_message(self):
        """Test custom error message."""
        error = TickerNotFoundError("7203", message="Custom message")
        assert str(error) == "Custom message"
        assert error.code == "7203"

    def test_can_catch_as_base(self):
        """Test that it can be caught as PykabutanError."""
        with pytest.raises(PykabutanError):
            raise TickerNotFoundError("7203")


class TestScrapingError:
    """Test ScrapingError."""

    def test_inherits_from_base(self):
        """Test that it inherits from PykabutanError."""
        assert issubclass(ScrapingError, PykabutanError)

    def test_stores_url(self):
        """Test that it stores the URL."""
        error = ScrapingError("https://example.com")
        assert error.url == "https://example.com"

    def test_default_message(self):
        """Test default error message."""
        error = ScrapingError("https://example.com")
        assert "example.com" in str(error)

    def test_custom_message(self):
        """Test custom error message."""
        error = ScrapingError("https://example.com", message="Parse failed")
        assert str(error) == "Parse failed"


class TestConfigurationError:
    """Test ConfigurationError."""

    def test_inherits_from_base(self):
        """Test that it inherits from PykabutanError."""
        assert issubclass(ConfigurationError, PykabutanError)

    def test_can_raise(self):
        """Test that it can be raised."""
        with pytest.raises(ConfigurationError):
            raise ConfigurationError("Invalid config")


class TestExceptionHierarchy:
    """Test exception hierarchy."""

    def test_all_exceptions_inherit_from_base(self):
        """Test that all exceptions inherit from PykabutanError."""
        exceptions = [
            TickerNotFoundError,
            ScrapingError,
            ConfigurationError,
        ]
        for exc in exceptions:
            assert issubclass(exc, PykabutanError)

    def test_can_catch_all_with_base(self):
        """Test that all exceptions can be caught with PykabutanError."""
        exceptions_to_raise = [
            TickerNotFoundError("7203"),
            ScrapingError("http://test"),
            ConfigurationError("bad config"),
        ]

        for exc in exceptions_to_raise:
            with pytest.raises(PykabutanError):
                raise exc
