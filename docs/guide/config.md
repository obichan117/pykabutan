# Configuration Guide

pykabutan provides a global configuration object to customize request behavior.

## Accessing Config

```python
import pykabutan as pk

# Access the global config
config = pk.config
```

## Configuration Options

### Timeout

Maximum time (in seconds) to wait for HTTP responses:

```python
# Default: 30 seconds
print(pk.config.timeout)  # 30

# Set custom timeout
pk.config.timeout = 60
```

### Request Delay

Delay (in seconds) between consecutive HTTP requests:

```python
# Default: 0.5 seconds
print(pk.config.request_delay)  # 0.5

# Increase delay for more respectful scraping
pk.config.request_delay = 1.0

# Disable delay (not recommended)
pk.config.request_delay = 0
```

!!! note "Rate Limiting"
    The request delay helps avoid overloading kabutan.jp servers. A value of 0.5-1.0 seconds is recommended.

### User Agent

HTTP User-Agent header sent with requests:

```python
# Default: Chrome browser user agent
print(pk.config.user_agent)

# Set custom user agent
pk.config.user_agent = "MyApp/1.0"
```

## Reset to Defaults

Reset all configuration to default values:

```python
pk.config.timeout = 120
pk.config.request_delay = 5.0

# Reset everything
pk.config.reset()

print(pk.config.timeout)        # 30
print(pk.config.request_delay)  # 0.5
```

## Validation

Configuration values are validated:

```python
# Timeout must be positive
pk.config.timeout = 0    # Raises ValueError
pk.config.timeout = -1   # Raises ValueError

# Request delay must be non-negative
pk.config.request_delay = -1  # Raises ValueError

# User agent must be non-empty
pk.config.user_agent = ""    # Raises ValueError
pk.config.user_agent = None  # Raises ValueError
```

## Type Conversion

Values are automatically converted to the correct type:

```python
# Float timeout is converted to int
pk.config.timeout = 30.5
print(pk.config.timeout)  # 30 (int)

# Int delay is converted to float
pk.config.request_delay = 2
print(pk.config.request_delay)  # 2.0 (float)
```

## Default Values

| Option | Default | Type | Description |
|--------|---------|------|-------------|
| `timeout` | 30 | int | HTTP timeout in seconds |
| `request_delay` | 0.5 | float | Delay between requests |
| `user_agent` | Chrome UA | str | HTTP User-Agent header |

## Example: Bulk Operations

When making many requests, increase the delay:

```python
import pykabutan as pk

# Increase delay for bulk operations
pk.config.request_delay = 1.0

# Search multiple industries
industries = ["電気機器", "輸送用機器", "銀行業"]
all_results = []

for industry in industries:
    results = pk.search_by_industry(industry)
    all_results.extend(results)
    print(f"{industry}: {len(results)} stocks")

# Reset when done
pk.config.reset()
```
