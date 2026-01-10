"""Unit tests for configuration."""

import pytest

from pykabutan.config import Config


class TestConfigDefaults:
    """Test Config default values."""

    def test_default_timeout(self):
        """Test default timeout is 30."""
        config = Config()
        assert config.timeout == 30

    def test_default_request_delay(self):
        """Test default request_delay is 0.5."""
        config = Config()
        assert config.request_delay == 0.5

    def test_default_user_agent(self):
        """Test default user_agent is set."""
        config = Config()
        assert config.user_agent is not None
        assert "Mozilla" in config.user_agent


class TestConfigSetters:
    """Test Config property setters."""

    def test_set_timeout(self):
        """Test setting timeout."""
        config = Config()
        config.timeout = 60
        assert config.timeout == 60

    def test_set_request_delay(self):
        """Test setting request_delay."""
        config = Config()
        config.request_delay = 1.5
        assert config.request_delay == 1.5

    def test_set_user_agent(self):
        """Test setting user_agent."""
        config = Config()
        config.user_agent = "CustomAgent/1.0"
        assert config.user_agent == "CustomAgent/1.0"


class TestConfigValidation:
    """Test Config validation."""

    def test_timeout_must_be_positive(self):
        """Test that timeout must be positive."""
        config = Config()
        with pytest.raises(ValueError):
            config.timeout = 0
        with pytest.raises(ValueError):
            config.timeout = -1

    def test_request_delay_must_be_non_negative(self):
        """Test that request_delay must be non-negative."""
        config = Config()
        with pytest.raises(ValueError):
            config.request_delay = -1
        # Zero should be allowed
        config.request_delay = 0
        assert config.request_delay == 0

    def test_user_agent_must_be_non_empty_string(self):
        """Test that user_agent must be non-empty string."""
        config = Config()
        with pytest.raises(ValueError):
            config.user_agent = ""
        with pytest.raises(ValueError):
            config.user_agent = None


class TestConfigReset:
    """Test Config reset method."""

    def test_reset_restores_timeout(self):
        """Test that reset restores timeout."""
        config = Config()
        config.timeout = 999
        config.reset()
        assert config.timeout == 30

    def test_reset_restores_request_delay(self):
        """Test that reset restores request_delay."""
        config = Config()
        config.request_delay = 999
        config.reset()
        assert config.request_delay == 0.5

    def test_reset_restores_user_agent(self):
        """Test that reset restores user_agent."""
        config = Config()
        original = config.user_agent
        config.user_agent = "Custom"
        config.reset()
        assert config.user_agent == original


class TestConfigTypes:
    """Test Config type handling."""

    def test_timeout_accepts_float(self):
        """Test that timeout accepts float (converts to int)."""
        config = Config()
        config.timeout = 30.5
        assert config.timeout == 30
        assert isinstance(config.timeout, int)

    def test_request_delay_accepts_int(self):
        """Test that request_delay accepts int (converts to float)."""
        config = Config()
        config.request_delay = 2
        assert config.request_delay == 2.0
        assert isinstance(config.request_delay, float)
