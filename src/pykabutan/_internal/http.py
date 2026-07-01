"""Internal HTTP layer: all network I/O for pykabutan.

Fetch functions return raw text; parsing happens in ``_internal.parsers``.
"""

import threading
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from pykabutan._internal import site
from pykabutan.config import config

_session: requests.Session | None = None
_session_lock = threading.Lock()

# Rate limiting: one politeness delay for the whole process, thread-safe.
_rate_lock = threading.Lock()
_last_request_time: float = 0.0


def _get_session() -> requests.Session:
    global _session
    if _session is None:
        with _session_lock:
            if _session is None:
                session = requests.Session()
                retry = Retry(
                    total=3,
                    backoff_factor=0.5,
                    status_forcelist=(429, 500, 502, 503),
                    allowed_methods=("GET",),
                )
                session.mount("https://", HTTPAdapter(max_retries=retry))
                _session = session
    return _session


def fetch(url: str) -> str:
    """Fetch a URL and return its body as text.

    Applies the configured rate limit, reuses a pooled connection with
    retries for transient errors, and raises ``requests.HTTPError`` for
    4xx/5xx responses that survive retries.
    """
    global _last_request_time
    session = _get_session()

    # Hold the lock while sleeping: concurrent callers must be spaced apart,
    # not released simultaneously after parallel sleeps.
    with _rate_lock:
        delay = config.request_delay
        if delay > 0 and _last_request_time > 0:
            elapsed = time.time() - _last_request_time
            if elapsed < delay:
                time.sleep(delay - elapsed)
        try:
            response = session.get(
                url,
                headers={"User-Agent": config.user_agent},
                timeout=config.timeout,
            )
        finally:
            _last_request_time = time.time()

    response.raise_for_status()
    response.encoding = site.ENCODING
    return response.text
