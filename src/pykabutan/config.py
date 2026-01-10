"""Configuration management for pykabutan.

Usage:
    import pykabutan as pk

    # Change settings
    pk.config.timeout = 60
    pk.config.request_delay = 1.0

    # Or via config file (~/.pykabutan/config.json)
"""

import json
from pathlib import Path


class Config:
    """Configuration for pykabutan.

    Attributes:
        timeout: Request timeout in seconds (default: 30)
        request_delay: Delay between requests in seconds (default: 0.5)
        user_agent: User agent string for HTTP requests
    """

    _DEFAULT_TIMEOUT = 30
    _DEFAULT_REQUEST_DELAY = 0.5
    _DEFAULT_USER_AGENT = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    def __init__(self):
        self._timeout = self._DEFAULT_TIMEOUT
        self._request_delay = self._DEFAULT_REQUEST_DELAY
        self._user_agent = self._DEFAULT_USER_AGENT
        self._load_config_file()

    def _load_config_file(self):
        """Load configuration from ~/.pykabutan/config.json if it exists."""
        config_path = Path.home() / ".pykabutan" / "config.json"
        if config_path.exists():
            try:
                with open(config_path) as f:
                    data = json.load(f)
                if "timeout" in data:
                    self._timeout = data["timeout"]
                if "request_delay" in data:
                    self._request_delay = data["request_delay"]
                if "user_agent" in data:
                    self._user_agent = data["user_agent"]
            except (json.JSONDecodeError, OSError):
                pass  # Ignore invalid config files

    @property
    def timeout(self) -> int:
        """Request timeout in seconds."""
        return self._timeout

    @timeout.setter
    def timeout(self, value: int):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("timeout must be a positive number")
        self._timeout = int(value)

    @property
    def request_delay(self) -> float:
        """Delay between requests in seconds."""
        return self._request_delay

    @request_delay.setter
    def request_delay(self, value: float):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("request_delay must be a non-negative number")
        self._request_delay = float(value)

    @property
    def user_agent(self) -> str:
        """User agent string for HTTP requests."""
        return self._user_agent

    @user_agent.setter
    def user_agent(self, value: str):
        if not isinstance(value, str) or not value:
            raise ValueError("user_agent must be a non-empty string")
        self._user_agent = value

    def reset(self):
        """Reset all settings to defaults."""
        self._timeout = self._DEFAULT_TIMEOUT
        self._request_delay = self._DEFAULT_REQUEST_DELAY
        self._user_agent = self._DEFAULT_USER_AGENT


# Global config instance
config = Config()
