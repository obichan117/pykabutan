# TASK-003: Custom Exceptions

**Status**: todo
**Priority**: high

## Description
Create custom exception classes for proper error handling.

## Acceptance Criteria
- [ ] Create `exceptions.py`
- [ ] Implement `TickerNotFoundError` for invalid stock codes
- [ ] Implement `ScrapingError` for parsing failures
- [ ] Implement `ConfigurationError` for config issues
- [ ] Add clear error messages

## Exception Classes
```python
class PykabutanError(Exception):
    """Base exception for pykabutan"""
    pass

class TickerNotFoundError(PykabutanError):
    """Raised when stock code doesn't exist on kabutan"""
    pass

class ScrapingError(PykabutanError):
    """Raised when HTML parsing fails (site structure changed?)"""
    pass

class ConfigurationError(PykabutanError):
    """Raised for configuration issues"""
    pass
```

## Notes
- All exceptions inherit from base `PykabutanError`
- Include helpful messages with context (e.g., which code failed)
