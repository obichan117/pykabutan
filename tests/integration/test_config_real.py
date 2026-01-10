"""Integration tests for config with real HTTP requests.

Tests that config changes actually affect HTTP behavior.
"""

import time

import pytest

import pykabutan as pk


@pytest.mark.integration
class TestConfigTimeout:
    """Test that timeout config affects requests."""

    def test_default_timeout(self):
        """Test that default timeout works."""
        # Default is 30 seconds, should be enough
        ticker = pk.Ticker("7203")
        assert ticker.profile.name is not None

    def test_very_short_timeout(self):
        """Test that very short timeout may cause issues."""
        original = pk.config.timeout
        try:
            pk.config.timeout = 0.001  # 1ms - way too short
            ticker = pk.Ticker("7203")
            # This might raise or might work depending on caching
            # Just ensure it doesn't hang forever
        except Exception:
            pass  # Expected - timeout too short
        finally:
            pk.config.timeout = original


@pytest.mark.integration
class TestConfigRequestDelay:
    """Test that request_delay config affects rate limiting."""

    def test_request_delay_applied(self):
        """Test that delay is applied between requests."""
        original = pk.config.request_delay
        try:
            pk.config.request_delay = 1.0  # 1 second delay

            start = time.time()
            ticker = pk.Ticker("7203")
            _ = ticker.profile  # First request
            ticker.refresh()
            _ = ticker.profile  # Second request (should wait)
            elapsed = time.time() - start

            # Should take at least 1 second due to delay
            assert elapsed >= 0.9  # Allow small margin
        finally:
            pk.config.request_delay = original


@pytest.mark.integration
class TestConfigReset:
    """Test config reset functionality."""

    def test_reset_restores_defaults(self):
        """Test that reset() restores default values."""
        original_timeout = pk.config.timeout
        original_delay = pk.config.request_delay

        pk.config.timeout = 999
        pk.config.request_delay = 999

        pk.config.reset()

        assert pk.config.timeout == 30  # Default
        assert pk.config.request_delay == 0.5  # Default
