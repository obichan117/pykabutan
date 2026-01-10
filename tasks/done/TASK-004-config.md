# TASK-004: Configuration System

**Status**: todo
**Priority**: medium

## Description
Create configuration management with sensible defaults and optional customization.

## Acceptance Criteria
- [ ] Create `config.py` with Config class
- [ ] Implement default values (timeout, delay, user_agent)
- [ ] Support module-level access: `pk.config.timeout = 60`
- [ ] Support JSON config file: `~/.pykabutan/config.json`
- [ ] Config file is optional (works without it)
- [ ] Validate configuration values

## Default Values
```python
DEFAULT_CONFIG = {
    "timeout": 30,           # seconds
    "request_delay": 0.5,    # seconds between requests
    "user_agent": "Mozilla/5.0 ...",
}
```

## Usage
```python
import pykabutan as pk

# Module-level (in-memory)
pk.config.timeout = 60

# File-based (~/.pykabutan/config.json)
# {
#   "timeout": 60,
#   "request_delay": 1.0
# }
```

## Notes
- Defaults must be sensible for beginners
- File config is loaded on import if exists
- Module-level changes override file config
