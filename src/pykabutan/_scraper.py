"""Internal scraper module for HTTP requests and HTML parsing.

This module is internal and should not be imported directly by users.
"""

import time
from io import StringIO

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Default configuration
_DEFAULT_TIMEOUT = 30  # seconds
_DEFAULT_REQUEST_DELAY = 0.5  # seconds
_DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

# Module-level state for rate limiting
_last_request_time: float = 0


def _get_config():
    """Get current configuration values.

    This allows config to be changed at runtime via pk.config.
    """
    # Import here to avoid circular imports
    try:
        from pykabutan.config import config

        return {
            "timeout": config.timeout,
            "request_delay": config.request_delay,
            "user_agent": config.user_agent,
        }
    except ImportError:
        return {
            "timeout": _DEFAULT_TIMEOUT,
            "request_delay": _DEFAULT_REQUEST_DELAY,
            "user_agent": _DEFAULT_USER_AGENT,
        }


def _rate_limit():
    """Apply rate limiting between requests."""
    global _last_request_time
    config = _get_config()
    delay = config["request_delay"]

    if delay > 0 and _last_request_time > 0:
        elapsed = time.time() - _last_request_time
        if elapsed < delay:
            time.sleep(delay - elapsed)

    _last_request_time = time.time()


def request_as_human(url: str) -> requests.Response:
    """Make HTTP GET request with proper headers to avoid 403 errors.

    Args:
        url: URL to fetch

    Returns:
        Response object with proper encoding set

    Raises:
        requests.RequestException: If request fails
    """
    _rate_limit()
    config = _get_config()

    response = requests.get(
        url,
        headers={"User-Agent": config["user_agent"]},
        timeout=config["timeout"],
    )
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    return response


def get_soup(url: str) -> BeautifulSoup:
    """Get BeautifulSoup object from URL.

    Args:
        url: URL to fetch and parse

    Returns:
        BeautifulSoup object
    """
    response = request_as_human(url)
    return BeautifulSoup(response.text, features="lxml")


def get_dfs(url: str) -> list[pd.DataFrame]:
    """Get list of DataFrames from all tables in HTML page.

    Args:
        url: URL to fetch

    Returns:
        List of DataFrames, one per table found
    """
    response = request_as_human(url)
    return pd.read_html(StringIO(response.text))


def get_dfs_from_soup(
    soup: BeautifulSoup,
    search_word: str | None = None,
    **kwargs,
) -> list[pd.DataFrame]:
    """Get DataFrames from BeautifulSoup object.

    Args:
        soup: BeautifulSoup object to parse
        search_word: Optional string to match in table (passed to pd.read_html match param)
        **kwargs: Additional arguments passed to pd.read_html

    Returns:
        List of DataFrames matching the criteria
    """
    return pd.read_html(StringIO(str(soup)), match=search_word, **kwargs)


def get_df_from_soup(
    soup: BeautifulSoup,
    search_word: str | None = None,
    **kwargs,
) -> pd.DataFrame:
    """Get first DataFrame from BeautifulSoup object matching criteria.

    Args:
        soup: BeautifulSoup object to parse
        search_word: Optional string to match in table
        **kwargs: Additional arguments passed to pd.read_html

    Returns:
        First DataFrame matching the criteria
    """
    return get_dfs_from_soup(soup, search_word, **kwargs)[0]
