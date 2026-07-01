"""Custom exceptions for pykabutan."""


class PykabutanError(Exception):
    """Base exception for pykabutan."""


class TickerNotFoundError(PykabutanError):
    """Raised when a stock code doesn't exist on kabutan.jp."""

    def __init__(self, code: str, message: str | None = None):
        self.code = code
        if message is None:
            message = f"Ticker '{code}' not found on kabutan.jp"
        super().__init__(message)


class ScrapingError(PykabutanError):
    """Raised when an expected page structure is missing.

    This usually means kabutan.jp changed its layout and pykabutan needs
    an update. The ``what`` attribute names the element that failed to parse.
    """

    def __init__(self, what: str, message: str | None = None):
        self.what = what
        if message is None:
            message = (
                f"Failed to parse {what} — kabutan.jp may have changed its layout. "
                "Try upgrading pykabutan or report the issue."
            )
        super().__init__(message)
