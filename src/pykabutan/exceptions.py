"""Custom exceptions for pykabutan."""


class PykabutanError(Exception):
    """Base exception for pykabutan."""

    pass


class TickerNotFoundError(PykabutanError):
    """Raised when a stock code doesn't exist on kabutan.jp."""

    def __init__(self, code: str, message: str | None = None):
        self.code = code
        if message is None:
            message = f"Ticker '{code}' not found on kabutan.jp"
        super().__init__(message)


class ScrapingError(PykabutanError):
    """Raised when HTML parsing fails (site structure may have changed)."""

    def __init__(self, url: str, message: str | None = None):
        self.url = url
        if message is None:
            message = f"Failed to scrape data from {url}. Site structure may have changed."
        super().__init__(message)


class ConfigurationError(PykabutanError):
    """Raised for configuration issues."""

    pass
