"""Pytest configuration and fixtures."""

from pathlib import Path

import pytest


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests (real HTTP requests)"
    )


@pytest.fixture
def fixtures_dir():
    """Path to the tests/fixtures directory."""
    return Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> str:
    """Read a fixture file from tests/fixtures as utf-8 text."""
    path = Path(__file__).parent / "fixtures" / name
    return path.read_text(encoding="utf-8")
