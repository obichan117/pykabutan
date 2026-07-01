"""Pure parsing functions: HTML/soup in, structured data out. No network I/O here."""

from bs4 import BeautifulSoup


def make_soup(html: str) -> BeautifulSoup:
    """Parse HTML text into a BeautifulSoup document (lxml backend)."""
    return BeautifulSoup(html, features="lxml")
